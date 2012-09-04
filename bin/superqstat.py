#!/usr/bin/env python3

import sys
import re

# TODO: Finish this

if __name__ == "__main__":
  '''
  qstat wrapper
  '''

pattern = r""
Job Id: (.*)
    Job_Name = (.*)
    Job_Owner = (.*)
    job_state = (.*)
    queue = (.*)
    server = (.*)
    Checkpoint = (.*)
    ctime = (.*)
    Error_Path = (.*)
	/qsub.chr.9.22.e1600362
    Hold_Types = (.*)
    Join_Path = (.*)
    Keep_Files = (.*)
    Mail_Points = (.*)
    mtime = (.*)
    Output_Path = (.*)
	s/qsub.chr.9.22.o1600362
    Priority = (.*)
    qtime = (.*)
    Rerunable = (.*)
    Resource_List.nodect = (.*)
    Resource_List.nodes = (.*)
    Resource_List.walltime = (.*)
    etime = (.*)
    submit_args = (.*)

  QFILE=sys.argv[1]
  with open(QFILE, 'r') as f:
    for line in f:
      if len(line.strip())>0:
        tab = line.strip().split('\t')
