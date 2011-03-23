#!/bin/bash
set -ux

for f in *.py;
do
  echo "Processing $f file...";
  ln -s $(readlink -f "$f") $HOME/.blender/scripts/
  ln -s $(readlink -f "$f") $HOME/bin/blender-2.56a-beta-linux-glibc27-x86_64/2.56/scripts
done
