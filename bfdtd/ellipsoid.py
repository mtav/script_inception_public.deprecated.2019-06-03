#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *

class Ellipsoid(Block):
  def __init__(self, name=None, layer=None, group=None, block_direction=None, non_elliptical_directions=None):
    if name is None: name = 'ellipsoid'
    if layer is None: layer = 'ellipsoid'
    if group is None: group = 'ellipsoid'
    if block_direction is None: block_direction = 'x'
    if non_elliptical_directions is None: non_elliptical_directions = [False, False, False]
  
    Block.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    
    # mesh used to discretize the ellipsoid into blocks
    self.mesh = MeshObject()
    self.mesh.setSizeAndResolution(self.getSize(),[10,10,10])
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += Geometry_object.__str__(self)
    return ret
        
  def write_entry(self, FILE):
    C = self.getCentro()
    L = self.lower
    size = self.getSize()
    centre_x = self.mesh.getYmeshCentres()
    centre_y = self.mesh.getYmeshCentres()
    centre_z = self.mesh.getZmeshCentres()
    delta_x = size[0]
    delta_y = self.mesh.getYmeshDelta()
    delta_z = self.mesh.getZmeshDelta()
    a = 0.5*size[0]
    b = 0.5*size[1]
    c = 0.5*size[2]
    for j in range(len(centre_y)):
      for k in range(len(centre_z)):
        
        y = -b+centre_y[j]
        #print(1-pow((y/b),2))
        dimX = 2*a*numpy.sqrt(1-pow((y/b),2))
        
        block = Block()
        block.name = "%s.j%d.k%d" % (self.name,j,k)
        block.setCentro([C[0],L[1]+centre_y[j],L[2]+centre_z[k]])
        block.setSize([dimX, delta_y[j], delta_z[k]])
        block.write_entry(FILE)
    return

# for testing
if __name__ == "__main__":
  sim = BFDTDobject()
  C = numpy.array([1,2,3])
  
  block = Block()
  block.setSize(C)
  block.setCentro(0.5*C)
  sim.geometry_object_list.append(block)

  ellipsoid = Ellipsoid()
  ellipsoid.setCentro(block.getCentro())
  ellipsoid.setSize(block.getSize())
  ellipsoid.mesh.setSizeAndResolution(ellipsoid.getSize(),[10,10,10])
  sim.geometry_object_list.append(ellipsoid)
  
  sim.writeGeoFile(sys.argv[1])
