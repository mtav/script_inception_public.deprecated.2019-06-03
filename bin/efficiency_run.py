#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from geometries.pillar_1D_wrapper import *
import re
from bfdtd.bfdtd_parser import *

def efficiency_run(src, dst):
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
    
  FDTDobj.geometry_object_list[:] = []
  FDTDobj.writeAll(dst,fileBaseName)

def main(argv=None):
  # main function
  src = sys.argv[1]
  dst = sys.argv[2]
  efficiency_run(src, dst)

if __name__ == "__main__":
  sys.exit(main())
