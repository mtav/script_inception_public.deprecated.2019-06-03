#!/bin/bash
#
#PBS -l walltime=360:00:00
#PBS -mae
#PBS -joe
#PBS -l nodes=1:ppn=4
#


export WORKDIR=$HOME/sims/FDTD32/MikeT/Andrew_pillars/pillar_M3687_1_5
export EXE=$HOME/bin/fdtd64_2003

cd $WORKDIR

$EXE qedc3_2_05.in > qedc3_2_05.out
