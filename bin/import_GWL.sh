#!/bin/bash
blender -P $(dirname $0)/../blender_scripts/GWL_import.py -- "$@"
#blender -P $BLENDER_USER_SCRIPTS/GWL_import.py -- "$@"
