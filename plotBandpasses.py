from __future__ import print_function, division

"""

 plot spectra and overplot survey filters

"""

import os
import sys

import subprocess
import sys
import os
import shutil
import argparse
import warnings
import datetime


import numpy as np
from matplotlib import pyplot as plt

import lsst.sims.photUtils.Bandpass as Bandpass
import lsst.sims.photUtils.Sed as Sed
import lsst.sims.photUtils.PhysicalParameters as PhysicalParameters

import scipy.integrate as integrate

import config

import getMags


if __name__ == '__main__':

    # plot the broadband filter bandpasses
    filters_LSST = ['u', 'g', 'r', 'i', 'z', 'y']
    for filter in filters_LSST:
        bp_wavelen, bp_trans = \
            getMags.getLsstThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.semilogx(bp_wavelen, bp_trans, alpha=0.8, color='blue',
                     label='LSST')

    filters_VISTA = ['Y', 'J', 'H', 'Ks']
    for filter in filters_VISTA:
        bp_wavelen, bp_trans = \
            getMags.getVistaThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        #for (irow, value) in enumerate(bp_trans):
        #    print(irow, bp_wavelen[irow], bp_trans[irow])
        bp_trans = bp_trans / bp_trans_max
        plt.plot(bp_wavelen, bp_trans, alpha=0.8, color='green',
                 label='VISTA')

    filters_WISE = ['W1', 'W2']
    for filter in filters_WISE:
        bp_wavelen, bp_trans = \
            getMags.getWiseThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.plot(bp_wavelen, bp_trans, alpha=0.8, color='red',
                 label='WISE')


    # plt.xlim(800.0, 3000.0)
    plt.xlim(300.0, 7000.0)

    plt.xlabel('Observed wavelength (nm)')
    plt.ylabel('Relative Transmission')

    # ax = plt.gca()
    # handles, labels = ax.get_legend_handles_labels()
    # legend(labels=labels[::-1])
    plt.title('LSST + VISTA + WISE bandpasses')
    plt.legend()
    plt.grid()

    plt.savefig('Bandpasses1.png')
    plt.show()
    plt.close()


    # plot just the Optical filter sets
    filters_LSST = ['u', 'g', 'r', 'i', 'z', 'y']
    for filter in filters_LSST:
        bp_wavelen, bp_trans = \
            getMags.getLsstThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.semilogx(bp_wavelen, bp_trans, alpha=0.8, color='blue',
                     label='LSST')

    filters_DES = ['g', 'r', 'i', 'z', 'y']
    for filter in filters_DES:
        bp_wavelen, bp_trans = \
            getMags.getDesThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.plot(bp_wavelen, bp_trans, alpha=0.8, color='orange',
                 linestyle='--', label='DES')


    filters_SDSS = ['u', 'g', 'r', 'i', 'z']
    for filter in filters_SDSS:
        bp_wavelen, bp_trans = \
            getMags.getSdssThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.plot(bp_wavelen, bp_trans, alpha=0.8, color='green',
                 linestyle='--', label='SDSS')


    # plt.xlim(800.0, 3000.0)
    plt.xlim(300.0, 1400.0)

    plt.xlabel('Observed wavelength (nm)')
    plt.ylabel('Relative Transmission')


    # ax = plt.gca()
    # handles, labels = ax.get_legend_handles_labels()
    # legend(labels=labels[::-1])
    plt.title('SDSS + DES + LSST bandpasses')
    plt.legend()
    plt.grid()

    plt.savefig('Bandpasses2.png')
    plt.show()
    plt.close()


    # zoom in on izY
    # plot just the Optical filter sets
    filters_LSST = ['i', 'z', 'y']
    for filter in filters_LSST:
        bp_wavelen, bp_trans = \
            getMags.getLsstThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.semilogx(bp_wavelen, bp_trans, alpha=0.8, color='blue',
                     label='LSST')

    filters_DES = ['i', 'z', 'y']
    for filter in filters_DES:
        bp_wavelen, bp_trans = \
            getMags.getDesThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.plot(bp_wavelen, bp_trans, alpha=0.8, color='orange',
                 linestyle='--', label='DES')


    filters_SDSS = ['i', 'z']
    for filter in filters_SDSS:
        bp_wavelen, bp_trans = \
            getMags.getSdssThroughput(filter).getBandpass()
        bp_trans_max = np.max(bp_trans)
        print('filter maximum transmission:', filter, bp_trans_max,
              len(bp_trans), np.min(bp_wavelen), np.max(bp_wavelen))
        bp_trans = bp_trans / bp_trans_max
        plt.plot(bp_wavelen, bp_trans, alpha=0.8, color='green',
                 linestyle='--', label='SDSS')


    # plt.xlim(800.0, 3000.0)
    plt.xlim(650.0, 1250.0)

    plt.xlabel('Observed wavelength (nm)')
    plt.ylabel('Relative Transmission')

    # ax = plt.gca()
    # handles, labels = ax.get_legend_handles_labels()
    # legend(labels=labels[::-1])
    plt.title('SDSS + DES + LSST izy bandpasses')
    plt.legend()
    plt.grid()

    plt.savefig('Bandpasses3.png')
    plt.show()
    plt.close()
