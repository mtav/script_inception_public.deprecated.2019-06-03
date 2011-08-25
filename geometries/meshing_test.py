#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *
from numpy import *
from utilities.common import *
from constants.constants import *
from meshing.subGridMultiLayer import *
import os
from geometries.triangular_prism import TriangularPrism
from geometries.SpecialTriangularPrism import SpecialTriangularPrism

pillar = BFDTDobject()

# define box
pillar.box.lower = [0,0,0]
pillar.box.upper = [10,10,10]

# define geometry
prism = Block()
prism.lower = [ 1,1,1 ]
prism.upper = [ 2,2,2 ]
prism.permittivity = 24
pillar.geometry_object_list.append(prism)
pillar.block_list.append(prism)
prism = Block()
prism.lower = [ 3,3,3 ]
prism.upper = [ 4,4,4 ]
prism.permittivity = 42
pillar.geometry_object_list.append(prism)
pillar.block_list.append(prism)

# define mesh
pillar.autoMeshGeometry()

# write
DSTDIR = os.getenv('TESTDIR')
BASENAME = 'meshing_test'
pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
print pillar.getNcells()
