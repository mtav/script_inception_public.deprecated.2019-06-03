#!/bin/bash
set -ux

# BLENDERPATH=$HOME/bin/blender-2.56a-beta-linux-glibc27-x86_64/2.56
#BLENDERPATH=$HOME/bin/blender-2.58a-linux-glibc27-x86_64/2.58
#BLENDERPATH=$HOME/bin/blender-2.62-linux-glibc27-i686/2.62
BLENDERPATH=$HOME/.blender/2.58

SCRIPTSDIR=$HOME/.blender/scripts/

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
  #ln -s $(readlink -f "$f") $BLENDERPATH/scripts
  #ln -s $(readlink -f "$f") $HOME/.blender/scripts/
  if [ -d $SCRIPTSDIR ]
  then
    safe_link_dir $(readlink -f "$f") $SCRIPTSDIR
  else
    echo "ERROR: $SCRIPTSDIR does not exist."
  fi
  #ln -s $(readlink -f "$f") $HOME/bin/blender-2.56a-beta-linux-glibc27-x86_64/2.56/scripts
done

safe_link_dir $(readlink -f "io_mesh_BristolFDTD") "$BLENDERPATH/scripts/addons/"
safe_link_dir $(readlink -f "io_mesh_BristolFDTD/io_import_scene_bfdtd.py") "$BLENDERPATH/scripts/addons/"
