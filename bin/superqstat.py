#!/usr/bin/env python

import sys

if __name__ == "__main__":
  '''
  qstat wrapper
  '''
  QFILE=sys.argv[1]
  with open(QFILE, 'r') as f:
    for line in f:
      if len(line.strip())>0:
        tab = line.strip().split('\t')
