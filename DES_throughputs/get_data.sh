#!/usr/bin/env bash

wget -O transmissions.txt http://www.ctio.noao.edu/noao/sites/default/files/DECam/STD_BANDPASSES_DR1.dat
wget -O README http://www.ctio.noao.edu/noao/sites/default/files/DECam/README_DR1_filters.txt

python extractThroughputs.py
