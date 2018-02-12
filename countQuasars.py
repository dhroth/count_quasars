from __future__ import print_function, division

from matplotlib import pyplot as plt
import scipy.integrate as integrate
import numpy as np
from getMags import quasarMag
import scipy.stats
import subprocess
import sys
import os
import shutil
import argparse
import warnings
import datetime

import config

# parse input argument
parser = argparse.ArgumentParser(description="")
parser.add_argument("-s", "--saveOutput", help="Save output to disk",
                    action="store_true")
parser.add_argument("-f", "--forceOverwrite", help="Overwrite output files " +
                    "if they already exist", action="store_true")
parser.add_argument("-x", "--minLimitingDepth",
                    help="x-axis minimum value", type=float)
parser.add_argument("-X", "--maxLimitingDepth",
                    help="x-axis maximum value", type=float)
parser.add_argument("-y", "--yMin", help="y-axis minimum value", type=float)
parser.add_argument("-Y", "--yMax", help="y-axis maximum value", type=float)
args = parser.parse_args()

for opt in ["minLimitingDepth", "maxLimitingDepth", "yMin", "yMax"]:
    argVal = getattr(args, opt)
    if argVal is not None:
        setattr(config, opt, argVal)

# read in Willott's 100 bootstrapped QLF parameters
# assuming alpha and k are constant as described in the paper
qlfParams = []
alpha = -1.5
k = config.k
with open(config.qlfParamsFilename, "r") as paramsFile:
    for line in paramsFile:
        # each line is log(phi*), beta, M*
        logPhiBreak, beta, MBreak = map(float, line.split())
        phiBreak = 10**logPhiBreak
        qlfParams.append((alpha, beta, MBreak, phiBreak, k))

#jiang = (-1.9,-2.8,-25.2,9.93e-9,-0.7)
#qlfParams = [jiang]

# Definition of Willott's quasar luminosity function
def qlf(params, z, m1450):
    alpha, beta, MBreak, phiBreak, k = params
    faintEnd = 10**(0.4 * (alpha + 1) * (m1450 - MBreak))
    brightEnd = 10**(0.4 * (beta + 1) * (m1450 - MBreak))
    redshiftEvolution = 10**(k * (z - 6))
    return redshiftEvolution * phiBreak / (faintEnd + brightEnd)

# helper functions for cosmology calculations
def E(z):
    # this is the denominator for various things
    return np.sqrt(config.omegaM * (1+z)**3 + config.omegaLambda)

def VC(z, dz, Omega):
    # get the comoving volume between redshift z and z+dz
    # over sky area Omega (in radians)
    
    # get the comoving distance to redshift z
    DC = config.DH * integrate.quad(lambda zp: 1/E(zp), 0, z)[0]

    # angular diameter distance to redshift z
    DA = DC / (1 + z)

    # the infinitessimal comoving volume element is related
    # to d\Omega dz as shown
    dVC = config.DH * (1 + z)**2 * DA**2 / E(z) # * d\Omega * dz

    # multiply through to get the comoving volume
    VC = dVC * Omega * dz
    VC = VC * config.m2pc**3 * (10**-6)**3
    return VC

# limitingDepths is the array of depths that we calculate # detections for
limitingDepths = np.arange(config.minLimitingDepth,
                           config.maxLimitingDepth,
                           config.limitingDepthStep)

# numQuasarsAbove[zCutoff] contains the number of quasars that are detected
# above redshift zCutoff
# TODO (yes this is kind of dumb -- I should store num detections by redshift
#       and do a cumulative sum...)
numQuasarsAbove = {zCutoff: np.zeros((len(qlfParams), len(limitingDepths)))
                   for zCutoff in config.zCutoffs}

# Integrate (numerically) over the redshift and intrinsic luminosity (M1450),
# summing up the number of quasars detected at each redshift and M1450 bin
for z in np.arange(config.zMin, config.zMax, config.zStep):
    # get the comoving volume at this redshift
    volume = VC(z, config.zStep, config.skyArea * (np.pi/180)**2)
    # now do the integral over M1450
    for M1450 in np.arange(config.M1450Min, config.M1450Max, config.M1450Step):
        # calculate the number of detections for each bootstrapped qlf
        # parameter tuple (so we can get mean and variance of final answer)
        for trialId in range(len(qlfParams)):
            # the qlf returns number of quasars / comoving volume / magnitude
            quasarDensity = qlf(qlfParams[trialId], z, M1450) 
            # to get the actual number of quasars, multiply by volume and magnitude
            numNewQuasars = quasarDensity * volume * config.M1450Step
            # get the apparent magnitude of quasars of this M1450 at redshift z
            yMag = quasarMag(z, M1450, config.survey, config.f)
            for zCutoff in config.zCutoffs[z >= config.zCutoffs]:
                # increment numQuasarsAbove by the number of new quasars found
                # for limiting depths greater than the apparent magnitude of
                # the quasar
                numQuasarsAbove[zCutoff][trialId,:][limitingDepths > yMag] += numNewQuasars

# get the mean and variance at each limiting depth for each zCutoff
# (mean and variance calculated over the sampled qlf parameters)
meanNumQuasarsAbove = {}
oneSigmaNumQuasarsAbove = {}
for zCutoff in config.zCutoffs:
    meanNumQuasarsAbove[zCutoff] = np.mean(numQuasarsAbove[zCutoff], axis=0)
    oneSigmaNumQuasarsAbove[zCutoff] = np.std(numQuasarsAbove[zCutoff], axis=0)

