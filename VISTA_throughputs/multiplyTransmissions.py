from __future__ import division
from __future__ import print_function

import numpy as np
from matplotlib import pyplot as plt

# EVERYTHING IS (coerced into) NM sigh

# qe/atm/j/h/k[nm] = transmission fraction
qe = np.zeros(2500)
atm = np.zeros(2500)
m1 = np.zeros(2500)
m2 = np.zeros(2500)

j = np.zeros(2500)
h = np.zeros(2500)
k = np.zeros(2500)

with open("qe.tab", "r") as qeFile:
    for line in qeFile:
        nm, percent = line.split(" ")
        nm = int(nm)
        percent = float(percent)
        if nm >= 2500:
            break
        qe[nm] = percent / 100

with open("trans_10_10.dat", "r") as atmFile:
    for i, line in enumerate(atmFile):
        # first 2 lines are header
        if i < 2:
            continue
        line = line.strip().split(" ")
        microns, fraction = (line[0], line[-1])
        microns = float(microns)
        nm = microns * 1000
        fraction = float(fraction)

        if round(nm) >= 2500:
            break

        # this is lazy (it overwrites the value when there are multiple
        # values per nanometer), but it's probably fine...
        atm[int(round(nm))] = fraction

dataFiles = [(m1, "VISTA_M1_Reflectivity_forETC_2009-Sep12.txt"),
             (m2, "VISTA_M2_Reflectivity_forETC_2007-Jun19.txt")]
for transmissions, filename in dataFiles:
    with open(filename, "r") as transFile:
        for line in transFile:
            line = line.strip().split(" ")
            nm, percent = (line[0], line[-1])
            nm = int(float(nm))
            if nm >= 2500:
                break
            fraction = float(percent) / 100
            transmissions[nm] = fraction

            # the file has only odd-numbered nm for lambda>800nm
            if nm > 800:
                transmissions[nm-1] = fraction

dataFiles = [(j, "VISTA_Filters_at80K_forETC_J.dat"),
             (h, "VISTA_Filters_at80K_forETC_H.dat"),
             (k, "VISTA_Filters_at80K_forETC_Ks.dat")]
for transmissions, filename in dataFiles:
    with open(filename, "r") as transFile:
        for line in transFile:
            line = line.strip().split(" ")
            nm, percent = (line[0], line[-1])
            nm = int(float(nm))
            if nm >= 2500:
                break
            fraction = float(percent) / 100

            transmissions[nm] = fraction

attenuation = qe*atm*m1*m2
jTot = j * attenuation
hTot = h * attenuation
kTot = k * attenuation

outFilenames = [(jTot, "VISTA_J_total.dat"),
                (hTot, "VISTA_H_total.dat"),
                (kTot, "VISTA_K_total.dat")]
for transmission, outFilename in outFilenames:
    with open(outFilename, "w") as outFile:
        for nm in range(2500):
            outFile.write(str(nm) + " " + str(transmission[nm]) + "\n")

x = np.arange(2500)
plt.plot(x, qe, color='c')
plt.plot(x, atm, color='k')
plt.plot(x, m1, color='r')
plt.plot(x, m2, color='g')
plt.plot(x, j, color='c')
plt.plot(x, h, color='g')
plt.plot(x, k, color='r')
plt.plot(x, jTot, color='c')
plt.plot(x, hTot, color='g')
plt.plot(x, kTot, color='r')
plt.ylim(0)
plt.xlim(800)
plt.show()
