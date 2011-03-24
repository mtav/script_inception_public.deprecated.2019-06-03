#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt

########################
# GENERATOR FUNCTIONS
########################
# mandatory objects
def GEOmesh(FILE, delta_X_vector, delta_Y_vector, delta_Z_vector):
  ''' writes mesh to FILE '''
  # mesh X
  fprintf(FILE,'XMESH **XMESH DEFINITION\n');
  fprintf(FILE,'{\n');
  for i in range(len(delta_X_vector)):
    fprintf(FILE,'%E\n', delta_X_vector[i]);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

  # mesh Y
  fprintf(FILE,'YMESH **YMESH DEFINITION\n');
  fprintf(FILE,'{\n');
  for i in range(len(delta_Y_vector)):
    fprintf(FILE,'%E\n', delta_Y_vector[i]);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

  # mesh Z
  fprintf(FILE,'ZMESH **ZMESH DEFINITION\n');
  fprintf(FILE,'{\n');
  for i in range(len(delta_Z_vector)):
    fprintf(FILE,'%E\n', delta_Z_vector[i]);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

def GEOflag(FILE, iteration_method, propagation_constant, flag_1, flag_2, iterations, timestep, id_character):
  fprintf(FILE,'FLAG  **PROGRAM CONTROL OPTIONS\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%d **ITERATION METHOD\n', iteration_method);
  fprintf(FILE,'%d **PROPAGATION CONSTANT (IGNORED IN 3D MODEL)\n', propagation_constant);
  fprintf(FILE,'%d **FLAG ONE\n', flag_1);
  fprintf(FILE,'%d **FLAG TWO\n', flag_2);
  fprintf(FILE,'%d **ITERATIONS\n', iterations);
  fprintf(FILE,'%E **TIMESTEP as a proportion of the maximum allowed\n', timestep);
  fprintf(FILE,'"%s" **ID CHARACTER (ALWAYS USE QUOTES)\n', id_character);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

def GEOboundary(FILE, Xpos_bc, Xpos_param,\
                            Ypos_bc, Ypos_param,\
                            Zpos_bc, Zpos_param,\
                            Xneg_bc, Xneg_param,\
                            Yneg_bc, Yneg_param,\
                            Zneg_bc, Zneg_param):
  fprintf(FILE,'BOUNDARY  **BOUNDARY DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%d %d %d %d **X+ \n', Xpos_bc, Xpos_param(1), Xpos_param(2), Xpos_param(3));
  fprintf(FILE,'%d %d %d %d **Y+ \n', Ypos_bc, Ypos_param(1), Ypos_param(2), Ypos_param(3));
  fprintf(FILE,'%d %d %d %d **Z+ \n', Zpos_bc, Zpos_param(1), Zpos_param(2), Zpos_param(3));
  fprintf(FILE,'%d %d %d %d **X- \n', Xneg_bc, Xneg_param(1), Xneg_param(2), Xneg_param(3));
  fprintf(FILE,'%d %d %d %d **Y- \n', Yneg_bc, Yneg_param(1), Yneg_param(2), Yneg_param(3));
  fprintf(FILE,'%d %d %d %d **Z- \n', Zneg_bc, Zneg_param(1), Zneg_param(2), Zneg_param(3));
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

def GEObox(FILE, lower, upper):
  fprintf(FILE,'BOX  **BOX DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **XL\n', lower(1));
  fprintf(FILE,'%E **YL\n', lower(2));
  fprintf(FILE,'%E **ZL\n', lower(3));
  fprintf(FILE,'%E **XU\n', upper(1));
  fprintf(FILE,'%E **YU\n', upper(2));
  fprintf(FILE,'%E **ZU\n', upper(3));
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

# geometry objects
def GEOsphere(FILE, center, outer_radius, inner_radius, permittivity, conductivity):
  ''' sphere
  {
   1-5 Coordinates of the sphere ( xc yc zc r1 r2 )
   6 permittivity
   7 conductivity
  } '''
  fprintf(FILE,'SPHERE  **SPHERE DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **XC\n', center(1));
  fprintf(FILE,'%E **YC\n', center(2));
  fprintf(FILE,'%E **ZC\n', center(3));
  fprintf(FILE,'%E **outer_radius\n', outer_radius);
  fprintf(FILE,'%E **inner_radius\n', inner_radius);
  fprintf(FILE,'%E **permittivity\n', permittivity);
  fprintf(FILE,'%E **conductivity\n', conductivity);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

