#!/bin/bash
set -eu

## To use this script, add the QSUBMAIL variable to your environment. You can add one of the following lines to your ~/.bashrc for example:
## single mail address:
#    export QSUBMAIL="foo.bar@bristol.ac.uk"
## multiple mail addresses:
#    export QSUBMAIL="foo.bar@bristol.ac.uk,big.boss@bristol.ac.uk"

# Check if all parameters are present
# If no, exit

source script_inception_common_functions.sh

# echo "NARGS = $#"

if [ $# -lt 1 ]
then
  echo "$(basename $0) SCRIPT1 SCRIPT2 ..."
  echo 'submits scripts using the following command:'
  echo 'qsub -M $QSUBMAIL -v JOBDIR="$(readlink -f $(dirname "$SCRIPT"))" $SCRIPT'
  echo "NOTE: \",\" in paths lead to problems when using torque/qsub with -v because -v expects a comma separated list!!!"
fi
#exit

#SCRIPT=$1

for SCRIPT in "$@"
do
  OUTFILE=$(getOutFile "$SCRIPT")
  
  set +e
  getDataState "$SCRIPT"
  status=$?
  set -e
  
  if  [ $status == 2 ]
  then
    echo "submitting $SCRIPT"
    qsub -l nodes=1:ppn=$PPN -M $QSUBMAIL -v JOBDIR="$(readlink -f "$(dirname "$SCRIPT")")" "$SCRIPT"
  else
    if  [ $status == 0 ]
    then
      echo "script already done. -> skipping (remove .out file to run it anyway)"
    else
      echo "script seems to be already running. -> skipping (remove .out file to run it anyway)"
    fi
  fi
done
