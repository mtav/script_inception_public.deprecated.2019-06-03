#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import os
import getopt
from numpy import *

def subGridMultiLayer(Section_MaxDeltaVector = [1.76, 2.1385, 2.3535, 1],Section_ThicknessVector = [1, 0.5, 1, 1]):
  ''' Create a list of thicknesses for meshing
  #
  # [Mesh_ThicknessVector,Section_FinalDeltaVector] = subGridMultiLayer(Section_MaxDeltaVector,Section_ThicknessVector)
  # Section_ThicknessVector = list of the thickness of each section
  # Section_MaxDeltaVector = list of maximum allowed deltas in each section
  # Mesh_ThicknessVector = thickness vector of the mesh
  # Section_FinalDeltaVector = list of final deltas used in the mesh
  #
  # ex:
  # Mesh_ThicknessVector = [ 3,2,2,1,1,1 ]
  # Section_FinalDeltaVector = [ 3,2,1 ]
  #
  # Note: If you are switching from the old to the new subGridMultiLayer version, replace:
  #  Section_MaxDeltaVector(new) = lambda(old)/16./indexVector(old)
  #  Section_ThicknessVector(new) = thicknessVector(old) '''
  
  print Section_MaxDeltaVector
  print Section_ThicknessVector
  
  # TODO: check for zeroes
  
  Section_MaxDeltaVector = array(Section_MaxDeltaVector)
  Section_ThicknessVector = array(Section_ThicknessVector)
  
  if len(Section_MaxDeltaVector) != len(Section_ThicknessVector) :
    print('FATAL ERROR: The 2 input vectors do not have the same size.')
    sys.exit(-1)

  if min(Section_MaxDeltaVector)<0:
    print('FATAL ERROR: Section_MaxDeltaVector contains negative values: '+str(Section_MaxDeltaVector))
    sys.exit(-1)

  if min(Section_ThicknessVector)<0:
    print('FATAL ERROR: Section_ThicknessVector contains negative values: '+str(Section_ThicknessVector))
    sys.exit(-1)

  totalHeight = sum(Section_ThicknessVector);

  nLayers = len(Section_ThicknessVector);

  nCellsV = ceil( Section_ThicknessVector.astype(float) / Section_MaxDeltaVector.astype(float) )
  Section_FinalDeltaVector = Section_ThicknessVector.astype(float) / nCellsV.astype(float)

  Mesh_ThicknessVector = [];
  for m in range(nLayers):
    Mesh_ThicknessVector = concatenate( ( Mesh_ThicknessVector, Section_FinalDeltaVector[m]*ones(nCellsV[m]) ) )

  return(Mesh_ThicknessVector,Section_FinalDeltaVector)

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
    Mesh_ThicknessVector, Section_FinalDeltaVector = subGridMultiLayer([1,2,3,4,5],[5,4,3,2,1])
    print('Mesh_ThicknessVector = '+str(Mesh_ThicknessVector))
    print('Section_FinalDeltaVector = '+str(Section_FinalDeltaVector))
    
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
