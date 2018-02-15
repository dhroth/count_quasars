#!/usr/bin/env bash

wget -O transmissions.tar.gz http://www.eso.org/sci/facilities/paranal/instruments/vircam/inst/Filters_QE_Atm_curves.tar.gz
tar -xzf transmissions.tar.gz
mv Filters_QE_Atm_curves transmissions

# for some reason all the files in transmissions/ are gzipped
cd transmissions
gunzip *

# generate total_<filt>.dat files, move them up
python ../multiplyTransmissions.py
mv total_*.dat ..
cd ..
