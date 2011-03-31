#!/bin/bash
set -eux
qstat | grep $USER | awk -F. '{print $1}' | xargs -n1 qdel
