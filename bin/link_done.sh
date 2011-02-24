#!/bin/bash
set -eu

usage()
{
        echo "usage :"
        echo "`basename $0` 0 file1.out file2.out ... (just list finished ones)"
        echo "`basename $0` 1 DEST  file1.out file2.out ... (create links to finished ones in DEST)"
        echo "`basename $0` 2 file1.out file2.out ... (list unfinished ones)"
	echo "creates links to the dirs containing *.out in DEST if *.out contains \"Deallocating\", i.e. if the simulations in those dirs are finished"
        exit 0
}

if [ $# -lt 2 ]
then
	usage;
fi

justlink=$1
shift

if [ $justlink = "0" ]
then
	for f in "$@"
	do
		DIR=$(dirname $(readlink -f $f))
		BASE=$(basename $DIR)
		if grep Deallocating  $f 1>/dev/null 2>&1
		then
			echo "$f"
		fi
	done
elif [ $justlink = "1" ]
then
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
elif [ $justlink = "2" ]
then
	for f in "$@"
	do
		DIR=$(dirname $(readlink -f $f))
		BASE=$(basename $DIR)
		if ! grep Deallocating  $f 1>/dev/null 2>&1
		then
			echo "$f"
		fi
	done
else
	usage;
fi
