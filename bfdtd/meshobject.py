#!/usr/bin/env python3

from __future__ import division
import numpy
from bfdtd.meshobject import *
from meshing.subGridMultiLayer import *
from bfdtd.meshingparameters import MeshingParameters

# TODO: mesh based on position instead of just thicknesses? More flexibility if ever needed... (like now :/)

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
def mergeMeshingParameters(MeshParamsList, minimum_mesh_delta = 1e-3):
  ''' returns parameters that can be used for meshing with subGridMultiLayer '''

  N = len(MeshParamsList)
  
  # Xvec is an array of size (N,2) containing a list of (lower,upper) pairs corresponding to the meshing subdomains defined by the various geometrical objects.
  # epsX is an array of size (N,1) containing a list of epsilon values corresponding to the meshing subdomains defined by the various geometrical objects.
  # The (lower,upper) pairs from Xvec are associated with the corresponding epsilon values from epsX to determine an appropriate mesh in the X direction.
  Xvec = numpy.zeros([N,2])
  epsX = numpy.zeros([N,1])

  for mesh_params_idx in range(N):
    mesh_params = MeshParamsList[mesh_params_idx]
    Xvec[mesh_params_idx,0] = mesh_params.pos_min
    Xvec[mesh_params_idx,1] = mesh_params.pos_max
    epsX[mesh_params_idx,0] = mesh_params.delta_max
  
  VX = numpy.unique(numpy.sort(numpy.vstack([Xvec[:,0],Xvec[:,1]])))
  MX = numpy.inf*numpy.ones((Xvec.shape[0],len(VX))) # We fill with numpy.inf so that when we take the min(), those values get discarded.

  # Fill MX so that each line is filled with the eps for that line, but only in the ranges where it should apply.
  for m in range(Xvec.shape[0]):
    indmin = numpy.nonzero(VX==Xvec[m,0])[0][0] # index in VX of Xvec[m,0] (=pos_min)
    indmaX = numpy.nonzero(VX==Xvec[m,1])[0][0] # index in VX of Xvec[m,1] (=pos_max)
    MX[m,indmin:indmaX] = epsX[m,0]

  # Compute thickness vector from position vector
  thicknessVX = numpy.diff(VX)
    
  # epsVX = MX minus the last column
  epsVX = MX[:,0:MX.shape[1]-1]
  epsVX = epsVX.min(0) # different from current implementation in bfdtd_parser automesher!
  
  maxPermittivityVector_X = []
  thicknessVector_X = []
  
  # TODO: use (thickness, epsilon) tuples so that filter() and similar functions can be used. Also prevents errors if lists have different lengths.
  # ex: t = filter(lambda x: x>=1, t)
  # filter out parts smaller than minimum_mesh_delta_vector3[i]
  # NOTE: This might lead to errors because we never make up for the eliminated layers.
  # TODO: Fix by merging close lines instead of simply ignoring the corresponding layers.
  for idx in range(len(thicknessVX)):
    if thicknessVX[idx] >= minimum_mesh_delta:
      maxPermittivityVector_X.append(epsVX[idx])
      thicknessVector_X.append(thicknessVX[idx])
  
  delta_X_vector, local_delta_X_vector = subGridMultiLayer(maxPermittivityVector_X, thicknessVector_X)

  mesh = numpy.cumsum(numpy.hstack((VX[0],delta_X_vector)))
  
  return mesh
