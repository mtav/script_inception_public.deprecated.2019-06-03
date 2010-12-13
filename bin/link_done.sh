#!/bin/bash
set -eu

if [ $# -lt 2 ]
then
        echo "usage :"
        echo "`basename $0` DEST  file1.out file2.out ..."
	echo "creates links to the dirs containing *.out in DEST if *.out contains \"Deallocating\", i.e. if the simulations in those dirs are finished"
        exit 0
fi

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

