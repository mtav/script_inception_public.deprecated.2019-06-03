#!/bin/bash
set -eux

for dir in wood*
do
  grep freq $dir/data.out | awk --field-separator "," '{ for (x=2; x<=NF; x++) {  printf "%s ", $x } printf "\n" }' | sed 's/k index/k_index/' | sed 's/band \([0-9]*\)/band_\1/g' | sed 's/kmag\/2pi/kmag_over_2pi/' >$dir/band.dat
done

