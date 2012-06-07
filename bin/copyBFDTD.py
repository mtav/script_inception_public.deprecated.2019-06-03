#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from geometries.pillar_1D_wrapper import *
import re
from bfdtd.bfdtd_parser import *

def copyBFDTD(src,dst):
  ''' Copy src to dst '''
  src = src.rstrip(os.sep)
  dst = dst.rstrip(os.sep)
  if os.path.isdir(src):
    print src +' is a directory'
    FDTDobj = readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print src +' is not a directory'
    FDTDobj = readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
  
  FDTDobj.writeAll(dst,fileBaseName)
  GEOshellscript(dst+os.sep+fileBaseName+'.sh', fileBaseName,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

def main(argv=None):
  # main function
  src = sys.argv[1]
  dst = sys.argv[2]
  copyBFDTD(src, dst)

if __name__ == "__main__":
  sys.exit(main())
