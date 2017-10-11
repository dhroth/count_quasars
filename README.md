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

# Plot Provenance

The output of this code is a plot. On the right side of the plot, the code
puts the name of the person who ran the code and the git revision hash.
This is done so plots can be reproduced. Therefore, it is important that
you commit all of your changes immediately before making any plots that
you intend to save, since otherwise, the git version will not refer to
the code that actually ran to generate the plot.
