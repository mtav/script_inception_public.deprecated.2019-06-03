#!/bin/bash
# remove .o and .obj files (practical if make clean/distclean is not available)

find . -type f \( -name "*.prn" -o -name "*.out" -o -name "ea.txt" -o -name "e_id_.txt" -o -name "geom.geo" -o -name "namiki.txt" -o -name "*.int" -o -name "time.txt" \) | less

echo "Remove those object files? (y=directly, i=interactively, *=exit)"
read ans
case $ans in
  y|Y|yes) find . -type f \( -name "*.prn" -o -name "*.out" -o -name "ea.txt" -o -name "e_id_.txt" -o -name "geom.geo" -o -name "namiki.txt" -o -name "*.int" -o -name "time.txt" \) -exec rm -v {} \; ;;
  i|I)     find . -type f \( -name "*.prn" -o -name "*.out" -o -name "ea.txt" -o -name "e_id_.txt" -o -name "geom.geo" -o -name "namiki.txt" -o -name "*.int" -o -name "time.txt" \) -exec rm -iv {} \; ;;
  *)       exit 1;;
esac
