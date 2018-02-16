#!/usr/bin/env bash

wget -O transmissions.tar http://www.ukidss.org/technical/photom/hewett-ukidss-tables.tar
mkdir transmissions
mv transmissions.tar transmissions
cd transmissions
tar -xf transmissions.tar

cd transmissions

OLDIFS=$IFS
IFS=','
for i in 'Table02_online.dat','Z' \
         'Table03_online.dat','Y' \
         'Table04_online.dat','J' \
         'Table05_online.dat','H' \
         'Table06_online.dat','K'
do
    set -- $i
    python ../convertThroughput.py $1 total_$2.dat
done

IFS=$OLDIFS

mv total_*.dat ..