def GEOblock(FILE, lower, upper, permittivity, conductivity):
  fprintf(FILE,'BLOCK **Block Definition (XL,YL,ZL,XU,YU,ZU)\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **XL\n', lower(1));
  fprintf(FILE,'%E **YL\n', lower(2));
  fprintf(FILE,'%E **ZL\n', lower(3));
  fprintf(FILE,'%E **XU\n', upper(1));
  fprintf(FILE,'%E **YU\n', upper(2));
  fprintf(FILE,'%E **ZU\n', upper(3));
  fprintf(FILE,'%E **relative Permittivity\n', permittivity);
  fprintf(FILE,'%E **Conductivity\n', conductivity);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

def GEOcylinder(FILE, centre, inner_radius, outer_radius, H, permittivity, conductivity, angle_deg):
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

  fprintf(FILE,'CYLINDER **Cylinder Definition\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **X CENTRE\n', centre(1));
  fprintf(FILE,'%E **Y CENTRE\n', centre(2));
  fprintf(FILE,'%E **Z CENTRE\n', centre(3));
  fprintf(FILE,'%E **inner_radius\n', inner_radius);
  fprintf(FILE,'%E **outer_radius\n', outer_radius);
  fprintf(FILE,'%E **HEIGHT\n', H);
  fprintf(FILE,'%E **Permittivity\n', permittivity);
  fprintf(FILE,'%E **Conductivity\n', conductivity);
  fprintf(FILE,'%E **Angle of rotation in degrees around -Z=(0,0,-1)\n', angle_deg);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

def GEOrotation(FILE, axis_point, axis_direction, angle_degrees):
  # rotation structure. Actually affects previous geometry object in Prof. Railton's modified BrisFDTD. Not fully implemented yet.
  # Should be integrated into existing structures using a directional vector anyway, like in MEEP. BrisFDTD hacking required... :)

  fprintf(FILE,'ROTATION **Rotation Definition, affects previous geometry object\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **X axis_point\n', axis_point(1));
  fprintf(FILE,'%E **Y axis_point\n', axis_point(2));
  fprintf(FILE,'%E **Z axis_point\n', axis_point(3));
  fprintf(FILE,'%E **X axis_direction\n', axis_direction(1));
  fprintf(FILE,'%E **Y axis_direction\n', axis_direction(2));
  fprintf(FILE,'%E **Z axis_direction\n', axis_direction(3));
  fprintf(FILE,'%E **angle_degrees\n', angle_degrees);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

# excitation objects
def GEOexcitation(FILE, current_source, P1, P2, E, H, type, time_constant, amplitude, time_offset, frequency, param1, param2, param3, param4):
  fprintf(FILE,'EXCITATION **EXCITATION DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%d ** CURRENT SOURCE \n', current_source);
  fprintf(FILE,'%E **X1\n', P1(1));
  fprintf(FILE,'%E **Y1\n', P1(2));
  fprintf(FILE,'%E **Z1\n', P1(3));
  fprintf(FILE,'%E **X2\n', P2(1));
  fprintf(FILE,'%E **Y2\n', P2(2));
  fprintf(FILE,'%E **Z2\n', P2(3));
  fprintf(FILE,'%d **EX\n', E(1));
  fprintf(FILE,'%d **EY\n', E(2));
  fprintf(FILE,'%d **EZ\n', E(3));
  fprintf(FILE,'%d **HX\n', H(1));
  fprintf(FILE,'%d **HY\n', H(2));
  fprintf(FILE,'%d **HZ\n', H(3));
  fprintf(FILE,'%d **GAUSSIAN MODULATED SINUSOID\n', type);
  fprintf(FILE,'%E **TIME CONSTANT\n', time_constant);
  fprintf(FILE,'%E **AMPLITUDE\n', amplitude);
  fprintf(FILE,'%E **TIME OFFSET\n', time_offset);
  fprintf(FILE,'%E **FREQ (HZ)\n', frequency);
  fprintf(FILE,'%d **UNUSED PARAMETER\n', param1);
  fprintf(FILE,'%d **UNUSED PARAMETER\n', param2);
  fprintf(FILE,'%d **UNUSED PARAMETER\n', param3);
  fprintf(FILE,'%d **UNUSED PARAMETER\n', param4);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

