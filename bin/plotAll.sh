#!/bin/bash
set -eux
DIR=$(readlink -f $1)
matlab_batcher.sh plotAll "'$DIR',1,{'p05id.prn','p005id.prn'},{'foo'}"
