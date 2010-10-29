#!/bin/bash
set -eux
# alias coming soon. I want dropbox sync first. :)
qstat | grep $USER | awk '{print $1}' | xargs qdel

