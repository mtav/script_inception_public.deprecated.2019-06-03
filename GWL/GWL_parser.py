#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from numpy import *

class GWLobject:
  def __init__(self):
    self.GWL_voxels = []
  
  def addLine(self,P1,P2):
    write_sequence = [P1,P2]
    self.GWL_voxels.append(write_sequence)

  def addWrite(self):
    write_sequence = []
    self.GWL_voxels.append(write_sequence)

  def readGWL(self,filename):
    write_sequence = []
    with open(filename, 'r') as file:
      for line in file:
        #print line
        line_stripped = line.strip()
        # TODO: handle comments and other commands
        if len(line_stripped)>0:
          cmd = re.split('[^a-zA-Z0-9_+-.]+',line_stripped)
          cmd = [ i.lower() for i in cmd ]
          print cmd
          if cmd[0]=='-999' or cmd[0]=='write':
            print 'write'
            self.GWL_voxels.append(write_sequence)
            write_sequence = []
          else:
            print 'voxel'
            voxel = [ float(i) for i in cmd ]
            write_sequence.append(voxel)
    #return GWL_voxels
  
  def write_GWL(self,filename):
    with open(filename, 'w') as file:
      for write_sequence in self.GWL_voxels:
        for voxel in write_sequence:
          file.write(str(voxel[0])+'\t'+str(voxel[1])+'\t'+str(voxel[2])+'\n')
        file.write('-999\t-999\t-999\n')
        
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
    self.offset = array([0,0,0])
    self.initialDirection = 1
    self.initialLayerType_X = 1
    self.initialLayerType_Y = 1
    self.Xmin = -5.5
    self.Xmax = 5.5
    self.Ymin = -5.5
    self.Ymax = 5.5
    
  def getGWL(self):
    GWL_obj = GWLobject()
    layer_type_X = self.initialLayerType_X
    layer_type_Y = self.initialLayerType_Y
    for layer_idx in range(self.Nlayers_Z):
      direction = layer_idx % 2 + self.initialDirection % 2
      if direction % 2 == 0:
        N = self.NRodsPerLayer_X + layer_type_X
        for rod_idx in range(N-1,-1,-1):
          X = -0.5*(N - 1)*self.interRodDistance + rod_idx*self.interRodDistance
          P1 = self.offset + array([X,self.Ymax,layer_idx*self.interLayerDistance])
          P2 = self.offset + array([X,self.Ymin,layer_idx*self.interLayerDistance])
          GWL_obj.addLine(P1,P2)
        layer_type_X = (layer_type_X + 1) % 2
      else:
        N = self.NRodsPerLayer_Y+layer_type_Y
        for rod_idx in range(N):
          Y = -0.5*(N - 1)*self.interRodDistance + rod_idx*self.interRodDistance
          P1 = self.offset + array([self.Xmin,Y,layer_idx*self.interLayerDistance])
          P2 = self.offset + array([self.Xmax,Y,layer_idx*self.interLayerDistance])
          GWL_obj.addLine(P1,P2)
        layer_type_Y = (layer_type_Y + 1) % 2
      if layer_idx<self.Nlayers_Z-1:
        GWL_obj.addWrite()
    return GWL_obj
  
if __name__ == "__main__":
  GWL_obj = GWLobject()
  GWL_obj.readGWL(sys.argv[1])
  print GWL_obj.GWL_voxels
  GWL_obj.write_GWL('copy.gwl')
  woodpile_obj = Woodpile()
  GWL_obj = woodpile_obj.getGWL()
  GWL_obj.write_GWL('woodpile_test.gwl')
  
