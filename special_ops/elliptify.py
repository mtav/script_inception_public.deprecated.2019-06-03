#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.ellipsoid import *

DSTDIR = sys.argv[1]
if not os.path.isdir(DSTDIR):
  os.mkdir(DSTDIR)

N = 31

Dx = 3.15
Dz = 3
block_direction = 'x'

#Dx = 3
#Dz = 3.15
#block_direction = 'z'

sim=readBristolFDTD('qedc3_2_05.in')

first = True

BASENAME = "ellipsoid.x%.2f.z%.2f" % (Dx,Dz)

for i in range(len(sim.geometry_object_list)):
  obj = sim.geometry_object_list[i]
  if isinstance(obj,Cylinder):
    ellipsoid = Ellipsoid()
    ellipsoid.setCentro(obj.getCentro())
    size = obj.getSize()
    ellipsoid.setSize([Dx,obj.height,Dz])
    ellipsoid.permittivity = obj.permittivity
    ellipsoid.conductivity = obj.conductivity
    ellipsoid.mesh.setSizeAndResolution(ellipsoid.getSize(),[N,N,N])
    ellipsoid.block_direction = block_direction
    sim.geometry_object_list[i] = ellipsoid
    if first:
      first=False
      ref=BFDTDobject()
      ref.box = sim.box
      ref.geometry_object_list.append(obj)
      ref.geometry_object_list.append(ellipsoid)
      ref.writeGeoFile(DSTDIR+os.sep+BASENAME+'.ref.geo')
    #print(id(obj))
    
Lambda = sim.excitation_list[0].getLambda()
# define mesh
a = 10
sim.autoMeshGeometry(Lambda/a)
#MAXCELLS=8000000;
MAXCELLS=1000000;
while(sim.getNcells()>MAXCELLS and a>1):
  a = a-1
  sim.autoMeshGeometry(Lambda/a)

#sim.writeGeoFile('ellipsoid.Yx.geo')
#sim.writeInpFile('ellipsoid.Yx.inp')
sim.fileList = []
print('number of geometry objects = '+str(N*len(sim.geometry_object_list)))
sim.writeAll(DSTDIR,BASENAME)
