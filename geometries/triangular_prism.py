#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from bfdtd.bfdtd_parser import *

class TriangularPrism(Geometry_object):
  def __init__(self,
    name = 'triangularprism',
    layer = 'triangularprism',
    group = 'triangularprism',
    lower = [0,0,0],
    upper = [1,1,1],
    permittivity = 1,# vacuum by default
    conductivity = 0,
    Nvoxels = 10,
    orientation = [0,1,2]):
    
    Geometry_object.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
    self.permittivity = permittivity
    self.conductivity = conductivity
    self.Nvoxels = Nvoxels
    self.orientation = orientation
    self.COMMENT = 'nada'
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += 'Nvoxels = '+str(self.Nvoxels)+'\n'
    ret += 'orientation = '+str(self.orientation)+'\n'
    ret += Geometry_object.__str__(self)
    return ret
    
  #def read_entry(self,entry):
    #if entry.name:
      #self.name = entry.name
    #self.lower = float_array(entry.data[0:3])
    #self.upper = float_array(entry.data[3:6])
    #self.permittivity = float(entry.data[6])
    #self.conductivity = float(entry.data[7])
    
  def getVoxels(self):
    voxel_list = []
    # Z = triangle peak
    # X = triangle size
    # Y = prism length
    ####################################
    voxel_Ymin = self.lower[1]#self.Ymax/2.0 - self.radius_Y_pillar_mum
    voxel_Ymax = self.upper[1]#self.Ymax/2.0 + self.radius_Y_pillar_mum
    D = self.upper[2]-self.lower[2]#self.radius_Z_pillar_mum - self.radius_Z_hole
    R = 0.5*(self.upper[0]-self.lower[0])
    N = self.Nvoxels
    voxel_radius_X = R/( 2.*self.Nvoxels + 1.)
    Z_left = self.lower[2] #self.Zmax/2.0 - self.radius_Z_pillar_mum
    offset = self.lower[0] #X_current - self.radius_X_hole
    for i in range(self.Nvoxels):
      # bottom left blocks
      L = [ offset+2*R*(i)/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
      U = [ offset+2*R*(i + 1)/(2*N+1), voxel_Ymax, Z_left+D*(i + 1.)/(N+1.)]
      print L, U, offset, R, i, 2*N+1, D, Z_left, i+1, N+1,(i + 1)/(N+1)
      LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
      UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
      voxel_list.append(Block(name=self.COMMENT, lower=LL, upper=UU, permittivity=self.permittivity, conductivity=self.conductivity))
      # top left blocks
      L = [ offset+2*R*((2*N+1)-(i))/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
      U = [ offset+2*R*((2*N+1)-(i + 1))/(2*N+1), voxel_Ymax, Z_left+D*(i + 1)/(N+1)]
      LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
      UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
      voxel_list.append(Block(name=self.COMMENT, lower=LL, upper=UU, permittivity=self.permittivity, conductivity=self.conductivity))
    ## middle left block
    L = [ offset+2*R*(N)/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
    U = [ offset+2*R*(N + 1)/(2*N+1), voxel_Ymax, Z_left+D*(N + 1)/(N+1)]# - self.radius_Z_pillar_mum + D]
    LL = [ L[self.orientation[0]],L[self.orientation[1]],L[self.orientation[2]] ]
    UU = [ U[self.orientation[0]],U[self.orientation[1]],U[self.orientation[2]] ]
    voxel_list.append(Block(name=self.COMMENT, lower=LL, upper=UU, permittivity=self.permittivity, conductivity=self.conductivity))
    ####################################
    return voxel_list
        
  def write_entry(self, FILE):
    voxels = self.getVoxels()
    for v in voxels:
      v.lower, v.upper = fixLowerUpper(v.lower, v.upper)
      FILE.write('BLOCK **name='+v.name+'\n')
      FILE.write('{\n')
      FILE.write("%E **XL\n" % v.lower[0])
      FILE.write("%E **YL\n" % v.lower[1])
      FILE.write("%E **ZL\n" % v.lower[2])
      FILE.write("%E **XU\n" % v.upper[0])
      FILE.write("%E **YU\n" % v.upper[1])
      FILE.write("%E **ZU\n" % v.upper[2])
      FILE.write("%E **relative Permittivity\n" % v.permittivity)
      FILE.write("%E **Conductivity\n" % v.conductivity)
      FILE.write('}\n')
      FILE.write('\n')
    
  def getCenter(self):
    return [ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ]

if __name__ == "__main__":
  foo = TriangularPrism()
  foo.getVoxels()
  #foo.write_entry()