# measurement objects
def GEOtime_snapshot(FILE, first, repetition, plane, P1, P2, E, H, J, power, eps):
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
    if plane == 1:
      plane_name='X';
    elif plane == 2:
      plane_name='Y';
    else: #plane == 3:
      plane_name='Z';
    end

    fprintf(FILE,'SNAPSHOT **SNAPSHOT DEFINITION %s\n',plane_name);
    fprintf(FILE,'{\n');
    fprintf(FILE,'%d **FIRST\n', first);
    fprintf(FILE,'%d **REPETITION\n', repetition);
    fprintf(FILE,'%d **PLANE\n', plane);
    fprintf(FILE,'%E **X1\n', P1(1));
    fprintf(FILE,'%E **Y1\n', P1(2));
    fprintf(FILE,'%E **Z1\n', P1(3));
    fprintf(FILE,'%E **X2\n', P2(1));
    fprintf(FILE,'%E **Y2\n', P2(2));
    fprintf(FILE,'%E **Z2\n', P2(3));
    fprintf(FILE,'%d **EX\n', E(1));
    fprintf(FILE,'%d **EY\n', E(2));
    fprintf(FILE,'%d **EZ\n', E(3));
    fprintf(FILE,'%d **HX\n', H(1));
    fprintf(FILE,'%d **HY\n', H(2));
    fprintf(FILE,'%d **HZ\n', H(3));
    fprintf(FILE,'%d **JX\n', J(1));
    fprintf(FILE,'%d **JY\n', J(2));
    fprintf(FILE,'%d **JZ\n', J(3));
    fprintf(FILE,'%d **POW\n', power);
    fprintf(FILE,'%d **EPS\n', eps);
    fprintf(FILE,'}\n');
    fprintf(FILE,'\n');

  if P1[plane] == P2[plane]:
    snapshot(plane,P1,P2);
  else:
    snapshot(1,[P1(1),P1(2),P1(3)],[P1(1),P2(2),P2(3)]);
    snapshot(1,[P2(1),P1(2),P1(3)],[P2(1),P2(2),P2(3)]);
    snapshot(2,[P1(1),P1(2),P1(3)],[P2(1),P1(2),P2(3)]);
    snapshot(2,[P1(1),P2(2),P1(3)],[P2(1),P2(2),P2(3)]);
    snapshot(3,[P1(1),P1(2),P1(3)],[P2(1),P2(2),P1(3)]);
    snapshot(3,[P1(1),P1(2),P2(3)],[P2(1),P2(2),P2(3)]);

def GEOfrequency_snapshot(FILE, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency, starting_sample, E, H, J):

  def snapshot(plane,P1,P2, frequency):
    if plane == 1:
      plane_name='X';
    elif plane == 2:
      plane_name='Y';
    else: #plane == 3
      plane_name='Z';
    fprintf(FILE,'FREQUENCY_SNAPSHOT **SNAPSHOT DEFINITION %s\n',plane_name);
    fprintf(FILE,'{\n');
    fprintf(FILE,'%d **FIRST\n', first);
    fprintf(FILE,'%d **REPETITION\n', repetition);
    fprintf(FILE,'%d **interpolate?\n', interpolate);
    fprintf(FILE,'%d **REAL DFT\n', real_dft);
    fprintf(FILE,'%d **MOD ONLY\n', mod_only);
    fprintf(FILE,'%d **MOD ALL\n', mod_all);
    fprintf(FILE,'%d **PLANE\n', plane);
    fprintf(FILE,'%E **X1\n', P1(1));
    fprintf(FILE,'%E **Y1\n', P1(2));
    fprintf(FILE,'%E **Z1\n', P1(3));
    fprintf(FILE,'%E **X2\n', P2(1));
    fprintf(FILE,'%E **Y2\n', P2(2));
    fprintf(FILE,'%E **Z2\n', P2(3));
    fprintf(FILE,'%E **FREQUENCY (HZ)\n', frequency);
    fprintf(FILE,'%d **STARTING SAMPLE\n', starting_sample);
    fprintf(FILE,'%d **EX\n', E(1));
    fprintf(FILE,'%d **EY\n', E(2));
    fprintf(FILE,'%d **EZ\n', E(3));
    fprintf(FILE,'%d **HX\n', H(1));
    fprintf(FILE,'%d **HY\n', H(2));
    fprintf(FILE,'%d **HZ\n', H(3));
    fprintf(FILE,'%d **JX\n', J(1));
    fprintf(FILE,'%d **JY\n', J(2));
    fprintf(FILE,'%d **JZ\n', J(3));
    fprintf(FILE,'}\n');
    fprintf(FILE,'\n');

  for i in range(len(frequency)):
    if P1[plane] == P2[plane]:
      snapshot(plane,P1,P2,frequency(i));
    else:
      snapshot(1,[P1(1),P1(2),P1(3)],[P1(1),P2(2),P2(3)],frequency(i));
      snapshot(1,[P2(1),P1(2),P1(3)],[P2(1),P2(2),P2(3)],frequency(i));
      snapshot(2,[P1(1),P1(2),P1(3)],[P2(1),P1(2),P2(3)],frequency(i));
      snapshot(2,[P1(1),P2(2),P1(3)],[P2(1),P2(2),P2(3)],frequency(i));
      snapshot(3,[P1(1),P1(2),P1(3)],[P2(1),P2(2),P1(3)],frequency(i));
      snapshot(3,[P1(1),P1(2),P2(3)],[P2(1),P2(2),P2(3)],frequency(i));