# plot one line and error envelope for each zCutoff
for zCutoff, zColor in zip(config.zCutoffs, config.zColors):
    mu = meanNumQuasarsAbove[zCutoff]
    sigma = oneSigmaNumQuasarsAbove[zCutoff]
    # plot the means
    plt.semilogy(limitingDepths, mu, color=zColor, label="z>=" + str(zCutoff))
    # plot the error envelopes
    plt.fill_between(limitingDepths,
                     (mu - config.errorNSigma * sigma).clip(config.yMin),
                     (mu + config.errorNSigma * sigma).clip(config.yMin),
                     alpha=config.errorEnvelopeAlpha,
                     color=zColor)

# put vertical lines to indicate (potentially planned) achieved depths
if len(config.depths) > 0:
    # you can specify multiple achieved depths in the conifg file, each
    # with a label and an x and y position
    for depth, label, x, y in zip(config.depths, config.labels,
                                  config.depthLabelXs, config.depthLabelYs):
        # make the vertical line
        plt.axvline(x=depth, linestyle="--", color='k')
        # format the depth to have one decimal point
        depthStr = "{0:,.1f}".format(depth)
        # make the text label
        plt.annotate(label + " " + config.f + " median $" + str(config.depthNSigma) +
                     "\sigma$ depth=" + depthStr, xy=(x, y))

# plot labels/legend/grid/limit/title
plt.legend(loc="upper left")
plt.xlabel("Limiting depth in {}-{}".format(config.survey, config.f))
areaStr = "{:,d}".format(int(round(config.skyArea)))
plt.ylabel("# quasars detected with $M_{1450}$<" + str(config.M1450Max) +
           " (" + areaStr + " sq. deg.)")
if config.plotGrid:
    plt.grid()
plt.ylim(config.yMin, config.yMax)
plt.xlim(config.minLimitingDepth, config.maxLimitingDepth)
plt.title(config.plotTitle)

# put provenance on the side of the plot
try:
    gitHash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
except subprocess.CalledProcessError as e:
    print("You need to be in a git repository in order to put provenance " +
          "information on the plots. Please clone the repository instead " +
          "of downloading the source files directly, and ensure that your " +
          "local git repo hasn't been corrupted")
    exit()
gitHash = gitHash.decode("utf-8")
try:
    producer = subprocess.check_output(["git", "config", "user.name"]).strip()
except subprocess.CalledProcessError as e:
    print("You have not set the git user.name property, which is needed " +
          "to add provenance information on the plots. You can set this " +
          "property globally using the command git config --global " +
          "user.name '<my name>'")
    exit()
provenance = producer.decode("utf-8") + ", " + gitHash
provenance += "\n Using {} QLF with k={:2.4f}".format(config.qlfName, config.k)
plt.figtext(0.93, 0.5, provenance, rotation="vertical",
            verticalalignment="center", alpha=0.7)

if not args.saveOutput:
    plt.show()
    exit()

# if we get here we need to save output

overwriteError = "Output path {} already exists. Refusing to overwrite. "
overwriteError += "Specify -f or --forceOverwrite to force overwriting."

# save one .tbl file for each zCutoff
date = datetime.datetime.now().strftime("%Y-%m-%d")
outPath = config.outputDir.format(config.survey, config.f, date)
if not os.path.exists(outPath):
    os.makedirs(outPath)
for z in config.zCutoffs:
    outFilename = config.outFilenameTbl.format(config.survey, config.f,
                                               config.reddening, z, date)
    outFilename = os.path.join(outPath, outFilename)

    # refuse to overwrite data table files
    if os.path.exists(outFilename) and not args.forceOverwrite:
        warnings.warn(overwriteError.format(outFilename))
    else:
        mus = meanNumQuasarsAbove[z]
        sigmas = oneSigmaNumQuasarsAbove[z]
        with open(outFilename, "w") as outFile:
            outFile.write("limitingDepth,numDetections,oneSigma\n")
            for depth, count, oneSigma in zip(limitingDepths, mus, sigmas):
                outFile.write("{:.1f},{:.2f},{:.2f}\n".format(depth, count, oneSigma))

# save the plot
outFilename = config.outFilenamePlt.format(config.survey, config.f,
                                           config.reddening, date)
outFilename = os.path.join(outPath, outFilename)
if os.path.exists(outFilename) and not args.forceOverwrite:
    # refuse to overwrite plot files unless --force is specified
    warnings.warn(overwriteError.format(outFilename))
else:
    plt.savefig(outFilename)

# copy the config file currently in use into outPath
confDest = os.path.join(outPath, "countQuasars.conf")
if not os.path.exists(confDest):
    shutil.copyfile("countQuasars.conf", confDest)
else:
    # No error is thrown if the config file already exists -- we assume the
    # user makes no changes between config files besides the survey/filter and
    # the reddening, but this is not enforced
    pass

# copy the command line arguments into outPath
with open(os.path.join(outPath, "commandArgs.txt"), "w") as outFile:
    outFile.write(" ".join(sys.argv[1:]))
