from matplotlib import pyplot as plt
import scipy.integrate as integrate
import numpy as np
from getMags import quasarMag
import scipy.stats
import subprocess

import config

# read in Willott's 100 bootstrapped QLF parameters
# assuming alpha and k are constant as described in the paper
qlfParams = []
alpha = -1.5
k = -0.47
with open(config.qlfParamsFilename, "r") as paramsFile:
    for line in paramsFile:
        # each line is log(phi*), beta, M*
        logPhiBreak, beta, MBreak = map(float, line.split())
        phiBreak = 10**logPhiBreak
        qlfParams.append((alpha, beta, MBreak, phiBreak, k))

# this commented code independently generates all the QLF parameters
# I'll probably delete it soon, since the params strongly covary
"""
numTrials = 3

alphaMean = -1.5
alphaSigma = 0.1*0

betaMean = -2.81
betaSigma = 0.25*0

kMean = -0.47
kSigma = 0.1*0

MBreakMean = -25.13
MBreakSigma = 0

phiBreakMean = 1.14*10**-8
phiBreakSigma = 3e-9*0

alphas    = scipy.stats.norm(loc=alphaMean,    scale=alphaSigma   ).rvs(numTrials)
betas     = scipy.stats.norm(loc=betaMean,     scale=betaSigma    ).rvs(numTrials)
ks        = scipy.stats.norm(loc=kMean,        scale=kSigma       ).rvs(numTrials)
MBreaks   = scipy.stats.norm(loc=MBreakMean,   scale=MBreakSigma  ).rvs(numTrials)
phiBreaks = scipy.stats.norm(loc=phiBreakMean, scale=phiBreakSigma).rvs(numTrials)

qlfParams = zip(alphas, betas, MBreaks, phiBreaks, ks)
"""

# Definition of Willott's quasar luminosity function
def qlf(params, z, m1450):
    alpha, beta, MBreak, phiBreak, k = params
    faintEnd = 10**(0.4 * (alpha + 1) * (m1450 - MBreak))
    brightEnd = 10**(0.4 * (beta + 1) * (m1450 - MBreak))
    redshiftEvolution = 10**(k * (z - 6))
    return redshiftEvolution * phiBreak / (faintEnd + brightEnd)

"""
# plot the QLF
ms = np.linspace(-22, -28)
phis = qlf(6, ms)
plt.semilogy(ms, phis)
plt.xlim(-22, -28)
plt.show()
"""

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
                     (mu - config.errorNSigma * sigma).clip(config.plotYMin),
                     (mu + config.errorNSigma * sigma).clip(config.plotYMin),
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
areaStr = "{:,d}".format(round(config.skyArea))
plt.ylabel("# quasars detected with $M_{1450}$<" + str(config.M1450Max) +
           " (" + areaStr + " sq. deg.)")
if config.plotGrid:
    plt.grid()
plt.ylim(config.plotYMin, config.plotYMax)
plt.title(config.plotTitle)

# put provenance on the side of the plot
gitHash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
producer = subprocess.check_output(["git", "config", "user.name"]).strip()
provenance = producer.decode("utf-8") + ", " + gitHash.decode("utf-8")
plt.figtext(0.93, 0.5, provenance, rotation="vertical",
            verticalalignment="center", alpha=0.7)
plt.show()
