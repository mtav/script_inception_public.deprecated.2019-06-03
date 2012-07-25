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
    self.block_direction = block_direction
    self.non_elliptical_directions = non_elliptical_directions
    
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
    centre_x = self.mesh.getXmeshCentres()
    centre_y = self.mesh.getYmeshCentres()
    centre_z = self.mesh.getZmeshCentres()
    delta_x = self.mesh.getXmeshDelta()
    delta_y = self.mesh.getYmeshDelta()
    delta_z = self.mesh.getZmeshDelta()
    a = 0.5*size[0]
    b = 0.5*size[1]
    c = 0.5*size[2]
    
    if self.block_direction=='x' and self.non_elliptical_directions==[False, False, True]:
      for j in range(len(centre_y)):
        y = -b+centre_y[j]
        dimX = 2*a*numpy.sqrt(1-pow((y/b),2))
        block = Block()
        block.name = "%s.Zx.j%d" % (self.name,j)
        block.setCentro([C[0],L[1]+centre_y[j],C[2]])
        block.setSize([dimX, delta_y[j], size[2]])
        block.write_entry(FILE)
    elif self.block_direction=='y' and self.non_elliptical_directions==[False, False, True]:
      for i in range(len(centre_x)):
        x = -a+centre_x[i]
        dimY = 2*b*numpy.sqrt(1-pow((x/a),2))
        block = Block()
        block.name = "%s.Zy.i%d" % (self.name,i)
        block.setCentro([L[0]+centre_x[i],C[1],C[2]])
        block.setSize([delta_x[i], dimY, size[2]])
        block.write_entry(FILE)
    elif self.block_direction=='x' and self.non_elliptical_directions==[False, True, False]:
      for k in range(len(centre_z)):
        z = -c+centre_z[k]
        dimX = 2*a*numpy.sqrt(1-pow((z/c),2))
        block = Block()
        block.name = "%s.Yx.k%d" % (self.name,k)
        block.setCentro([C[0],C[1],L[2]+centre_z[k]])
        block.setSize([dimX, size[1], delta_z[k]])
        block.write_entry(FILE)
    elif self.block_direction=='z' and self.non_elliptical_directions==[False, True, False]:
      for i in range(len(centre_x)):
        x = -a+centre_x[i]
        dimZ = 2*c*numpy.sqrt(1-pow((x/a),2))
        block = Block()
        block.name = "%s.Yz.i%d" % (self.name,i)
        block.setCentro([L[0]+centre_x[i],C[1],C[2]])
        block.setSize([delta_x[i], size[1], dimZ])
        block.write_entry(FILE)
    elif self.block_direction=='y' and self.non_elliptical_directions==[True, False, False]:
      for k in range(len(centre_z)):
        z = -c+centre_z[k]
        dimY = 2*b*numpy.sqrt(1-pow((z/c),2))
        block = Block()
        block.name = "%s.Xy.k%d" % (self.name,k)
        block.setCentro([C[0],C[1],L[2]+centre_z[k]])
        block.setSize([size[0], dimY, delta_z[k]])
        block.write_entry(FILE)
    elif self.block_direction=='z' and self.non_elliptical_directions==[True, False, False]:
      for j in range(len(centre_y)):
        y = -b+centre_y[j]
        dimZ = 2*c*numpy.sqrt(1-pow((y/b),2))
        block = Block()
        block.name = "%s.Xz.j%d" % (self.name,j)
        block.setCentro([C[0],L[1]+centre_y[j],C[2]])
        block.setSize([size[0], delta_y[j], dimZ])
        block.write_entry(FILE)
    else:
      print('FATAL ERROR: not supported yet', file=sys.stderr)
      sys.exit(-1)
      
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

  ellipsoid.non_elliptical_directions = [True, False, False]
  ellipsoid.block_direction = 'y'
  sim.writeGeoFile('ellipsoid.Xy.geo')
  ellipsoid.block_direction = 'z'
  sim.writeGeoFile('ellipsoid.Xz.geo')

  ellipsoid.non_elliptical_directions = [False, True, False]
  ellipsoid.block_direction = 'z'
  sim.writeGeoFile('ellipsoid.Yz.geo')
  ellipsoid.block_direction = 'x'
  sim.writeGeoFile('ellipsoid.Yx.geo')

  ellipsoid.non_elliptical_directions = [False, False, True]
  ellipsoid.block_direction = 'x'
  sim.writeGeoFile('ellipsoid.Zx.geo')
  ellipsoid.block_direction = 'y'
  sim.writeGeoFile('ellipsoid.Zy.geo')
