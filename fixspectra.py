from  __future__ import division

import sys
import os
import glob

import numpy as np

from astropy.table import Table

# This replaces 0's in flux with nonzero values to avoid
# log of zero problems in LSST phot utils
# and saves the spectrum to a directory/filename specified in the config file

inFilenames = glob.glob("nmSeds/qm1804_r*_ls_z*.dat")

for inFilename in inFilenames:
    print(inFilename)
    table = Table.read(inFilename, format='ascii')
    table.info('stats')

    print(table[0])
    print(table[1])
    print(table[2])
    non0 = np.where(table["col2"] !=0.0)[0]
    inon0 = non0[0]

    print(inon0, table["col1"][inon0], table["col2"][inon0])
    print(inon0-1, table["col1"][inon0-1], table["col2"][inon0-1])


    min_flux = np.nanmin(table["col2"])
    table["col2"][:inon0] = 1e-99

    print(0, table["col1"][0], table["col2"][0])
    print(1, table["col1"][1], table["col2"][1])
    print(inon0-1, table["col1"][inon0-1], table["col2"][inon0-1])
    print(inon0-2, table["col1"][inon0-2], table["col2"][inon0-2])
    print(inon0, table["col1"][inon0], table["col2"][inon0])

    table.info('stats')

    outFilename = inFilename
    table.write(inFilename, format='ascii.no_header')

sys.exit()


def test():

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
