import os
import sys
from matplotlib import pyplot as plt
import lsst.sims.photUtils.Bandpass as Bandpass
import lsst.sims.photUtils.Sed as Sed
import scipy.integrate as integrate
import numpy as np

import config

def getLsstThroughput(f):
    if f not in ["u", "g", "r", "i", "z", "y"]:
        raise ValueError("LSST does not have a {} filter".format(f))
    # Get the throughputs directory using the 'throughputs' package env variables.
    throughputsDir = os.getenv('LSST_THROUGHPUTS_BASELINE')
    throughputsFile = os.path.join(throughputsDir, 'total_{}.dat'.format(f))

    # read the throughputs file into lsstBand
    lsstBand = Bandpass()
    lsstBand.readThroughput(throughputsFile)
    return lsstBand

def getWiseThroughput(f):
    if f not in ["W1", "W2"]:
        raise ValueError("WISE does not have a {} filter".format(f))
    # the WISE throughputs are in a subdirectory WISE, not baseline
    throughputsDir = os.getenv('LSST_THROUGHPUTS_BASELINE')
    throughputsFile = os.path.join(throughputsDir, '..', 'WISE',
                                   'WISE_{}.dat'.format(f.lower()))

    # TODO hacky to set the min/max wavelengths, but I think readThroughput
    # complains because the files don't overlap in wavelength with what it's
    # expecting. Sad!
    wiseBand = Bandpass()
    if f == 'W1':
        wavelen_min = 2600
        wavelen_max = 4000
    elif f == 'W2':
        wavelen_min = 3890
        wavelen_max = 5560

    wiseBand.readThroughput(throughputsFile,
                            wavelen_min=wavelen_min,
                            wavelen_max=wavelen_max,
                            wavelen_step=10)
    return wiseBand

def getVistaThroughput(f):
    if f not in ['J', 'H', 'K']:
        raise ValueError("VISTA does not have a {} filter".format(f))

    throughputsDir = "VISTA_throughputs"
    throughputsFile = os.path.join(throughputsDir, 'VISTA_{}_total.dat'.format(f))
    vistaBand = Bandpass()
    vistaBand.readThroughput(throughputsFile)
    return vistaBand

def getDesThroughput(f):
    if f not in ["u", "g", "r", "i", "z", "y"]:
        raise ValueError("DES does not have a {} filter".format(f))
    throughputsDir = "DES_throughputs"
    throughputsFile = os.path.join(throughputsDir, "total_{}.dat".format(f))
    desBand = Bandpass()
    desBand.readThroughput(throughputsFile)
    return desBand

def f2Throughput(survey, f):
    if survey == "LSST":
        return getLsstThroughput(f)
    elif survey == "WISE":
        return getWiseThroughput(f)
    elif survey == "VISTA":
        return getVistaThroughput(f)
    elif survey == "DES":
        return getDesThroughput(f)
    else:
        raise RuntimeError("Invalid survey name {}".format(survey))

# cache results of quasarMag in magCache
magCache = {}
def quasarMag(z, M1450, survey, f):
    if (z, M1450, survey, f) in magCache:
        return magCache[(z, M1450, survey, f)]
    # for files containing $\lambda$ / F$_\lambda$, we use the Sed method
    # readSED_flambda. For files containing $\lambda$ / F$_\nu$,
    # we would use the readSED_fnu method instead.

    # get the path to the SED file for this z
    sedFilename = config.sedFilenameFormat.format(config.reddening, z)
    spectrumFilename = os.path.join(config.sedDir, sedFilename)

    # Read the spectrum.
    agn = Sed()
    agn.readSED_flambda(spectrumFilename)

    # Suppose you had a spectrum, but it didn't have an absolute scale. Or you
    # wanted to scale it to have a given magnitude in a particular bandpass.
    # For example, say we wanted to make our 'agn' spectrum have an r band
    # magnitude of 20, then calculate the magnitudes in all bandpasses. We
    # just use the calcFluxNorm and multiplyFluxNorm methods.


    # Scale spectrum and recalculate magnitudes.

    # given an absolute M1450, the observed magnitude m corresponding
    # to rest-frame 145nm radiation is
    # m = M1450+5log(d_L/10pc) - 2.5log(1+z)
    # so let's calculate m and then normalize our spectrum to that

    # first we need d_L = (1+z) * comoving distance
    # comoving distance is D_hubble * int_0^z dz'/sqrt(omegaM(1+z)^3+omegaLambda)
    def E(zp):
        return np.sqrt(config.omegaM * (1+zp)**3 + config.omegaLambda)
    DC = config.DH * integrate.quad(lambda zp: 1/E(zp), 0, z)[0]
    DL = (1 + z) * DC
    DL = DL * config.m2pc
    m = M1450 + 5 * np.log10(DL / 10) - 2.5 * np.log10(1 + z)

    # make a square bandpass at 145nm (in the quasar rest frame)
    # with a width of 1nm
    wavelen = np.arange(300, 2000, 0.1)
    sb = np.zeros(wavelen.shape)
    id1450 = int(((145 * (1 + z)) - 300) / 0.1)
    sb[id1450-5:id1450+5] = 1
    band1450 = Bandpass(wavelen=wavelen, sb=sb)

    # normalize the sed to m at the (rest-frame) 1450A bandpass
    fluxNorm = agn.calcFluxNorm(m, band1450)
    agn.multiplyFluxNorm(fluxNorm)

    # Calculate expected AB magnitudes in the requested lsst band 
    bandpass = f2Throughput(survey, f)
    mag = agn.calcMag(bandpass)
    magCache[(z, M1450, survey, f)] = mag
    return mag
