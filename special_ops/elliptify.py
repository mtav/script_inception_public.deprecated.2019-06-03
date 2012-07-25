#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bfdtd.ellipsoid import *

Nz = 31

sim=readBristolFDTD('qedc3_2_05.in')
for i in range(len(sim.geometry_object_list)):
  obj = sim.geometry_object_list[i]
  if isinstance(obj,Cylinder):
    ellipsoid = Ellipsoid()
    ellipsoid.setCentro(obj.getCentro())
    size = obj.getSize()
    ellipsoid.setSize([3,obj.height,3.15])
    ellipsoid.permittivity = obj.permittivity
    ellipsoid.conductivity = obj.conductivity
    ellipsoid.mesh.setSizeAndResolution(ellipsoid.getSize(),[1,1,Nz])
    sim.geometry_object_list[i] = ellipsoid
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

BASENAME = 'ellipsoid'
DSTDIR = sys.argv[1]
if not os.path.isdir(DSTDIR):
  os.mkdir(DSTDIR)

#sim.writeGeoFile('ellipsoid.Yx.geo')
#sim.writeInpFile('ellipsoid.Yx.inp')
sim.fileList = []
print('number of geometry objects = '+str(Nz*len(sim.geometry_object_list)))
sim.writeAll(DSTDIR,BASENAME)
