#!/bin/bash
set -eux
DIR=$(readlink -f $1)
matlab_batcher.sh plotAll "'$DIR',1,{'p05id.prn','p005id.prn'},{'foo'}"
#find . -name "*.png" | xargs -n1 -I{} convert {} -trim {}new
trim.sh .
find . -name "*.eps" | xargs rm -v
