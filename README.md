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
1. Python 2 or 3 (see below for which to choose)
2. `numpy`, `scipy`, `matplotlib`
3. `sims_photUtils` from the LSST stack

If you don't already have the LSST software stack on your machine, getting
`sims_photUtils` may be difficult. If possible, you should install the
stack from source, since the simulations stack no longer supports conda.
In this case, you should use Python 3, since the LSST stack is mostly
moving to Python 3.

However, in practice, installing the LSST stack from source
is very difficult to do. Instead, you can install an old version
of `sims_photUtils` using conda by running the following commands:
```
conda update conda
conda config --add channels http://conda.lsst.codes/sims
conda install lsst-sims-photutils
```
This will add the lsst sims conda distribution channel and then install
`sims_photUtils` along with all of its dependencies. In this case, I think
you may need to use Python 2, but I'm not entirely sure.

Note that installing an old version in this way may downgrade packages
pip and astropy. I recommend installing `lsst-sims-photutils` in a conda
virtual environment.

Before running code in this repository, you need to set up the
`sims_photUtils` package. First, source the correct loadLSST file for
your terminal. This should be located in the bin directory for your
conda virtual environment if you installed with conda, or in the root
directory of your stack install if you installed from source.
You might be able to get the path by running `setup` with no arguments.
```
source path/to/conda/env/or/stack/root/loadLSST.myshell
```
Then set up the `sims_photUtils` package:
```
setup sims_photUtils
```


# Configuration

The code has many configuration options located in countQuasars.conf.
The parameters are documented in the file.

# Output

When run without any options, the `countQuasars.py` script will show the
output plot but will not save any results to disk. When the --saveOutput
argument is present, it will save the output plot and tables respectively to
`config.outputDir/<current git revision>/config.outFilenamePlt(Tbl)`.
Because the output filenames are
formatted with only the survey, filter, and reddening (as documented in the
config file), it is important to commit any changes you make to the config file
or the code between output-saving runs unless the changes are made exclusively
to `config.survey`, `config.f`, and `config.reddening`, since those parameters
are saved in the filenames themselves.

The config file currently in use is also saved to
`config.outputDir/<current git revision>`
