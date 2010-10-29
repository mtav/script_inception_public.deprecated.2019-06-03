#!/bin/bash
set -eux
SCRIPT=$1

## To use this script, add the QSUBMAIL variable to your environment. You can add one of the following lines to your ~/.bashrc for example:
## single mail address:
#    export QSUBMAIL="foo.bar@bristol.ac.uk"
## multiple mail addresses:
#    export QSUBMAIL="foo.bar@bristol.ac.uk,big.boss@bristol.ac.uk"

qsub -M $QSUBMAIL -v JOBDIR=$(readlink -f $(dirname $SCRIPT)) $SCRIPT
