#!/bin/bash

set -eux

trimit()
{
  OLD=$1
  NEW=$(dirname $OLD)/$(basename $OLD .eps).png
  gs -r300 -dEPSCrop -dTextAlphaBits=4 -sDEVICE=png16m -sOutputFile=$NEW -dBATCH -dNOPAUSE $OLD
  convert $NEW -trim $NEW
}

#trimit $1
#find . -name "*.eps" | xargs -n1 -I{} trimit() {}

find . -name "*.eps"  | while read FILENAME;
do
  trimit $FILENAME
done

# convert image1.png \( image2.png  image3.png -append \) -gravity center +append out.png
#ls -d */resonance/*/ | xargs -n1 -I{} ~/Development/script_inception_public/special_ops/SO_delimages.py {}
