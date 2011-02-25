#!/bin/bash
set -eux
# alias coming soon. I want dropbox sync first. :)
qstat | grep $USER | awk -F. '{print $1}' | xargs qdel

