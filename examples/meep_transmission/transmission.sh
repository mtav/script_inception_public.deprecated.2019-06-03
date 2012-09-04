#!/bin/bash

set -eux

CTL="transmission.ctl"

meep is-reference?=true $CTL | tee bend0.out
meep $CTL | tee bend.out
grep flux1: bend.out > bend.dat
grep flux1: bend0.out > bend0.dat

# meep sx=32 sy=64 is-reference?=true $CTL | tee bend0-big.out
# meep sx=32 sy=64 $CTL | tee bend-big.out
# grep flux1: bend-big.out > bend-big.dat
# grep flux1: bend0-big.out > bend0-big.dat

# /usr/bin/octave-3.2.3 ./transmission.m
# matlab_batcher.sh transmission
