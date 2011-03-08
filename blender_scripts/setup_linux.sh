#!/bin/bash
set -ux

for f in *.py;
do
  echo "Processing $f file...";
  ln -s $(readlink -f "$f") $HOME/.blender/scripts/
done
