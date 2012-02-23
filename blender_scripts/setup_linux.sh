#!/bin/bash
set -ux

safe_link_dir()
{
  if [[ ! $1 ]];then exit 2; fi
  if [[ ! $2 ]];then exit 2; fi

  TARGET="$1"
  DEST="$2"
  FILE="$DEST/$(basename $TARGET)"

  if [ ! -e $TARGET ]
  then
    echo "ERROR: Target $TARGET not found."
    exit 1
  fi

  # check if target already exists and remove eventually
  if [ -L "$FILE" ] # FILE exists and is a symbolic link (same as -h)
  then
      echo "WARNING: Removing symbolic link $FILE"
      ls -l "$FILE"
      rm -v "$FILE"
  else
    if [ -e $FILE ]
    then
      echo "WARNING: $FILE already exists and is not a symbolic link."
      ls -l "$FILE"
      cp -iv "$FILE" "$FILE.$(date +%Y%m%d_%H%M%S)"
      rm -iv "$FILE"
    fi
  fi

  # link if the file does not exist
  if [ ! -e $FILE ]
  then
    echo "Linking $TARGET"
    ln -s "$TARGET" "$FILE"
  fi
}

for f in *.py;
do
  echo "Processing $f file...";
  #ln -s $(readlink -f "$f") $HOME/.blender/scripts/
  safe_link_dir $(readlink -f "$f") $HOME/.blender/scripts/
#  ln -s $(readlink -f "$f") $HOME/bin/blender-2.56a-beta-linux-glibc27-x86_64/2.56/scripts
done
