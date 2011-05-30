#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
#~ import utilities.getuserdir
from utilities.getuserdir import *
#from bfdtd.bfdtd_parser import *
from utilities.common import fixLowerUpper

def planeNumberName(var):
  S=['X','Y','Z']
  if var in [1,2,3]:
    return var, S[var-1]
  elif var.upper() in S:
    return S.index(var.upper())+1,var.upper()
  else:
    print('unknown plane: '+str(var))
    sys.exit(-1)
  #~ elif var == 'x' or var == 'X':
    #~ return 1
  #~ elif var == 'y' or var == 'Y':
    #~ return 2
  #~ elif var == 'z' or var == 'Z':
    #~ return 3
  #~ else:
    #~ print('unknown plane: '+str(x))
    #~ sys.exit(-1)
#~ 
#~ def planeName(var):
  #~ if var.lower() in ['x','y','z']:
    #~ return var.lower()
  #~ elif var == 1:
    #~ return 'x'
  #~ elif var == 2:
    #~ return 'y'
  #~ elif var == 3:
    #~ return 'z'
  #~ else:
    #~ print('unknown plane: '+str(x))
    #~ sys.exit(-1)

########################
# GENERATOR FUNCTIONS
########################
# mandatory objects

# geometry objects
def GEOsphere(FILE, COMMENT, center, outer_radius, inner_radius, permittivity, conductivity):
  ''' sphere
  {
   1-5 Coordinates of the sphere ( xc yc zc r1 r2 )
   6 permittivity
   7 conductivity
  } '''
  FILE.write('SPHERE  **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%E **XC\n" % center[0])
  FILE.write("%E **YC\n" % center[1])
  FILE.write("%E **ZC\n" % center[2])
  FILE.write("%E **outer_radius\n" % outer_radius)
  FILE.write("%E **inner_radius\n" % inner_radius)
  FILE.write("%E **permittivity\n" % permittivity)
  FILE.write("%E **conductivity\n" % conductivity)
  FILE.write('}\n')

  FILE.write('\n')

def GEOcylinder(FILE, COMMENT, centre, inner_radius, outer_radius, H, permittivity, conductivity, angle_deg):
  ''' # cylinder
  # {
  # 1-7 Coordinates of the material volume ( xc yc zc r1 r2 h )
  # 7 permittivity
  # 8 conductivity
  # 9 angle_deg of inclination
  # }
  # xc, yc and zc are the coordinates of the centre of the cylinder. r1 and r2 are the inner and outer
  # radius respectively, h is the cylinder height, is the angle_deg of inclination. The cylinder is aligned
  # with the y direction if =0 and with the x direction if =90
  #
  # i.e. angle_deg = Angle of rotation in degrees around -Z=(0,0,-1) '''

  FILE.write('CYLINDER **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%E **X CENTRE\n" % centre[0])
  FILE.write("%E **Y CENTRE\n" % centre[1])
  FILE.write("%E **Z CENTRE\n" % centre[2])
  FILE.write("%E **inner_radius\n" % inner_radius)
  FILE.write("%E **outer_radius\n" % outer_radius)
  FILE.write("%E **HEIGHT\n" % H)
  FILE.write("%E **Permittivity\n" % permittivity)
  FILE.write("%E **Conductivity\n" % conductivity)
  FILE.write("%E **Angle of rotation in degrees around -Z=(0,0,-1)\n" % angle_deg)
  FILE.write('}\n')

  FILE.write('\n')


def GEOrotation(FILE, COMMENT, axis_point, axis_direction, angle_degrees):
  # rotation structure. Actually affects previous geometry object in Prof. Railton's modified BrisFDTD. Not fully implemented yet.
  # Should be integrated into existing structures using a directional vector anyway, like in MEEP. BrisFDTD hacking required... :)

  FILE.write('ROTATION **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%E **X axis_point\n" % axis_point[0])
  FILE.write("%E **Y axis_point\n" % axis_point[1])
  FILE.write("%E **Z axis_point\n" % axis_point[2])
  FILE.write("%E **X axis_direction\n" % axis_direction[0])
  FILE.write("%E **Y axis_direction\n" % axis_direction[1])
  FILE.write("%E **Z axis_direction\n" % axis_direction[2])
  FILE.write("%E **angle_degrees\n" % angle_degrees)
  FILE.write('}\n')

  FILE.write('\n')

# measurement objects

def GEOfrequency_snapshot(FILE, COMMENT, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency, starting_sample, E, H, J):
  P1, P2 = fixLowerUpper(P1, P2)

  def snapshot(plane,P1,P2, frequency):
    plane_ID, plane_name = planeNumberName(plane)
    #~ if plane == 1:
      #~ plane_name='X'
    #~ elif plane == 2:
      #~ plane_name='Y'
    #~ else: #plane == 3
      #~ plane_name='Z'
    FILE.write('FREQUENCY_SNAPSHOT **name='+COMMENT+'\n')
    FILE.write('{\n')

    FILE.write("%d **FIRST\n" % first)
    FILE.write("%d **REPETITION\n" % repetition)
    FILE.write("%d **interpolate?\n" % interpolate)
    FILE.write("%d **REAL DFT\n" % real_dft)
    FILE.write("%d **MOD ONLY\n" % mod_only)
    FILE.write("%d **MOD ALL\n" % mod_all)
    FILE.write("%d **PLANE %s\n" % (plane_ID, plane_name))
    FILE.write("%E **X1\n" % P1[0])
    FILE.write("%E **Y1\n" % P1[1])
    FILE.write("%E **Z1\n" % P1[2])
    FILE.write("%E **X2\n" % P2[0])
    FILE.write("%E **Y2\n" % P2[1])
    FILE.write("%E **Z2\n" % P2[2])
    FILE.write("%E **FREQUENCY (HZ)\n" % frequency)
    FILE.write("%d **STARTING SAMPLE\n" % starting_sample)
    FILE.write("%d **EX\n" % E[0])
    FILE.write("%d **EY\n" % E[1])
    FILE.write("%d **EZ\n" % E[2])
    FILE.write("%d **HX\n" % H[0])
    FILE.write("%d **HY\n" % H[1])
    FILE.write("%d **HZ\n" % H[2])
    FILE.write("%d **JX\n" % J[0])
    FILE.write("%d **JY\n" % J[1])
    FILE.write("%d **JZ\n" % J[2])
    FILE.write('}\n')

    FILE.write('\n')


  plane_ID, plane_name = planeNumberName(plane)
  for i in range(len(frequency)):
    if P1[plane_ID-1] == P2[plane_ID-1]:
      snapshot(plane_ID,P1,P2,frequency[i])
    else:
      snapshot(1,[P1[0],P1[1],P1[2]],[P1[0],P2[1],P2[2]],frequency[i])
      snapshot(1,[P2[0],P1[1],P1[2]],[P2[0],P2[1],P2[2]],frequency[i])
      snapshot(2,[P1[0],P1[1],P1[2]],[P2[0],P1[1],P2[2]],frequency[i])
      snapshot(2,[P1[0],P2[1],P1[2]],[P2[0],P2[1],P2[2]],frequency[i])
      snapshot(3,[P1[0],P1[1],P1[2]],[P2[0],P2[1],P1[2]],frequency[i])
      snapshot(3,[P1[0],P1[1],P2[2]],[P2[0],P2[1],P2[2]],frequency[i])

# files
def GEOcommand(filename, BASENAME):
  ''' CMD file generation '''

  #open file
  with open(filename, 'w') as FILE:

    #~ FILE = fopen(strcat(filename,'.cmd'),'wt')

    # Executable = 'D:\fdtd\source\latestfdtd02_03\subgrid\Fdtd32.exe'
    Executable = os.path.join(getuserdir(),'bin','fdtd.exe')

    #write file
    FILE.write("Executable = %s\n" % Executable)
    FILE.write("\n")
    FILE.write("input = %s.in\n" %  BASENAME)
    FILE.write("\n")
    FILE.write("output = fdtd.out\n")
    FILE.write("\n")
    FILE.write("error = error.log\n")
    FILE.write("\n")
    FILE.write("Universe = vanilla\n")
    FILE.write("\n")
    FILE.write("transfer_files = ALWAYS\n")
    FILE.write("\n")
    FILE.write("transfer_input_files = entity.lst, %s.geo, %s.inp\n" %  (BASENAME, BASENAME))
    FILE.write("\n")
    FILE.write("Log = foo.log\n")
    FILE.write("\n")
    FILE.write("Rank = Memory >= 1000\n")
    FILE.write("\n")
    FILE.write("LongRunJob = TRUE\n")
    FILE.write("\n")
    FILE.write("###Requirements = (LongRunMachine =?= TRUE)\n")
    FILE.write("\n")
    FILE.write("queue\n")

    #close file
    FILE.close()

def GEOin(filename, file_list):
  ''' IN file generation '''

  #open file
  with open(filename, 'w') as FILE:
    #write file
    for obj in file_list:
      FILE.write("%s\n" %  obj)
  
    #close file
    FILE.close()

# TODO: simplify it + merge with GEOshellscript_advanced by adding options
def GEOshellscript(filename, BASENAME, EXE = 'fdtd', WORKDIR = '$JOBDIR', WALLTIME = 12):

  #open file
  with open(filename, 'w') as FILE:
    #write file
    FILE.write("#!/bin/bash\n")
    FILE.write("#\n")
    FILE.write("#PBS -l walltime=%d:00:00\n" % WALLTIME)
    FILE.write("#PBS -mabe\n")
    FILE.write("#PBS -joe\n")
    FILE.write("#\n")
    FILE.write("\n")
    FILE.write("\n")
    FILE.write("export WORKDIR=%s\n" % WORKDIR)
    FILE.write("export EXE=%s\n" % EXE)
    FILE.write("\n")
    FILE.write("cd $WORKDIR\n")
    FILE.write("\n")
    FILE.write("$EXE %s.in > %s.out\n" %  (BASENAME, BASENAME))
    FILE.write("fix_filenames.py -v .\n")
  
    #close file
    FILE.close()

# TODO: maybe create a submission function in python...
def GEOshellscript_advanced(filename, BASENAME, probe_col, EXE = 'fdtd', WORKDIR = '$JOBDIR', WALLTIME = 12):

  #open file
  with open(filename, 'w') as FILE:
    #write file
    FILE.write("#!/bin/bash\n")
    FILE.write("#\n")
    FILE.write("#PBS -l walltime=%d:00:00\n" % WALLTIME)
    FILE.write("#PBS -mabe\n")
    FILE.write("#PBS -joe\n")
    FILE.write("#\n")
    FILE.write("\n")
    FILE.write("set -eux\n")
    FILE.write("\n")
    FILE.write('if [ -n "${JOBDIR+x}" ]; then\n')
    FILE.write('  echo JOBDIR is set\n')
    FILE.write('else\n')
    FILE.write('  echo JOBDIR is not set\n')
    FILE.write('  JOBDIR="$(readlink -f $(dirname "$0"))"\n')
    FILE.write('fi\n')
    FILE.write("\n")
    FILE.write("export WORKDIR=%s\n" % WORKDIR)
    FILE.write("export EXE=%s\n" % EXE)
    FILE.write("\n")
    FILE.write("cd $WORKDIR\n")
    FILE.write("\n")
    FILE.write("$EXE %s.in > %s.out\n" %  (BASENAME, BASENAME))
    FILE.write("fix_filenames.py -v .\n")
    FILE.write("matlab_batcher.sh getResonanceFrequencies2 \"'$WORKDIR/p005id.prn',%d,'$WORKDIR/freq_list.txt'\"\n" % probe_col)
    FILE.write("rerun.py $WORKDIR/freq_list.txt\n")
    FILE.write("cd resonance/%s && $EXE %s.in >> %s.out\n" %  (BASENAME, BASENAME, BASENAME))
    FILE.write("fix_filenames.py -v .\n")
    FILE.write("plotAll.sh .\n")
  
    #close file
    FILE.close()

########################
# MAIN
########################
class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
      argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
      raise Usage(msg)
    # more code, unchanged
    with open('tmp.txt', 'w') as FILE:
      delta_X_vector = [11.25,21.25,31.25]
      delta_Y_vector = [12.25,22.25,32.25]
      delta_Z_vector = [13.25,23.25,33.25]
      COMMENT = 'example comment'
      GEOmesh(FILE, COMMENT, delta_X_vector, delta_Y_vector, delta_Z_vector)
      GEOflag(FILE, COMMENT, 70, 12.34, 24, 42, 1000, 0.755025, '_id_')
      GEOboundary(FILE, COMMENT, 1.2, [3.4,3.4,3.4],\
                                  5.6, [7.8,7.8,6.2],\
                                  9.10, [11.12,1,2],\
                                  13.14, [15.16,3,4],\
                                  17.18, [19.20,5,6],\
                                  21.22, [23.24,7.8,5.4])
      GEObox(FILE, COMMENT, [1.2,3.4,5.6], [9.8,7.6,5.4])
      GEOsphere(FILE, COMMENT, [1,2,3], 9, 8, 7, 6)
      GEOblock(FILE, COMMENT, [1.1,2.2,3.3], [4.4,5.5,6.6], 600, 700)
      GEOcylinder(FILE, COMMENT, [1.2,3.4,5.6], 77, 88, 99, 100, 0.02, 47.42)
      GEOrotation(FILE, COMMENT, [1,2,3], [4,5,6], 56)
      #excitation_obj = Excitation(COMMENT, 77, [1,2,3], [4,5,6], [7,8,9], [77,88,99], 69, 12.36, 45.54, 78.87, 456, 1, 22, 333, 4444)
      #excitation_obj.write_entry(FILE)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'x', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'y', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'z', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'x', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'y', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'z', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOfrequency_snapshot(FILE, COMMENT, 369, 852, 147, 258, 369, 987, 'x', [1,2,3], [1,2,3], [852,741,963], 147, [7,8,9],[4,5,6],[1,2,3])
      GEOprobe(FILE, COMMENT, [1,2,3], 56, [5,6,7], [5,6,7], [5,6,7], 4564654 )
      GEOcommand('tmp.bat', 'BASENAME')
      GEOin('tmp.in', ['file','list'])
      GEOshellscript('tmp.sh', 'BASENAME', '/usr/bin/superexe', '/work/todo', 999)
      
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