def GEOprobe(FILE, position, step, E, H, J, power ):
  fprintf(FILE,'PROBE **PROBE DEFINITION\n');
  fprintf(FILE,'{\n');
  fprintf(FILE,'%E **X\n', position(1));
  fprintf(FILE,'%E **Y\n', position(2));
  fprintf(FILE,'%E **Z\n', position(3));
  fprintf(FILE,'%d **STEP\n', step);
  fprintf(FILE,'%d **EX\n', E(1));
  fprintf(FILE,'%d **EY\n', E(2));
  fprintf(FILE,'%d **EZ\n', E(3));
  fprintf(FILE,'%d **HX\n', H(1));
  fprintf(FILE,'%d **HY\n', H(2));
  fprintf(FILE,'%d **HZ\n', H(3));
  fprintf(FILE,'%d **JX\n', J(1));
  fprintf(FILE,'%d **JY\n', J(2));
  fprintf(FILE,'%d **JZ\n', J(3));
  fprintf(FILE,'%d **POW\n', power);
  fprintf(FILE,'}\n');
  fprintf(FILE,'\n');

# files
def GEOcommand(filename, BASENAME):
  ''' CMD file generation '''
  print('Writing CMD file...');

  #open file
  out = fopen(strcat(filename,'.cmd'),'wt');

  # Executable = 'D:\fdtd\source\latestfdtd02_03\subgrid\Fdtd32.exe';
  Executable = fullfile(getuserdir(),'bin','fdtd.exe');

  #write file
  fprintf(out,'Executable = %s\n',Executable);
  fprintf(out,'\n');
  fprintf(out,'input = %s.in\n', BASENAME);
  fprintf(out,'\n');
  fprintf(out,'output = fdtd.out\n');
  fprintf(out,'\n');
  fprintf(out,'error = error.log\n');
  fprintf(out,'\n');
  fprintf(out,'Universe = vanilla\n');
  fprintf(out,'\n');
  fprintf(out,'transfer_files = ALWAYS\n');
  fprintf(out,'\n');
  fprintf(out,'transfer_input_files = entity.lst, %s.geo, %s.inp\n', BASENAME, BASENAME);
  fprintf(out,'\n');
  fprintf(out,'Log = foo.log\n');
  fprintf(out,'\n');
  fprintf(out,'Rank = Memory >= 1000\n');
  fprintf(out,'\n');
  fprintf(out,'LongRunJob = TRUE\n');
  fprintf(out,'\n');
  fprintf(out,'###Requirements = (LongRunMachine =?= TRUE)\n');
  fprintf(out,'\n');
  fprintf(out,'queue\n');

  #close file
  fclose(out);
  print('...done');

def GEOin(filename, file_list):
  ''' IN file generation '''
  print('Writing IN file...');

  #open file
  out = fopen(filename,'wt');

  #write file
  for idx in len(file_list):
    fprintf(out, '%s\n', file_list[idx]);

  #close file
  fclose(out);
  print('...done');

def GEOshellscript(filename, BASENAME, EXE, WORKDIR, WALLTIME):
  print('Writing shellscript...')

  #open file
  out = fopen(filename,'wt');

  if exist('EXE','var')==0:
    # print('EXE not given');
    # EXE = '$HOME/bin/fdtd64_2003';
    # EXE = '$HOME/bin/fdtd';
    EXE = 'fdtd';
    print(['EXE not given. Using default: EXE=',EXE]);

  if exist('WORKDIR','var')==0:
    # print('WORKDIR not given');
    # WORKDIR = '$(dirname "$0")';
    #TODO: Is WORKDIR even necessary in the script? O.o
    WORKDIR = '$JOBDIR';
    print(['WORKDIR not given. Using default: WORKDIR=',WORKDIR]);
  
  if exist('WALLTIME','var')==0:
    WALLTIME = 12;
    print(['WALLTIME not given. Using default: WALLTIME=',WALLTIME]);

  #write file
  fprintf(out,'#!/bin/bash\n');
  fprintf(out,'#\n');
  fprintf(out,'#PBS -l walltime=%d:00:00\n',WALLTIME);
  fprintf(out,'#PBS -mabe\n');
  fprintf(out,'#PBS -joe\n');
  fprintf(out,'#\n');
  fprintf(out,'\n');
  fprintf(out,'\n');
  fprintf(out,'export WORKDIR=%s\n',WORKDIR);
  fprintf(out,'export EXE=%s\n',EXE);
  fprintf(out,'\n');
  fprintf(out,'cd $WORKDIR\n');
  fprintf(out,'\n');
  fprintf(out,'$EXE %s.in > %s.out\n', BASENAME, BASENAME);
  fprintf(out,'fix_filenames.sh\n');

  #close file
  fclose(out);
  print('...done')


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
    with open('tmp.txt', 'w') as f:
      f.write('hello\n')
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
