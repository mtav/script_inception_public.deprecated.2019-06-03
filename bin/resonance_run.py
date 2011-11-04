#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from geometries.pillar_1D_wrapper import *
import re
from bin.harminv import getFrequencies
from bfdtd.bfdtd_parser import *

def resonance_run(src, dst, freqListFile):
  ''' Copy src to dst with added frequency snapshots from freqListFile '''
  src = os.path.abspath(src).rstrip(os.sep)
  dst = os.path.abspath(dst).rstrip(os.sep)
  if os.path.isdir(src):
    print src +' is a directory'
    FDTDobj = readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print src +' is not a directory'
    FDTDobj = readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
  
  freq_snapshots = getFrequencies(freqListFile)
  for obj in FDTDobj.frequency_snapshot_list:
    obj.frequency_vector = freq_snapshots
  
  FDTDobj.writeAll(dst,fileBaseName)

def main(argv=None):
  # main function
  src = sys.argv[1]
  dst = sys.argv[2]
  freqListFile = sys.argv[3]
  resonance_run(src, dst, freqListFile)

if __name__ == "__main__":
  sys.exit(main())
