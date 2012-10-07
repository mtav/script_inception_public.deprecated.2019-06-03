#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import os
import getopt
import numpy

# TODO: Make it work with Section_MaxDelta = numpy.inf as well.
def subGridMultiLayer(Section_MaxDeltaVector_in = [1.76, 2.1385, 2.3535, 1],Section_ThicknessVector_in = [1, 0.5, 1, 1]):
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
  
  # check lengths
  if len(Section_ThicknessVector_in)!=len(Section_MaxDeltaVector_in):
    print('FATAL ERROR: len(Section_ThicknessVector_in)!=len(Section_MaxDeltaVector_in)')
    sys.exit(-1)
    
  #if 0 in Section_ThicknessVector_in:
    #print('WARNING: Section_ThicknessVector_in contains zeroes')
  
  Section_ThicknessVector = []
  Section_MaxDeltaVector = []
  for i in range(len(Section_ThicknessVector_in)):
    if Section_ThicknessVector_in[i]!=0:
      Section_ThicknessVector.append(Section_ThicknessVector_in[i])
      Section_MaxDeltaVector.append(Section_MaxDeltaVector_in[i])
      
  # check for zeroes
  if 0 in Section_MaxDeltaVector:
    print(('FATAL ERROR: Section_MaxDeltaVector contains zeroes : '+str(Section_MaxDeltaVector)))
    sys.exit(-1)
  
  Section_MaxDeltaVector = numpy.array(Section_MaxDeltaVector)
  Section_ThicknessVector = numpy.array(Section_ThicknessVector)
  
  if len(Section_MaxDeltaVector) != len(Section_ThicknessVector) :
    print('FATAL ERROR: The 2 input vectors do not have the same size.')
    sys.exit(-1)

  if min(Section_MaxDeltaVector)<0:
    print(('FATAL ERROR: Section_MaxDeltaVector contains negative values: '+str(Section_MaxDeltaVector)))
    sys.exit(-1)

  if min(Section_ThicknessVector)<0:
    print(('FATAL ERROR: Section_ThicknessVector contains negative values: '+str(Section_ThicknessVector)))
    sys.exit(-1)

  totalHeight = sum(Section_ThicknessVector);

  nLayers = len(Section_ThicknessVector);

  nCellsV = numpy.ceil( Section_ThicknessVector.astype(float) / Section_MaxDeltaVector.astype(float) )
  #print('nCellsV')
  #print(nCellsV)
  #sys.exit(-1)
  for i in range(len(nCellsV)):
    if nCellsV[i]==0:
      nCellsV[i]=1
    
  Section_FinalDeltaVector = Section_ThicknessVector.astype(float) / nCellsV.astype(float)

  Mesh_ThicknessVector = [];
  for m in range(nLayers):
    Mesh_ThicknessVector = numpy.concatenate( ( Mesh_ThicknessVector, Section_FinalDeltaVector[m]*numpy.ones(nCellsV[m]) ) )

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
    except getopt.error as msg:
      raise Usage(msg)
    # more code, unchanged
    Mesh_ThicknessVector, Section_FinalDeltaVector = subGridMultiLayer([1,2,3,4,5],[5,4,3,2,1])
    print(('Mesh_ThicknessVector = '+str(Mesh_ThicknessVector)))
    print(('Section_FinalDeltaVector = '+str(Section_FinalDeltaVector)))
    
  except Usage as err:
    print(err.msg, file=sys.stderr)
    print("for help use --help", file=sys.stderr)
    return 2

if __name__ == "__main__":
  sys.exit(main())
