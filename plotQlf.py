"""

plot high redshift QLFs

"""
from __future__ import print_function, division

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colorbar import ColorbarBase
from matplotlib import gridspec

import config
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

# McGreer+2013; z=5
McGreer2013_parameters = (-2.03, -4.00, -27.21, 1.14815e-9, -0.47)
# McGreer+2018; z=5
McGreer2018_parameters = (-1.97, -4.00, -27.47, 1.07152e-9, -0.47)

# Kulkarni+2019 in prep
Kulkarni2019_z3p88_parameters = (-2.20, -4.19, -29.26,
                                 np.power(10.0, -7.92), 0.00)
Kulkarni2019_z4p35_parameters = (-2.20, -4.19, -27.38,
                                 np.power(10.0, -8.32), 0.00)
Kulkarni2019_z4p92_parameters = (-2.31, -4.51, -27.88,
                                 np.power(10.0, -9.02), 0.00)
Kulkarni2019_z6p00_parameters = (-2.40, -4.99, -29.12,
                                 np.power(10.0, -10.60), 0.00)


Manti2018_z4p75_parameters = (-1.76, -3.21, -24.06,
                              np.power(10.0, -5.87), 0.00)
Manti2018_z6p00_parameters = (-1.33, -3.16, -22.11,
                              np.power(10.0, -5.06), 0.00)

M1450_limits = (-18.0, -31.0)
M1450_limits = [-25.0, -29.0]

ms = np.linspace(M1450_limits[0], M1450_limits[1])

plt.figure(figsize=(10,7))

gs = gridspec.GridSpec(1, 2, width_ratios=[15,1])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

# put the QLFs in ax1
colors = ["#0000FF", "#4400BB", "#880088", "#BB0044", "#FF0000"]
zs = [4,5,6,7,8]

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
McGreer2013_qlf = qlf(McGreer2013_parameters, z, ms)
label = 'z = 5.00 (McGreer+2013): (-1.97, -4.00, -27.47, 1.148e-9, -0.47)'
ax1.semilogy(ms, McGreer2013_qlf, label=label,
             color='black', linestyle="--")

McGreer2018_qlf = qlf(McGreer2018_parameters, z, ms)
label = 'z = 5.00 (McGreer+2018): (-1.97, -4.00, -27.47, 1.148e-9, -0.47)'
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


cb = ColorbarBase(ax2, cmap=cmap, boundaries=bounds, ticks=ticks)
ax2.set_title("z")

plot_provenance()

plotfile = "results/QLFs_z4-8"
print()
print('Saving plotfile:', plotfile + '.png')
plt.savefig(plotfile + '.png')
plt.savefig(plotfile + '.svg')




# z from 4 to 6 including McGreer

M1450_limits = [-25.0, -29]

ms = np.linspace(M1450_limits[0], M1450_limits[1])

plt.figure(figsize=(10,7))
gs = gridspec.GridSpec(1, 2, width_ratios=[15,1])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

# put the QLFs in ax1
colors = ["#0000FF", "#4400BB", "#880088"]
zs = [4,5,6]
for z, color in zip(zs, colors):
    willottPhis = qlf(willott, z, ms)
    jiangPhis = qlf(jiang, z, ms)

    wLabel = "Willott+2018 QLF (-1.50, -2.81, -25.13)" \
        if z == 4 else None
    jLabel = "Jiang+2016 QLF (-1.90, -2.80, -25.20)" \
        if z == 4 else None

    ax1.semilogy(ms, willottPhis, label=wLabel, color=color)
    ax1.semilogy(ms, jiangPhis, label=jLabel, color=color, linestyle="--")


z = 5.0
McGreer2013_qlf = qlf(McGreer2013_parameters, z, ms)
label = 'z=5 (McGreer+2013): (-2.03, -4.00, -27.21)'
ax1.semilogy(ms, McGreer2013_qlf, label=label,
             color='black', linestyle="--")

McGreer2018_qlf = qlf(McGreer2018_parameters, z, ms)
label = 'z=5 (McGreer+2018): (-1.97, -4.00, -27.47)'
ax1.semilogy(ms, McGreer2018_qlf, label=label,
             color='black', linestyle="-")


#
Kulkarni2019_qlf = qlf(Kulkarni2019_z3p88_parameters, z, ms)
label = 'z = 3.88 (Kulkarni+2019)  2.07, -4.81, -27.26'
ax1.semilogy(ms, Kulkarni2019_qlf, label=label,
             color='red', linestyle=":")
Kulkarni2019_qlf = qlf(Kulkarni2019_z4p35_parameters, z, ms)
label = 'z = 4.35 (Kulkarni+2019)  2.20, -4.19, -27.38'
ax1.semilogy(ms, Kulkarni2019_qlf, label=label,
             color='red', linestyle=":")
Kulkarni2019_qlf = qlf(Kulkarni2019_z4p92_parameters, z, ms)
label = 'z = 4.92 (Kulkarni+2019) 2.31, -4.51, -27.88'
ax1.semilogy(ms, Kulkarni2019_qlf, label=label,
             color='red', linestyle="--")
Kulkarni2019_qlf = qlf(Kulkarni2019_z6p00_parameters, z, ms)
label = 'z = 6.00 (Kulkarni+2019) 2.40, -4.99, -29.12'
ax1.semilogy(ms, Kulkarni2019_qlf, label=label,
             color='red', linestyle="-")


Manti2018_qlf = qlf(Manti2018_z6p00_parameters, z, ms)
label = 'z = 6.00 (Manti+2018): (-1.33, -3.16, -22.11)'
ax1.semilogy(ms, Manti2018_qlf, label=label,
             color='orange', linestyle="-")


