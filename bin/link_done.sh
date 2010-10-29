#!/bin/bash
set -eu

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

