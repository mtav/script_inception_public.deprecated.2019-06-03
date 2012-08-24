#!/usr/bin/env python

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
