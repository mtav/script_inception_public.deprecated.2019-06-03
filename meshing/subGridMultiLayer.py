#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import os
import getopt
import numpy

# TODO: Generic 1-D function to merge meshing parameters of the form [lower, upper, maxDelta]
def calculateMeshingParameters(minimum_mesh_delta_vector3):
  ''' returns parameters that can be used for meshing:
  -Section_MaXDeltaVector_X
  -Section_ThicknessVector_X
  -Section_MaXDeltaVector_Y
  -Section_ThicknessVector_Y
  -Section_MaXDeltaVector_Z
  -Section_ThicknessVector_Z
  '''

  simMinX = self.box.lower[0]
  simMinY = self.box.lower[1]
  simMinZ = self.box.lower[2]
  simMaXX = self.box.upper[0]
  simMaXY = self.box.upper[1]
  simMaXZ = self.box.upper[2]

  # Xvec, Yvec, Zvec are arrays of size (N,2) containing a list of (lower,upper) pairs corresponding to the meshing subdomains defined by the various geometrical objects.
  # epsX, epsY, epsZ are arrays of size (N,1) containing a list of epsilon values corresponding to the meshing subdomains defined by the various geometrical objects.
  # The (lower,upper) pairs from Xvec,Yvec,Zvec are associated with the corresponding epsilon values from epsX,epsY,epsZ to determine an appropriate mesh in the X,Y,Z directions respectively.

  # box mesh
  Xvec = numpy.array([[simMinX,simMaXX]])
  Yvec = numpy.array([[simMinY,simMaXY]])
  Zvec = numpy.array([[simMinZ,simMaXZ]])
  
  epsX = numpy.array([[1]])
  epsY = numpy.array([[1]])
  epsZ = numpy.array([[1]])

  # geometry object meshes
  for obj in self.geometry_object_list:
    if self.verboseMeshing:
      print(obj.name)
      print((Xvec,Yvec,Zvec,epsX,epsY,epsZ))
    Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)
    if self.verboseMeshing:
      print((Xvec,Yvec,Zvec,epsX,epsY,epsZ))

  # mesh object meshes
  for obj in self.mesh_object_list:
    Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

  # excitation object meshes
  if self.fitMeshToExcitations:
    for obj in self.excitation_list:
      Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

  # probe object meshes
  if self.fitMeshToProbes:
    for obj in self.probe_list:
      Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

  # snapshot object meshes
  if self.fitMeshToSnapshots:
    for obj in self.snapshot_list:
      Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)
    
  # postprocess the meshes
  Xvec[Xvec<simMinX] = simMinX
  Xvec[Xvec>simMaXX] = simMaXX
  Yvec[Yvec<simMinY] = simMinY
  Yvec[Yvec>simMaXY] = simMaXY
  Zvec[Zvec<simMinZ] = simMinZ
  Zvec[Zvec>simMaXZ] = simMaXZ

  ##
  VX = numpy.unique(numpy.sort(numpy.vstack([Xvec[:,0],Xvec[:,1]])))
  MX = numpy.zeros((Xvec.shape[0],len(VX)))

  for m in range(Xvec.shape[0]):
    indmin = numpy.nonzero(VX==Xvec[m,0])[0][0]
    indmaX = numpy.nonzero(VX==Xvec[m,1])[0][0]
    eps = epsX[m,0]
    vv = numpy.zeros(len(VX))
    vv[indmin:indmaX] = eps
    MX[m,:] = vv

  thicknessVX = numpy.diff(VX)
  epsVX = MX[:,0:MX.shape[1]-1]
  epsVX = epsVX.max(0)

  ##
  VY = numpy.unique(numpy.sort(numpy.vstack([Yvec[:,0],Yvec[:,1]])))
  MY = numpy.zeros((Yvec.shape[0],len(VY)))

  for m in range(Yvec.shape[0]):
    indmin = numpy.nonzero(VY==Yvec[m,0])[0][0]
    indmax = numpy.nonzero(VY==Yvec[m,1])[0][0]
    eps = epsY[m,0]
    vv = numpy.zeros(len(VY))
    vv[indmin:indmax] = eps
    MY[m,:] = vv

  thicknessVY = numpy.diff(VY)
  epsVY = MY[:,0:MY.shape[1]-1]
  epsVY = epsVY.max(0)

  ##
  VZ = numpy.unique(numpy.sort(numpy.vstack([Zvec[:,0],Zvec[:,1]])))
  MZ = numpy.zeros((Zvec.shape[0],len(VZ)))

  for m in range(Zvec.shape[0]):
    indmin = numpy.nonzero(VZ==Zvec[m,0])[0][0]
    indmax = numpy.nonzero(VZ==Zvec[m,1])[0][0]
    eps = epsZ[m,0]
    vv = numpy.zeros(len(VZ))
    vv[indmin:indmax] = eps
    MZ[m,:] = vv

  thicknessVZ = numpy.diff(VZ)
  epsVZ = MZ[:,0:MZ.shape[1]-1]
  epsVZ = epsVZ.max(0)
      
  meshing_parameters = MeshingParameters()
  meshing_parameters.maxPermittivityVector_X = []
  meshing_parameters.thicknessVector_X = []
  meshing_parameters.maxPermittivityVector_Y = []
  meshing_parameters.thicknessVector_Y = []
  meshing_parameters.maxPermittivityVector_Z = []
  meshing_parameters.thicknessVector_Z = []
  
  # TODO: use (thickness, epsilon) tuples so that filter() and similar functions can be used. Also prevents errors if lists have different lengths.
  # ex: t = filter(lambda x: x>=1, t)
  # filter out parts smaller than minimum_mesh_delta_vector3[i]
  for idx in range(len(thicknessVX)):
    if thicknessVX[idx] >= minimum_mesh_delta_vector3[0]:
      meshing_parameters.maxPermittivityVector_X.append(epsVX[idx])
      meshing_parameters.thicknessVector_X.append(thicknessVX[idx])
  for idx in range(len(thicknessVY)):
    if thicknessVY[idx] >= minimum_mesh_delta_vector3[1]:
      meshing_parameters.maxPermittivityVector_Y.append(epsVY[idx])
      meshing_parameters.thicknessVector_Y.append(thicknessVY[idx])
  for idx in range(len(thicknessVZ)):
    if thicknessVZ[idx] >= minimum_mesh_delta_vector3[2]:
      meshing_parameters.maxPermittivityVector_Z.append(epsVZ[idx])
      meshing_parameters.thicknessVector_Z.append(thicknessVZ[idx])
  
  return meshing_parameters
  
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
