from  __future__ import division

import sys
import os
import glob

import config

# This file converts the wavelength column in spectra
# from angstroms to nanometers
# It also parses the redshift and reddening from the strange
# filename format (where z is multiplied by 100 and the reddening by 1000)
# and saves the spectrum to a directory/filename specified in the config file

inFilenames = glob.glob("HZQ_Tracks_PH_20170817/qm1708_*_ls_*.dat")

for inFilename in inFilenames:
    with open(inFilename, "r") as inFile:
        base = os.path.basename(inFilename)
        parts = base.split("_")
        reddening = parts[1]
        if reddening[0] == "m":
            # if reddning starts with m, it's actually negative O.o
            reddening = int(reddening[1:]) / 1000. * -1
        else:
            reddening = int(reddening) / 1000.
        z = parts[3].split(".")[0]
        z = int(z) / 100.

        outFilename = config.sedFilenameFormat.format(reddening, z)
        outPath = os.path.join(config.sedDir, outFilename)
        if os.path.exists(outPath):
            raise RuntimeError("Refusing to overwrite file %s" % outPath)

        with open(outPath, "w") as outFile:
            # TODO this is hacky -- put a value of 0 at 300 nm so that there's
            # more likely to be some overlap with the bandpasses so that the 
            # lsst sims_photUtils code doesn't crash when the redshifted SED has
            # no flux in some bandpass we care about
            outFile.write("300.0 0.0\n")
            for line in inFile:
                # parse lambda and F_lambda, convert to nm, and output
                line = line.strip().split(" ")
                lambdaAngstroms = float(line[0].strip())
                fLambda = line[-1].strip()

                lambdaNm = lambdaAngstroms / 10

                outFile.write(str(lambdaNm) + " " + fLambda + "\n")
