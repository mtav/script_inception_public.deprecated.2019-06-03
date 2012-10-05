#!/usr/bin/env python3

from __future__ import division
import numpy
from bfdtd.meshobject import *
from meshing.subGridMultiLayer import *

class MeshObject(object):
  def __init__(self):
    '''
    xmesh: list of the position (not a thickness list!) of each line of the mesh in the x direction
    ymesh: list of the position (not a thickness list!) of each line of the mesh in the y direction
    zmesh: list of the position (not a thickness list!) of each line of the mesh in the z direction
    ex:
    xmesh = [0, 0.25, 0.5, 0.75, 1] will create a [0.25, 0.25, 0.25, 0.25] thickness sequence in the XMESH object of the .inp file.
    '''
    self.name = 'mesh'
    self.xmesh = numpy.array([0,1])
    self.ymesh = numpy.array([0,1])
    self.zmesh = numpy.array([0,1])

  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'xmesh = ' + str(self.xmesh) + '\n' +\
    'ymesh = ' + str(self.ymesh) + '\n' +\
    'zmesh = ' + str(self.zmesh)
    return ret
    
  def setXmesh(self,xmesh):
    self.xmesh = xmesh
  def setYmesh(self,ymesh):
    self.ymesh = ymesh
  def setZmesh(self,zmesh):
    self.zmesh = zmesh
  def setMesh(self,xmesh,ymesh,zmesh):
    self.xmesh = xmesh
    self.ymesh = ymesh
    self.zmesh = zmesh
    
  def getXmesh(self):
    return(self.xmesh)
  def getYmesh(self):
    return(self.ymesh)
  def getZmesh(self):
    return(self.zmesh)
  def getMesh(self):
    return(self.xmesh,self.ymesh,self.zmesh)

  def setXmeshDelta(self,xmesh_delta):
    self.xmesh = numpy.cumsum(numpy.hstack((0,xmesh_delta)))
  def setYmeshDelta(self,ymesh_delta):
    self.ymesh = numpy.cumsum(numpy.hstack((0,ymesh_delta)))
  def setZmeshDelta(self,zmesh_delta):
    self.zmesh = numpy.cumsum(numpy.hstack((0,zmesh_delta)))
  def setMeshDelta(self,xmesh_delta,ymesh_delta,zmesh_delta):
    self.xmesh = numpy.cumsum(numpy.hstack((0,xmesh_delta)))
    self.ymesh = numpy.cumsum(numpy.hstack((0,ymesh_delta)))
    self.zmesh = numpy.cumsum(numpy.hstack((0,zmesh_delta)))
  
  def getXmeshDelta(self):
    return(numpy.diff(self.xmesh))
  def getYmeshDelta(self):
    return(numpy.diff(self.ymesh))
  def getZmeshDelta(self):
    return(numpy.diff(self.zmesh))
  def getMeshDelta(self):
    return(numpy.diff(self.xmesh),numpy.diff(self.ymesh),numpy.diff(self.zmesh))

  def setSizeAndResolution(self, size_vec3, N_vec3):
    self.xmesh = numpy.linspace(0, size_vec3[0], N_vec3[0]+1)
    self.ymesh = numpy.linspace(0, size_vec3[1], N_vec3[1]+1)
    self.zmesh = numpy.linspace(0, size_vec3[2], N_vec3[2]+1)
    return

  def getXmeshCentres(self):
    return [ 0.5*(self.xmesh[i+1]+self.xmesh[i]) for i in range(len(self.xmesh)-1)]

  def getYmeshCentres(self):
    return [ 0.5*(self.ymesh[i+1]+self.ymesh[i]) for i in range(len(self.ymesh)-1)]

  def getZmeshCentres(self):
    return [ 0.5*(self.zmesh[i+1]+self.zmesh[i]) for i in range(len(self.zmesh)-1)]

  def getNcells(self):
    ''' Returns the number of cells in the mesh. '''
    return len(self.getXmeshDelta())*len(self.getYmeshDelta())*len(self.getZmeshDelta())

  def getSizeAndResolution(self):
    return ([self.xmesh[-1],self.zmesh[-1],self.zmesh[-1]],[len(self.getXmeshDelta()),len(self.getYmeshDelta()),len(self.getZmeshDelta())])