ax1.set_xlim(M1450_limits)
ax1.set_ylabel("Phi(M_1450) (Mpc^-3 mag^-1)")
ax1.set_xlabel("M_1450")
ax1.legend(fontsize='small')
ax1.grid()

# create the colorbar in ax2
cmap = ListedColormap(colors)

bounds = [3.5,4.5,5.5,6.5]
ticks = [4,5,6]

cb = ColorbarBase(ax2, cmap=cmap, boundaries=bounds, ticks=ticks)
ax2.set_title("z")

plot_provenance()

plotfile = "results/QLFs_z4-6"
print()
print('Saving plotfile:', plotfile + '.png')
plt.savefig(plotfile + '.png')
plt.savefig(plotfile + '.svg')




# z = 5

M1450_limits = [-25.0, -29]

ms = np.linspace(M1450_limits[0], M1450_limits[1])

plt.figure(figsize=(10,7))

gs = gridspec.GridSpec(1, 2, width_ratios=[15,1])
ax1 = plt.subplot(gs[0])


# put the QLFs in ax1
colors = ["#4400BB", "#880088"]
zs = [5]
for z, color in zip(zs, colors):
    willottPhis = qlf(willott, z, ms)
    jiangPhis = qlf(jiang, z, ms)

    wLabel = 'z = ' + '{:4.2f}'.format(z) \
             + '; Willott+2018 QLF (-1.50, -2.81, -25.13)'
    jLabel = 'z = ' + '{:4.2f}'.format(z) \
             + '; Jiang+2016 QLF (-1.90, -2.80, -25.20)'

    ax1.semilogy(ms, willottPhis, label=wLabel, color=color)
    ax1.semilogy(ms, jiangPhis, label=jLabel, color=color, linestyle="--")


z = 5.0
McGreer2013_qlf = qlf(McGreer2013_parameters, z, ms)
label = 'z=5 (McGreer+2013): (-2.03, -4.00, -27.21)'
ax1.semilogy(ms, McGreer2013_qlf, label=label,
             color='black', linestyle="--")

McGreer2018_qlf = qlf(McGreer2018_parameters, z, ms)
label = 'z=5 (McGreer+2018): (-1.97, -4.00, -27.47)'
ax1.semilogy(ms, McGreer2018_qlf, label=label,
             color='black', linestyle="-")


#
Kulkarni2019_qlf = qlf(Kulkarni2019_z4p92_parameters, z, ms)
label = 'z = 4.92 (Kulkarni+2019) 2.31, -4.51, -27.88'
ax1.semilogy(ms, Kulkarni2019_qlf, label=label,
             color='red', linestyle="--")


Manti2018_qlf = qlf(Manti2018_z4p75_parameters, z, ms)
label = 'z = 4.75 (Manti+2018): (-1.33, -3.16, -22.11)'
ax1.semilogy(ms, Manti2018_qlf, label=label,
             color='orange', linestyle="-")

ax1.set_xlim(M1450_limits)
ax1.set_ylabel("Phi(M_1450) (Mpc^-3 mag^-1)")
ax1.set_xlabel("M_1450")
ax1.legend(fontsize='small')
ax1.grid()

plot_provenance()

plotfile = "results/QLFs_z5"
print()
print('Saving plotfile:', plotfile + '.png')
plt.savefig(plotfile + '.png')
plt.savefig(plotfile + '.svg')



# z = 6

M1450_limits = [-25.0, -29]

ms = np.linspace(M1450_limits[0], M1450_limits[1])

plt.figure(figsize=(10,7))
gs = gridspec.GridSpec(1, 2, width_ratios=[15,1])
ax1 = plt.subplot(gs[0])

# put the QLFs in ax1
colors = ["#4400BB", "#880088"]
zs = [6]
for z, color in zip(zs, colors):
    willottPhis = qlf(willott, z, ms)
    jiangPhis = qlf(jiang, z, ms)

    wLabel = 'z = ' + '{:4.2f}'.format(z) \
             + '; Willott+2018 QLF (-1.50, -2.81, -25.13)'
    jLabel = 'z = ' + '{:4.2f}'.format(z) \
             + '; Jiang+2016 QLF (-1.90, -2.80, -25.20)'

    ax1.semilogy(ms, willottPhis, label=wLabel, color=color)
    ax1.semilogy(ms, jiangPhis, label=jLabel, color=color, linestyle="--")


Kulkarni2019_qlf = qlf(Kulkarni2019_z6p00_parameters, z, ms)
label = 'z = 6.00 (Kulkarni+2019) 2.40, -4.99, -29.12'
ax1.semilogy(ms, Kulkarni2019_qlf, label=label,
             color='red', linestyle="-")


Manti2018_qlf = qlf(Manti2018_z6p00_parameters, z, ms)
label = 'z = 6.00 (Manti+2018): (-1.33, -3.16, -22.11)'
ax1.semilogy(ms, Manti2018_qlf, label=label,
             color='orange', linestyle="-")


ax1.set_xlim(M1450_limits)
ax1.set_ylabel("Phi(M_1450) (Mpc^-3 mag^-1)")
ax1.set_xlabel("M_1450")
ax1.legend(fontsize='small')
ax1.grid()


plot_provenance()

plotfile = "results/QLFs_z6"
print()
print('Saving plotfile:', plotfile + '.png')
plt.savefig(plotfile + '.png')
plt.savefig(plotfile + '.svg')
