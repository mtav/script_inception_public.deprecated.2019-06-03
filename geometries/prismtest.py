#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *
from numpy import *
from utilities.common import *
from constants.constants import *
from meshing.subGridMultiLayer import *
import os
from bfdtd.triangular_prism import TriangularPrism
from bfdtd.SpecialTriangularPrism import SpecialTriangularPrism
from bfdtd.excitationTemplate import *
  
pillar = BFDTDobject()

## define geometry
offset = array([1,2,3])
prism = SpecialTriangularPrism()
prism.lower = offset+array([ 0,0,0 ])
prism.upper = offset+array([ 5,1,2 ])
prism.orientation = [2,0,1]
prism.permittivity = pow(2.4,2)
prism.conductivity = 0
prism.NvoxelsX = 30
prism.NvoxelsY = 30
prism.NvoxelsZ = 30
pillar.geometry_object_list.append(prism)

# define excitation
P_centre = prism.getGeoCentre()
#template_radius = prism.getInscribedSquarePlaneRadius(P_centre)
#print('template_radius = ',template_radius)
template_radius = 0.0307

#(A1_global,B1_global,C1_global,A2_global,B2_global,C2_global) = prism.getGlobalEnvelopPoints()
envelop = prism.getGlobalEnvelopPoints()

# define probes
probe = Probe(position = P_centre)
pillar.probe_list.append(probe)
for i in envelop:
  print(i)
  probe = Probe(position = i)
  pillar.probe_list.append(probe)
  
# write
DSTDIR = os.getenv('TESTDIR')
BASENAME = 'prismtest'
pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