########################################
# GENERIC 1-D MESH CLASSES:

# NOTE: This will go into external 1-D MeshObjects (of which there will be heterogeneous (arbitrary mesh) and homogeneous ones (meshing parameters)).
# NOTE: Each Geometry object will be able to have a set of MeshObjects of one or both types. HeteroMeshs can be created from sets of homo+hetero meshs.
# NOTE: There may be a parent generic MeshObject class.

# TODO: Ability somehow to mix 1D,2D,3D meshes (infinity thickness/delta value? new classes? "useForMeshing" attribute? <- sounds good)

# The following class names are all temporary and subject to change!

# NOTE: Temporary name. To be changed later, once everything is nicely in place.
class MeshPapa(object):
  def __init__(self):
    self.useForMeshing = True
    
    # NOTE: to be able to fix certain meshing regions. But might conflict with MaxCells targets, etc. Need to find a solution.
    self.useMeshFactor = True
    
    return

# NOTE: previously named HomogeneousMesh
class MeshParams(MeshPapa):
  def __init__(self, pos_min = None, pos_max = None):
    
    if pos_min is None: pos_min = 0
    if pos_max is None: pos_max = 1
    
    self.pos_min = min(pos_min,pos_max)
    self.pos_max = max(pos_min,pos_max)
    self.delta_max = abs(self.pos_max-self.pos_min)
    return

  def __str__(self):
    ret = 'pos_min = '+str(self.pos_min)+'\n'
    ret += 'pos_max = '+str(self.pos_max)+'\n'
    ret += 'delta_max = '+str(self.delta_max)
    return ret

  def setExtension(self, pos_min, pos_max):
    self.pos_min = min(pos_min,pos_max)
    self.pos_max = max(pos_min,pos_max)
    return
  def getExtension(self):
    return (self.pos_min, self.pos_max)

  def setDeltaMax(self, DeltaMax):
    self.delta_max = DeltaMax
    return
  def getDeltaMax(self):
    return self.delta_max
  
  def setNmin(self, Nmin):
    ''' set the number of "cells" in the mesh (NOT the number of "positions", which is Nmin+1) '''
    self.delta_max = abs(self.pos_max-self.pos_min)/float(Nmin)
    return
  def getNmin(self):
    ''' get the number of "cells" in the mesh (NOT the number of "positions", which is Nmin+1) '''
    Nmin = numpy.ceil(abs(self.pos_max-self.pos_min)/float(self.delta_max))
    if Nmin < 1:
      Nmin = 1
    return(Nmin)

  def setPermittivityMin(self, PermittivityMin):
    self.delta_max = 1./numpy.sqrt(PermittivityMin)
    return
  def getPermittivityMin(self):
    return numpy.power(1./self.delta_max,2)

  def setRefractiveIndexMin(self, RefractiveIndexMin):
    self.delta_max = 1./RefractiveIndexMin
    return
  def getRefractiveIndexMin(self):
    return 1./self.delta_max
    
  # This class uses "delta" as main attribute for more flexibility. Useful when merging meshes.
  # But when a thickness or position list is requested, we simply switch to "N" as main, i.e. we create a homogeneous mesh. (hence why class name should be changed to meshParams or something)
  def getThicknessList(self):
    return(numpy.diff(self.getPositionList()))
  def getPositionList(self):
    N = self.getNmin()
    return numpy.linspace(self.pos_min, self.pos_max, N+1)

# TODO: Rename to ArbitraryMesh ?
class HeterogeneousMesh(MeshPapa):
  def __init__(self):
    self.PositionList = [0,1]
    return

  def getPositionList(self):
    return self.PositionList
  def setPositionList(self, PositionList):
    self.PositionList = PositionList
    return

  def getThicknessList(self):
    return(numpy.diff(self.PositionList))
  def setThicknessList(self, pos_min, ThicknessList):
    self.PositionList = numpy.cumsum(numpy.hstack((pos_min,ThicknessList)))
    return

########################################

# TODO: 3-D MESH CLASS
# TODO: Cleanup, get rid of deprecated mesh system, make sure everything works

# TODO: mesh merging functions + mesh conversion functions
# TODO: Generic 1-D function to merge meshing parameters of the form [lower, upper, maxDelta]
def mergeMeshingParameters(minimum_mesh_delta_vector3):
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
  
