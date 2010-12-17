#!/bin/bash
set -eu

usage()
{
        echo "usage :"
        echo "`basename $0` 0 file1.out file2.out ..."
        echo "`basename $0` 1 DEST  file1.out file2.out ..."
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
	shift
	for f in "$@"
	do
		echo "$f"
		DIR=$(dirname $(readlink -f $f))
		BASE=$(basename $DIR)
		LINKNAME=$DST/$BASE
		if ! [ -e $LINKNAME ]
		then
			if grep Deallocating  $f
			then
				echo "ln -s $DIR $LINKNAME"
				ln -s $DIR $LINKNAME
			fi
		fi
	done
else
	usage;
fi
