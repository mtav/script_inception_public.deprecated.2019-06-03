#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
#~ import utilities.getuserdir
from utilities.getuserdir import *

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
def GEOmesh(FILE, COMMENT, delta_X_vector, delta_Y_vector, delta_Z_vector):
  ''' writes mesh to FILE '''
  # mesh X
  FILE.write('XMESH **name='+COMMENT+'\n')

  FILE.write('{\n')

  for i in range(len(delta_X_vector)):
    FILE.write("%E\n" % delta_X_vector[i])
  FILE.write('}\n')

  FILE.write('\n')


  # mesh Y
  FILE.write('YMESH **name='+COMMENT+'\n')

  FILE.write('{\n')

  for i in range(len(delta_Y_vector)):
    FILE.write("%E\n" % delta_Y_vector[i])
  FILE.write('}\n')

  FILE.write('\n')


  # mesh Z
  FILE.write('ZMESH **name='+COMMENT+'\n')

  FILE.write('{\n')

  for i in range(len(delta_Z_vector)):
    FILE.write("%E\n" % delta_Z_vector[i])
  FILE.write('}\n')

  FILE.write('\n')

def GEOflag(FILE, COMMENT, iteration_method, propagation_constant, flag_1, flag_2, iterations, timestep, id_character):
  FILE.write('FLAG  **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%d **ITERATION METHOD\n" % iteration_method)
  FILE.write("%E **PROPAGATION CONSTANT (IGNORED IN 3D MODEL)\n" % propagation_constant)
  FILE.write("%d **FLAG ONE\n" % flag_1)
  FILE.write("%d **FLAG TWO\n" % flag_2)
  FILE.write("%d **ITERATIONS\n" % iterations)
  FILE.write("%E **TIMESTEP as a proportion of the maximum allowed\n" % timestep)
  FILE.write("\"%s\" **ID CHARACTER (ALWAYS USE QUOTES)\n" % id_character)
  FILE.write('}\n')

  FILE.write('\n')

def GEOboundary(FILE, COMMENT, Xpos_bc, Xpos_param,\
                            Ypos_bc, Ypos_param,\
                            Zpos_bc, Zpos_param,\
                            Xneg_bc, Xneg_param,\
                            Yneg_bc, Yneg_param,\
                            Zneg_bc, Zneg_param):
  FILE.write('BOUNDARY  **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%d %d %d %d **X+ \n" % (Xpos_bc, Xpos_param[0], Xpos_param[1], Xpos_param[2]))
  FILE.write("%d %d %d %d **Y+ \n" % (Ypos_bc, Ypos_param[0], Ypos_param[1], Ypos_param[2]))
  FILE.write("%d %d %d %d **Z+ \n" % (Zpos_bc, Zpos_param[0], Zpos_param[1], Zpos_param[2]))
  FILE.write("%d %d %d %d **X- \n" % (Xneg_bc, Xneg_param[0], Xneg_param[1], Xneg_param[2]))
  FILE.write("%d %d %d %d **Y- \n" % (Yneg_bc, Yneg_param[0], Yneg_param[1], Yneg_param[2]))
  FILE.write("%d %d %d %d **Z- \n" % (Zneg_bc, Zneg_param[0], Zneg_param[1], Zneg_param[2]))
  FILE.write('}\n')

  FILE.write('\n')

def GEObox(FILE, COMMENT, lower, upper):
  FILE.write('BOX  **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%E **XL\n" % lower[0])
  FILE.write("%E **YL\n" % lower[1])
  FILE.write("%E **ZL\n" % lower[2])
  FILE.write("%E **XU\n" % upper[0])
  FILE.write("%E **YU\n" % upper[1])
  FILE.write("%E **ZU\n" % upper[2])
  FILE.write('}\n')

  FILE.write('\n')

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

def GEOblock(FILE, COMMENT, lower, upper, permittivity, conductivity):
  FILE.write('BLOCK **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%E **XL\n" % lower[0])
  FILE.write("%E **YL\n" % lower[1])
  FILE.write("%E **ZL\n" % lower[2])
  FILE.write("%E **XU\n" % upper[0])
  FILE.write("%E **YU\n" % upper[1])
  FILE.write("%E **ZU\n" % upper[2])
  FILE.write("%E **relative Permittivity\n" % permittivity)
  FILE.write("%E **Conductivity\n" % conductivity)
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


# excitation objects
#def GEOexcitation(FILE, COMMENT, current_source, P1, P2, E, H, type, time_constant, amplitude, time_offset, frequency, param1, param2, param3, param4):
  #FILE.write('EXCITATION **name='+COMMENT+'\n')

  #FILE.write('{\n')

  #FILE.write("%d ** CURRENT SOURCE \n" % current_source)
  #FILE.write("%E **X1\n" % P1[0])
  #FILE.write("%E **Y1\n" % P1[1])
  #FILE.write("%E **Z1\n" % P1[2])
  #FILE.write("%E **X2\n" % P2[0])
  #FILE.write("%E **Y2\n" % P2[1])
  #FILE.write("%E **Z2\n" % P2[2])
  #FILE.write("%d **EX\n" % E[0])
  #FILE.write("%d **EY\n" % E[1])
  #FILE.write("%d **EZ\n" % E[2])
  #FILE.write("%d **HX\n" % H[0])
  #FILE.write("%d **HY\n" % H[1])
  #FILE.write("%d **HZ\n" % H[2])
  #FILE.write("%d **GAUSSIAN MODULATED SINUSOID\n" % type)
  #FILE.write("%E **TIME CONSTANT\n" % time_constant)
  #FILE.write("%E **AMPLITUDE\n" % amplitude)
  #FILE.write("%E **TIME OFFSET\n" % time_offset)
  #FILE.write("%E **FREQ (HZ)\n" % frequency)
  #FILE.write("%d **UNUSED PARAMETER\n" % param1)
  #FILE.write("%d **UNUSED PARAMETER\n" % param2)
  #FILE.write("%d **UNUSED PARAMETER\n" % param3)
  #FILE.write("%d **UNUSED PARAMETER\n" % param4)
  #FILE.write('}\n')

  #FILE.write('\n')

# measurement objects
def GEOtime_snapshot(FILE, COMMENT, first, repetition, plane, P1, P2, E, H, J, power, eps):
  ''' # def GEOtime_snapshot(FILE, first, repetition, plane, P1, P2, E, H, J, power, eps):
  #
  # format specification:
  # 1 iteration number for the first snapshot
  # 2 number of iterations between snapshots
  # 3 plane - 1=x 2=y 3=z
  # 4-9 coordinates of the lower left and top right corners of the plane x1 y1 z1 x2 y2 z2
  # 10-18 field components to be sampled ex ey ez hx hy hz Ix Iy Iz
  # 19 print power? =0/1
  # 20 create EPS (->epsilon->refractive index) snapshot? =0/1
  # 21 write an output file in "list" format
  # 22 write an output file in "matrix" format
  #
  # List format ( as used in version 11 ) which has a filename of the form "x1idaa.prn", where "x" is the plane over
  # which the snapshot has been taken, "1"is the snapshot serial number. ie. the snaps are numbered in the order which
  # they appear in the input file.. "id" in an identifier specified in the "flags" object. "aa" is the time serial number ie.
  # if snapshots are asked for at every 100 iterations then the first one will have "aa", the second one "ab" etc
  # The file consists of a single header line followed by columns of numbers, one for each field component wanted and
  # two for the coordinates of the point which has been sampled. These files can be read into Gema.
  #
  # Matrix format for each snapshot a file is produced for each requested field component with a name of the form
  # "x1idaa_ex" where the "ex" is the field component being sampled. The rest of the filename is tha same as for the list
  # format case. The file consists of a matrix of numbers the first column and first row or which, gives the position of
  # the sample points in each direction. These files can be read into MathCad or to spreadsheet programs.'''

  def snapshot(plane,P1,P2):
    plane_ID, plane_name = planeNumberName(plane)
    #~ if plane == 1:
      #~ plane_name='X'
    #~ elif plane == 2:
      #~ plane_name='Y'
    #~ else: #plane == 3:
      #~ plane_name='Z'
    #~ end

    FILE.write('SNAPSHOT **name='+COMMENT+'\n')
    FILE.write('{\n')

    FILE.write("%d **FIRST\n" % first)
    FILE.write("%d **REPETITION\n" % repetition)
    FILE.write("%d **PLANE %s\n" % (plane_ID, plane_name))
    FILE.write("%E **X1\n" % P1[0])
    FILE.write("%E **Y1\n" % P1[1])
    FILE.write("%E **Z1\n" % P1[2])
    FILE.write("%E **X2\n" % P2[0])
    FILE.write("%E **Y2\n" % P2[1])
    FILE.write("%E **Z2\n" % P2[2])
    FILE.write("%d **EX\n" % E[0])
    FILE.write("%d **EY\n" % E[1])
    FILE.write("%d **EZ\n" % E[2])
    FILE.write("%d **HX\n" % H[0])
    FILE.write("%d **HY\n" % H[1])
    FILE.write("%d **HZ\n" % H[2])
    FILE.write("%d **JX\n" % J[0])
    FILE.write("%d **JY\n" % J[1])
    FILE.write("%d **JZ\n" % J[2])
    FILE.write("%d **POW\n" % power)
    FILE.write("%d **EPS\n" % eps)
    FILE.write('}\n')

    FILE.write('\n')


  plane_ID, plane_name = planeNumberName(plane)
  if P1[plane_ID-1] == P2[plane_ID-1]:
    snapshot(plane_ID,P1,P2)
  else:
    snapshot(1,[P1[0],P1[1],P1[2]],[P1[0],P2[1],P2[2]])
    snapshot(1,[P2[0],P1[1],P1[2]],[P2[0],P2[1],P2[2]])
    snapshot(2,[P1[0],P1[1],P1[2]],[P2[0],P1[1],P2[2]])
    snapshot(2,[P1[0],P2[1],P1[2]],[P2[0],P2[1],P2[2]])
    snapshot(3,[P1[0],P1[1],P1[2]],[P2[0],P2[1],P1[2]])
    snapshot(3,[P1[0],P1[1],P2[2]],[P2[0],P2[1],P2[2]])

def GEOfrequency_snapshot(FILE, COMMENT, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency, starting_sample, E, H, J):

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

def GEOprobe(FILE, COMMENT, position, step, E, H, J, power ):
  FILE.write('PROBE **name='+COMMENT+'\n')

  FILE.write('{\n')

  FILE.write("%E **X\n" % position[0])
  FILE.write("%E **Y\n" % position[1])
  FILE.write("%E **Z\n" % position[2])
  FILE.write("%d **STEP\n" % step)
  FILE.write("%d **EX\n" % E[0])
  FILE.write("%d **EY\n" % E[1])
  FILE.write("%d **EZ\n" % E[2])
  FILE.write("%d **HX\n" % H[0])
  FILE.write("%d **HY\n" % H[1])
  FILE.write("%d **HZ\n" % H[2])
  FILE.write("%d **JX\n" % J[0])
  FILE.write("%d **JY\n" % J[1])
  FILE.write("%d **JZ\n" % J[2])
  FILE.write("%d **POW\n" % power)
  FILE.write('}\n')

  FILE.write('\n')


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
    FILE.write("fix_filenames.sh\n")
  
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
      GEOexcitation(FILE, COMMENT, 77, [1,2,3], [4,5,6], [7,8,9], [77,88,99], 69, 12.36, 45.54, 78.87, 456, 1, 22, 333, 4444)
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
