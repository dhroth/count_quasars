from __future__ import print_function, division

import sys

if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "input_file output_file")
    exit()

with open(sys.argv[1], "r") as inFile:
    with open(sys.argv[2], "w") as outFile:
        for line in inFile:
            if line[0] == "#":
                continue
            microns, throughput = list(map(float, line.split()))
            nm = microns * 1000

            # only keep integer nm to conform to format
            if nm == int(nm):
                outFile.write(str(nm) + " " + str(throughput) + "\n")
