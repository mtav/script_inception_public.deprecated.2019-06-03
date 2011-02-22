#!/bin/bash
set -eux

## To use this script, add the QSUBMAIL variable to your environment. You can add one of the following lines to your ~/.bashrc for example:
## single mail address:
#    export QSUBMAIL="foo.bar@bristol.ac.uk"
## multiple mail addresses:
#    export QSUBMAIL="foo.bar@bristol.ac.uk,big.boss@bristol.ac.uk"

# Check if all parameters are present
# If no, exit

echo $#

if [ $# -lt 1 ]
then
	echo "$(basename $0) SCRIPT1 SCRIPT2 ..."
        echo 'submits scripts using the following command:'
	echo 'qsub -M $QSUBMAIL -v JOBDIR="$(readlink -f $(dirname "$SCRIPT"))" $SCRIPT'
fi
#exit

#SCRIPT=$1

for SCRIPT in "$@"
do
	echo "submitting $SCRIPT"
	qsub -M $QSUBMAIL -v JOBDIR="$(readlink -f $(dirname "$SCRIPT"))" $SCRIPT
done
