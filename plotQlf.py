from __future__ import print_function
from __future__ import division

import config

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colorbar import ColorbarBase
from matplotlib import gridspec

from plot_provenance import plot_provenance

"""
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
"""

# Definition of Willott's quasar luminosity function
def qlf(params, z, m1450):
    alpha, beta, MBreak, phiBreak, k = params
    faintEnd = 10**(0.4 * (alpha + 1) * (m1450 - MBreak))
    brightEnd = 10**(0.4 * (beta + 1) * (m1450 - MBreak))
    redshiftEvolution = 10**(k * (z - 6))
    return redshiftEvolution * phiBreak / (faintEnd + brightEnd)


# plot the Willott and Jiang QLFs

# willott best-fit
# https://doi.org/10.1088/0004-6256/139/3/906
# http://adsabs.harvard.edu/abs/2010AJ....139..906W
# tuple with
# Faint end slope,
# Bright end slope
# Mstar
# PhiStar(1450)
# kPhiStar
willott = (-1.50, -2.81, -25.13, 1.14e-8, -0.47)

# maximum likelihood Jiang
jiang = (-1.90, -2.80, -25.20, 9.93e-9, -0.70)

# McGreer+2018; z=5
# 1.14815362e-9
McGreer2018_parameters = (-1.97, -4.00, -27.47, 1.148e-9, -0.47)

M1450_limits = (-18, -31)
M1450_limits = [-25.0, -29]

ms = np.linspace(M1450_limits[0], M1450_limits[1])

plt.figure(figsize=(10,7))
gs = gridspec.GridSpec(1, 2, width_ratios=[15,1])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

# put the QLFs in ax1
colors = ["#0000FF", "#4400BB", "#880088", "#BB0044", "#FF0000"]
zs = [4,5,6,7,8]

colors = ["#0000FF", "#4400BB", "#880088"]
zs = [4,5,6]
for z, color in zip(zs, colors):
    willottPhis = qlf(willott, z, ms)
    jiangPhis = qlf(jiang, z, ms)

    wLabel = "Willott+2018 QLF (-1.50, -2.81, -25.13, 1.14e-8, -0.47)" \
        if z == 4 else None
    jLabel = "Jiang+2016 QLF (-1.90, -2.80, -25.20, 9.93e-9, -0.70)" \
        if z == 4 else None

    ax1.semilogy(ms, willottPhis, label=wLabel, color=color)
    ax1.semilogy(ms, jiangPhis, label=jLabel, color=color, linestyle="--")


z = 5.0
McGreer2018_qlf = qlf(McGreer2018_parameters, z, ms)
label = 'z=5 (McGreer+2018): (-1.97, -4.00, -27.47, 1.148e-9, -0.47)'
ax1.semilogy(ms, McGreer2018_qlf, label=label,
             color='black', linestyle="-")

ax1.set_xlim(M1450_limits)
ax1.set_ylabel("Phi(M_1450) (Mpc^-3 mag^-1)")
ax1.set_xlabel("M_1450")
ax1.legend()
ax1.grid()

# create the colorbar in ax2
cmap = ListedColormap(colors)
bounds = [3.5,4.5,5.5,6.5,7.5,8.5]
ticks = [4,5,6,7,8]

bounds = [3.5,4.5,5.5,6.5]
ticks = [4,5,6]

cb = ColorbarBase(ax2, cmap=cmap, boundaries=bounds, ticks=ticks)
ax2.set_title("z")

plot_provenance()

plt.savefig("results/QLFs.svg")
plt.savefig("results/QLFs.png")
