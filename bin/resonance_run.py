#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bin.bfdtd_tool import *

def main(argv=None):
  '''
  Copy src to dst with added frequency snapshots from freqListFile
  '''
  src = sys.argv[1]
  dst = sys.argv[2]
  freqListFile = sys.argv[3]
  resonance_run(src, dst, freqListFile)

if __name__ == "__main__":
  sys.exit(main())
