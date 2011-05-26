#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geometries.pillar_1D_wrapper import *
import re
from bfdtd.bfdtd_parser import *

# TODO: rewrite this function so it doesn't depend on the filename (i.e. just copy (import/export better of course :) ) everything as it is and add the snapshots to the .inp file...)

def rerun(filename):
  filename = os.path.abspath(filename)
  freq_snapshots = getFrequencies(filename)
  print freq_snapshots
  
  BASE = os.path.basename(filename)
  DIR = os.path.dirname(filename)
  print 'BASE = ', BASE
  print 'DIR = ', DIR
  updir1,filename_base = os.path.split(filename)
  updir2,updir1_base = os.path.split(updir1)
  if updir1_base == 'harminv':
    basedir = os.path.abspath(updir2)
  else:
    basedir = os.path.abspath(updir1)
    
  #head,basedir = os.path.split(head)
  print 'basedir = ', basedir
  
  pattern = re.compile("(.*).bottomN_(\d+).topN_(\d+).excitationType_([XYZ]m[12])")
  str_to_match = os.path.basename(basedir)
  m = pattern.match(str_to_match)
  print m
  if m:
    print m.groups()
    pillarType = m.group(1).strip()
    bottomN = int(m.group(2).strip())
    topN = int(m.group(3).strip())
    axis = m.group(4).strip()
    print axis
    excitationType = -1
    if axis == 'Ym1':
      excitationType = 0
    elif axis == 'Zm1':
      excitationType = 1
    elif axis == 'Ym2':
      excitationType = 2
    elif axis == 'Zm2':
      excitationType = 3
    print 'excitationType = ', excitationType

    DSTDIR = os.path.abspath(basedir+os.sep+'resonance')
    print 'DSTDIR=', DSTDIR
    if not os.path.isdir(DSTDIR):
      os.mkdir(DSTDIR)
      
    INPFILE = os.path.dirname(filename)+os.sep+os.path.basename(basedir)+'.inp'
    print 'INPFILE = ', INPFILE
    # TODO: use this to write out exactly the same geo/inp set, except with frequency snapshots added
    structured_entries = readBristolFDTD(INPFILE)
    iterations = structured_entries.flag.numSteps
    print 'iterations = ', iterations
    
    #for iterations in [10,32000,261600,300000,1048400]:
    #DSTDIR = basedir+os.sep+'resonance' + os.sep + 'iterations_' + str(iterations)
    #if not os.path.isdir(DSTDIR):
      #os.mkdir(DSTDIR)
    if pillarType == 'rectangular_holes':
      rectangular_holes(DSTDIR,bottomN,topN,excitationType,iterations,freq_snapshots)
    elif pillarType == 'rectangular_yagi':
      P = rectangular_yagi(bottomN, topN, excitationType, iterations, freq_snapshots, 1)
      baseName = 'rectangular_yagi.bottomN_%BOTTOMN.topN_%TOPN.excitationType_%EXCITATIONTYPESTR'
      P.write(DSTDIR,baseName)
    elif pillarType == 'rectangular_yagi_LambdaOver2Cavity':
      P = rectangular_yagi(bottomN, topN, excitationType, iterations, freq_snapshots, 0.5)
      baseName = 'rectangular_yagi_LambdaOver2Cavity.bottomN_%BOTTOMN.topN_%TOPN.excitationType_%EXCITATIONTYPESTR'
      P.write(DSTDIR,baseName)
    elif pillarType == 'cylinder':
      cylinder(DSTDIR,bottomN,topN,excitationType,iterations,freq_snapshots)
    elif pillarType == 'triangular_yagi':
      triangular_yagi(DSTDIR,bottomN,topN,excitationType,iterations,freq_snapshots)
    elif pillarType == 'triangular_yagi_voxel':
      triangular_yagi_voxel(DSTDIR,bottomN,topN,excitationType,iterations,freq_snapshots)
    elif pillarType == 'triangular_yagi_voxel_sym':
      triangular_yagi_voxel_sym(DSTDIR,bottomN,topN,excitationType,iterations,freq_snapshots)
    else:
      print 'UNKNOWN pillarType = ', pillarType

  else:
    print 'NO MATCH ON : ', str_to_match
  
  
  #for excitationType in range(4):
    #for iterations in [10,32000,261600,300000,1048400]:
      #freq_snapshots = 
      #mission1(os.getenv('DATADIR')+os.sep+'mission1.iterations_'+str(iterations),excitationType,iterations,freq_snapshots)
      #mission2(os.getenv('DATADIR')+os.sep+'mission2.iterations_'+str(iterations),excitationType,iterations,freq_snapshots)
      #mission3(os.getenv('DATADIR')+os.sep+'mission3.iterations_'+str(iterations),excitationType,iterations,freq_snapshots)
      #mission4(os.getenv('DATADIR')+os.sep+'mission4.iterations_'+str(iterations),excitationType,iterations,freq_snapshots)
  
  #loncar_cylinder('loncar_cyl_python', DSTDIR, iterations, True, True, 'cylinder', 0.150/2.0, 0.637, [get_c0()/0.637],excitationType)
  #loncar_structure('loncar_rect_python', DSTDIR, iterations, True, True, 'rectangular_holes', 1, 0.637, [get_c0()/0.637], excitationType)

  #cylinder(os.getenv('TESTDIR'), 12, 12, 0)

#def preRerun(filename):
  #with open(filename, 'r') as f:
    #f.readline()
    #for line in f:
      #freq_snapshots.append(double(line.split()[1])*1e-6)
            ##read_data = f.read()
    ##print read_data
  #f.closed
  #return freq_snapshots

def copyBFDTD(src,dst):
  ''' Copy src to dst '''
  FDTDobj = readBristolFDTD(src)
  FDTDobj.writeAll(dst)

def main(argv=None):
  if argv is None:
      argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
      raise Usage(msg)
      
    copyBFDTD(sys.argv[1],sys.argv[2])
    sys.exit(0)
    
    # main function
    for i in sys.argv[1:]:
      print '==>Processing '+i
      rerun(i)
    return

  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
