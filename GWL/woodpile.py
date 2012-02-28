#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from GWL.GWL_parser import *

class Woodpile:
  def __init__(self):
    self.Nlayers_Z = 12
    self.NRodsPerLayer_X = 17
    self.NRodsPerLayer_Y = 17
    self.rod_width = 0.100
    self.rod_height = 0.200
    self.rod_type = 'cylinder'
    self.interLayerDistance = 0.212
    self.interRodDistance = 0.600
    self.offset = numpy.array([0,0,0])
    self.initialDirection = 1
    self.initialLayerType_X = 1
    self.initialLayerType_Y = 1
    self.Xmin = -5.5
    self.Xmax = 5.5
    self.Ymin = -5.5
    self.Ymax = 5.5
    self.BottomToTop = 0 # 1=write from bottom to top, 0=write from top to bottom

  def adaptXYMinMax(self):
    self.Xmin = -0.5*(self.NRodsPerLayer_X+1)*self.interRodDistance+0.1
    self.Xmax = 0.5*(self.NRodsPerLayer_X+1)*self.interRodDistance+0.1
    self.Ymin = -0.5*(self.NRodsPerLayer_Y+1)*self.interRodDistance+0.1
    self.Ymax = 0.5*(self.NRodsPerLayer_Y+1)*self.interRodDistance+0.1
    
  def getGWL(self):
    GWL_obj = GWLobject()
    layer_type_X = self.initialLayerType_X
    layer_type_Y = self.initialLayerType_Y

    if self.BottomToTop == 1:
        layer_idx_list = range(self.Nlayers_Z)
    else:
        layer_idx_list = range(self.Nlayers_Z-1,-1,-1)
        layer_type_X = (layer_type_X + 1) % 2
        layer_type_Y = (layer_type_Y + 1) % 2

    for layer_idx in layer_idx_list:
      direction = layer_idx % 2 + self.initialDirection % 2
      if direction % 2 == 0:
        N = self.NRodsPerLayer_X + layer_type_X
        for rod_idx in range(N-1,-1,-1):
          X = -0.5*(N - 1)*self.interRodDistance + rod_idx*self.interRodDistance
          P1 = self.offset + numpy.array([X,self.Ymax,layer_idx*self.interLayerDistance])
          P2 = self.offset + numpy.array([X,self.Ymin,layer_idx*self.interLayerDistance])
          GWL_obj.addLine(P1,P2)
        layer_type_X = (layer_type_X + 1) % 2
      else:
        N = self.NRodsPerLayer_Y+layer_type_Y
        for rod_idx in range(N):
          Y = -0.5*(N - 1)*self.interRodDistance + rod_idx*self.interRodDistance
          P1 = self.offset + numpy.array([self.Xmin,Y,layer_idx*self.interLayerDistance])
          P2 = self.offset + numpy.array([self.Xmax,Y,layer_idx*self.interLayerDistance])
          GWL_obj.addLine(P1,P2)
        layer_type_Y = (layer_type_Y + 1) % 2
      if layer_idx<self.Nlayers_Z-1:
        GWL_obj.addWrite()
    return GWL_obj
  
  def write_GWL(self,filename):
    GWL_obj = self.getGWL()
    GWL_obj.write_GWL(filename)

if __name__ == "__main__":
  woodpile_obj = Woodpile()
  woodpile_obj.write_GWL('woodpile_test.gwl')
