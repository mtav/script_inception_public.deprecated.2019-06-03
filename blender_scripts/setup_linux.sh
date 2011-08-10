#!/bin/bash
set -ux

# BLENDERPATH=$HOME/bin/blender-2.56a-beta-linux-glibc27-x86_64/2.56
BLENDERPATH=$HOME/bin/blender-2.58a-linux-glibc27-x86_64/2.58

for f in *.py;
do
  echo "Processing $f file...";
  ln -s $(readlink -f "$f") $HOME/.blender/scripts/
#  ln -s $(readlink -f "$f") $BLENDERPATH/scripts
done

ln -s io_mesh_bristolFDTD $BLENDERPATH/scripts/addons/
