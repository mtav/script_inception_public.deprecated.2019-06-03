#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bfdtd.bfdtd_parser import *
from constants.constants import *

def rerun_with_new_excitation(src, dst, excitation_wavelength_nm, excitation_time_constant):
  ''' Copy src to dst, only changing excitation_wavelength_nm and excitation_time_constant'''
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
    
  FDTDobj.excitation_list[0].time_constant = excitation_time_constant
  FDTDobj.excitation_list[0].frequency = get_c0()/(1e-3*excitation_wavelength_nm)
    
  FDTDobj.writeAll(dst,fileBaseName)
  GEOshellscript(dst+os.sep+fileBaseName+'.sh', fileBaseName,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

# example run:
# rerun_with_new_excitation.py qedc3_2_05.in /tmp/new 637 42
def main(argv=None):
  # main function
  src = sys.argv[1]
  dst = sys.argv[2]
  excitation_wavelength_nm = float(sys.argv[3])
  excitation_time_constant = float(sys.argv[4])
  rerun_with_new_excitation(src, dst, excitation_wavelength_nm, excitation_time_constant)

if __name__ == "__main__":
  sys.exit(main())
