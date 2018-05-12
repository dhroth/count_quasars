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
