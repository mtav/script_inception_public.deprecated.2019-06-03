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
    self.NRodsPerLayer_X = 12
    self.NRodsPerLayer_Y = 12
    self.rod_width = 0.100
    self.rod_height = 0.200
    self.rod_type = 'cylinder'
    self.interLayerDistance = 0.500
    self.interRodDistance = 0.600
    self.offset = array([-5.5,-5.5,0])
    self.initialDirection = 0
    
  def getGWL(self):
    GWL_obj = GWLobject()
    for layer_idx in range(self.Nlayers_Z):
      direction = layer_idx % 2 + self.initialDirection % 2
      if direction % 2 == 0:
        for rod_idx in range(self.NRodsPerLayer_X):
          P1 = self.offset + array([rod_idx*self.interRodDistance,0,layer_idx*self.interLayerDistance])
          P2 = self.offset + array([rod_idx*self.interRodDistance,self.NRodsPerLayer_Y*self.interRodDistance,layer_idx*self.interLayerDistance])
          GWL_obj.addLine(P1,P2)
      else:
        for rod_idx in range(self.NRodsPerLayer_Y):
          P1 = self.offset + array([0,rod_idx*self.interRodDistance,layer_idx*self.interLayerDistance])
          P2 = self.offset + array([self.NRodsPerLayer_X*self.interRodDistance,rod_idx*self.interRodDistance,layer_idx*self.interLayerDistance])
          GWL_obj.addLine(P1,P2)
    return GWL_obj
  
if __name__ == "__main__":
  GWL_obj = GWLobject()
  GWL_obj.readGWL(sys.argv[1])
  print GWL_obj.GWL_voxels
  GWL_obj.write_GWL('copy.gwl')
  woodpile_obj = Woodpile()
  GWL_obj = woodpile_obj.getGWL()
  GWL_obj.write_GWL('woodpile_test.gwl')
  
