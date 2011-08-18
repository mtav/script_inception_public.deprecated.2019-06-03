#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += Geometry_object.__str__(self)
    self.Nvoxels = Nvoxels
    self.orientation = orientation
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.lower = float_array(entry.data[0:3])
    self.upper = float_array(entry.data[3:6])
    self.permittivity = float(entry.data[6])
    self.conductivity = float(entry.data[7])
  def write_entry(self, FILE):
    self.lower, self.upper = fixLowerUpper(self.lower, self.upper)
    FILE.write('BLOCK **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XL\n" % self.lower[0])
    FILE.write("%E **YL\n" % self.lower[1])
    FILE.write("%E **ZL\n" % self.lower[2])
    FILE.write("%E **XU\n" % self.upper[0])
    FILE.write("%E **YU\n" % self.upper[1])
    FILE.write("%E **ZU\n" % self.upper[2])
    FILE.write("%E **relative Permittivity\n" % self.permittivity)
    FILE.write("%E **Conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')
  def getCenter(self):
    return [ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ]

if __name__ == "__main__":
  foo = TriangularPrism()

####################################
voxel_Ymin = self.Ymax/2.0 - self.radius_Y_pillar_mum
voxel_Ymax = self.Ymax/2.0 + self.radius_Y_pillar_mum
voxel_radius_X = self.radius_X_hole/( 2.*self.Nvoxels + 1.)
D = self.radius_Z_pillar_mum - self.radius_Z_hole
R = self.radius_X_hole
N = self.Nvoxels
Z_left = self.Zmax/2.0 - self.radius_Z_pillar_mum
Z_right = self.Zmax/2.0 + self.radius_Z_pillar_mum
offset = X_current - self.radius_X_hole
for i in range(self.Nvoxels):
  # bottom left blocks
  lower = [ offset+2*R*(i)/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
  upper = [ offset+2*R*(i + 1)/(2*N+1), voxel_Ymax, Z_left+D*(i + 1)/(N+1)]
  self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
  # top left blocks
  lower = [ offset+2*R*((2*N+1)-(i))/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
  upper = [ offset+2*R*((2*N+1)-(i + 1))/(2*N+1), voxel_Ymax, Z_left+D*(i + 1)/(N+1)]
  self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
  # bottom right blocks
  lower = [ offset+2*R*(i)/(2*N+1), voxel_Ymin, Z_right-D*(0)/(N+1)]
  upper = [ offset+2*R*(i + 1)/(2*N+1), voxel_Ymax, Z_right-D*(i + 1)/(N+1)]
  self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
  # top right blocks
  lower = [ offset+2*R*((2*N+1)-(i))/(2*N+1), voxel_Ymin, Z_right-D*(0)/(N+1)]
  upper = [ offset+2*R*((2*N+1)-(i + 1))/(2*N+1), voxel_Ymax, Z_right-D*(i + 1)/(N+1)]
  self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
## middle left block
lower = [ offset+2*R*(N)/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
upper = [ offset+2*R*(N + 1)/(2*N+1), voxel_Ymax, Z_left+D*(N + 1)/(N+1)]# - self.radius_Z_pillar_mum + D]
self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
## middle right block
lower = [ offset+2*R*(N)/(2*N+1), voxel_Ymin, Z_right-D*(0)/(N+1)]
upper = [ offset+2*R*(N + 1)/(2*N+1), voxel_Ymax, Z_right-D*(N + 1)/(N+1)]# - self.radius_Z_pillar_mum + D]
self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
####################################
