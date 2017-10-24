# Introduction

This project aims to compute how many quasars could be detected by an
astronomical survey. For any filter of interest, this code will produce
a plot of # quasar detections vs. limiting magnitude with curves showing
how many quasars will be found above specified redshift cutoffs.

The code uses simulated quasar lightcurves to calculate the expected
magnitude of quasars at many redshifts. It then integrates, over
redshift and over absolute quasar magnitude, the number density
of quasars as given by a parameterized quasar luminosity function.

# Prerequisites
1. Python 3 (adapting the code to Python 2 should be straightforward)
2. `numpy`, `scipy`, `matplotlib`
3. `sims_photUtils` from the LSST stack

If you don't already have the LSST software stack on your machine, getting
`sims_photUtils` may be difficult. If possible, you should install the
stack from source, since the simulations stack no longer supports conda.
However, in practice this is very difficult to do. To install `sims_photUtils`
using conda, follow the instructions here:
https://confluence.lsstcorp.org/display/SIM/Catalogs+and+MAF#CatalogsandMAF-BinaryInstallation
and then install `sims_photUtils` using
```
conda install lsst-sims-photutils
```

# Configuration

The code has many configuration options located in countQuasars.conf.
The parameters are documented in the file.

# Output

When run with the --dryrun argument, the `countQuasars.py` script will show the
output plot but will not save any results to disk. When this argument is not
present, it will save the output plot and tables respectively to
`config.outputDir/<current git revision>/config.outFilenamePlt(Tbl)`.
Because the output filenames are
formatted with only the survey, filter, and reddening (as documented in the
config file), it is important to commit any changes you make to the config file
or the code between output-saving runs unless the changes are made exclusively
to `config.survey`, `config.f`, and `config.reddening`, since those parameters
are saved in the filenames themselves.

The config file currently in use is also saved to
`config.outputDir/<current git revision>`
