#!/usr/bin/env python

from __future__ import division
import numpy

class MeshObject(object):
  def __init__(self):
    self.name = 'mesh'
    self.xmesh = numpy.array([])
    self.ymesh = numpy.array([])
    self.zmesh = numpy.array([])

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
