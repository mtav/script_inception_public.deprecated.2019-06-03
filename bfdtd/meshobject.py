#!/usr/bin/env python

from __future__ import division
from numpy import *

class MeshObject:
  def __init__(self):
    self.name = 'mesh'
    self.xmesh = array([])
    self.ymesh = array([])
    self.zmesh = array([])

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
    self.xmesh = cumsum(hstack((0,xmesh_delta)))
  def setYmeshDelta(self,ymesh_delta):
    self.ymesh = cumsum(hstack((0,ymesh_delta)))
  def setZmeshDelta(self,zmesh_delta):
    self.zmesh = cumsum(hstack((0,zmesh_delta)))
  def setMeshDelta(self,xmesh_delta,ymesh_delta,zmesh_delta):
    self.xmesh = cumsum(hstack((0,xmesh_delta)))
    self.ymesh = cumsum(hstack((0,ymesh_delta)))
    self.zmesh = cumsum(hstack((0,zmesh_delta)))
  
  def getXmeshDelta(self):
    return(diff(self.xmesh))
  def getYmeshDelta(self):
    return(diff(self.ymesh))
  def getZmeshDelta(self):
    return(diff(self.zmesh))
  def getMeshDelta(self):
    return(diff(self.xmesh),diff(self.ymesh),diff(self.zmesh))
