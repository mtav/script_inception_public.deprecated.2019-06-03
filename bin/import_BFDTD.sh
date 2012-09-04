#!/bin/bash
blender -P $(dirname $0)/../blender_scripts/bfdtd_import.py -- "$@"
#blender -P $BLENDER_USER_SCRIPTS/bfdtd_import.py -- "$@"
