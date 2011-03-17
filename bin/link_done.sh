#!/bin/bash
set -eu

usage()
{
  echo "usage :"
  echo "`basename $0` 0 file1.out file2.out ... (just list finished ones)"
  echo "`basename $0` 1 file1.out file2.out ... (list unfinished running ones)"
  echo "`basename $0` 2 file1.out file2.out ... (list all unfinished ones)"
  echo "`basename $0` 3 DEST  file1.out file2.out ... (create links to finished ones in DEST)"
  echo "creates links to the dirs containing *.out in DEST if *.out contains \"Deallocating\", i.e. if the simulations in those dirs are finished"
  echo "`basename $0` 4 file1.sh file2.sh ... (submit unfinished ones)"
  exit 0
}

if [ $# -lt 2 ]
then
  usage;
fi

operation_type=$1
shift

function list_finished()
{
  echo "==>list_finished called"
  for f in "$@"
  do
    DIR=$(dirname $(readlink -f $f))
    BASE=$(basename $DIR)
    if grep Deallocating  $f 1>/dev/null 2>&1
    then
      echo "$f"
    fi
  done
}

function list_unfinished_running()
{
  echo "==>list_unfinished_running called"
  for f in "$@"
  do
    DIR=$(dirname $(readlink -f $f))
    BASE=$(basename $DIR)
    if ! grep Deallocating  $f 1>/dev/null 2>&1
    then
      echo "$f"
    fi
  done
}

function list_all_unfinished()
{
  echo "==>list_all_unfinished called"
  for f in "$@"
  do
    DIR=$(dirname $(readlink -f "$f"))
    BASE=$(basename $f '.out')
    OUTFILE="$DIR/$BASE.out"
    if [ -s  "$OUTFILE" ]
    then
      #~ echo "$OUTFILE exists"
      if ! grep Deallocating  "$OUTFILE" 1>/dev/null 2>&1
      then
        #~ echo "$OUTFILE exists but is unfinished"
        echo "$OUTFILE"
      fi
    else
      #~ echo "$OUTFILE does not exist"
      echo "$OUTFILE"
    fi
  done
}

function link_finished()
{
  echo "==>link_finished called"
  DST=$(readlink -f $1)
  if ! [ -d $DST ]
  then
    echo "Error: $DST does not exist or is not a directory"
    exit -1
  fi
  shift
  for f in "$@"
  do
    echo "Processing $f"
    DIR=$(dirname $(readlink -f $f))
    BASE=$(basename $DIR)
    LINKNAME=$DST/$BASE
    if ! [ -e $LINKNAME ]
    then
      if grep Deallocating  $f
      then
        echo "ln -s $DIR $LINKNAME"
        ln -s $DIR $LINKNAME
      else
        echo "Deallocating not found in $f"
      fi
    else
      echo "Warning: $LINKNAME already exists"
    fi
  done
}

function qsub_unfinished()
{
  echo "==>qsub_unfinished called"
  for f in "$@"
  do
    DIR=$(dirname $(readlink -f "$f"))
    BASE=$(basename $f '_4ppn.sh')
    BASE=$(basename $BASE '_8ppn.sh')
    OUTFILE="$DIR/$BASE.out"
    if [ -s  "$OUTFILE" ]
    then
      #~ echo "$OUTFILE exists"
      if ! grep Deallocating  "$OUTFILE" 1>/dev/null 2>&1
      then
        #~ echo "$OUTFILE exists but is unfinished"
        superqsub.sh "$f"
      fi
    else
      #~ echo "$OUTFILE does not exist"
      superqsub.sh "$f"
    fi
  done
}

if [ $operation_type = "0" ]
then
  list_finished "$@";
elif [ $operation_type = "1" ]
then
  list_unfinished_running "$@";
elif [ $operation_type = "2" ]
then
  list_all_unfinished "$@";
elif [ $operation_type = "3" ]
then
  link_finished "$@";
elif [ $operation_type = "4" ]
then
  qsub_unfinished "$@";
else
  usage;
fi
