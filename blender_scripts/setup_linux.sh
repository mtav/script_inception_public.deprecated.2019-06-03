#!/bin/bash
set -ux

# BLENDERPATH=$HOME/bin/blender-2.56a-beta-linux-glibc27-x86_64/2.56
#BLENDERPATH=$HOME/bin/blender-2.58a-linux-glibc27-x86_64/2.58
BLENDERPATH=$HOME/bin/blender-2.62-linux-glibc27-i686/2.62

for f in *.py;
do
  echo "Processing $f file...";
  ln -s $(readlink -f "$f") $HOME/.blender/scripts/
#  ln -s $(readlink -f "$f") $BLENDERPATH/scripts
done

ln -s $(readlink -f "io_mesh_BristolFDTD") $BLENDERPATH/scripts/addons/
