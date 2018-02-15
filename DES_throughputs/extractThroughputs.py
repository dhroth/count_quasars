from __future__ import print_function, division

import csv

wavelengths = []
gTrans = []
rTrans = []
iTrans = []
zTrans = []
YTrans = []

with open("transmissions.txt", "r") as inFile:
    for line in inFile:
        # first line is headers
        if line[0] == "#":
            continue

        # atmosphere contribution is already included in throughputs
        angstroms, g, r, i, z, Y, atm = list(map(float, line.split()))
        nm = angstroms / 10

        # only take the values at integer wavelengths
        # should probably average or something instead
        # of just throwing away the non-integer lambdas
        if nm - int(nm) == 0:
            wavelengths.append(nm)
            gTrans.append(g)
            rTrans.append(r)
            iTrans.append(i)
            zTrans.append(z)
            YTrans.append(Y)

for outFilename, throughput in [("total_g.dat", gTrans),
                                ("total_r.dat", rTrans),
                                ("total_i.dat", iTrans),
                                ("total_z.dat", zTrans),
                                ("total_Y.dat", YTrans)]:
    with open(outFilename, "w") as outFile:
        for i in range(len(wavelengths)):
            outFile.write("{} {}\n".format(wavelengths[i], throughput[i]))
