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
  
def ExcitationWrapper(centre,size,plane_direction,type,excitation_direction,frequency,template_filename='template.dat'):
  plane_direction_vector,plane_direction_alpha = getVecAlphaDirectionFromVar(plane_direction)
  excitation = Excitation()
  excitation.frequency = frequency
  excitation.E = excitation_direction
  excitation.template_filename = template_filename
  excitation.template_source_plane = plane_direction_alpha
  excitation.template_target_plane = plane_direction_alpha
  excitation.template_direction = 1
  excitation.template_rotation = 1
  if type=='1D':
    excitation.current_source = 7
    excitation.setExtension(centre,centre + size*array(excitation_direction))
  else:
    excitation.current_source = 11
    diagonal = (array(plane_direction_vector)^array([1,1,1]))
    excitation.setExtension(centre - size*diagonal, centre + size*diagonal)
  return(excitation)

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
template_radius = prism.getInscribedSquarePlaneRadius(P_centre)
print('template_radius = ',template_radius)
#template_radius = 0.0307

#(A1_global,B1_global,C1_global,A2_global,B2_global,C2_global) = prism.getGlobalEnvelopPoints()
envelop = prism.getGlobalEnvelopPoints()

# define probes
probe = Probe(position = P_centre)
pillar.probe_list.append(probe)
for i in envelop:
  print(i)
  probe = Probe(position = i)
  pillar.probe_list.append(probe)

# excitations
excitation = ExcitationWrapper(centre=P_centre,size=template_radius,plane_direction='x',type='1D',excitation_direction=[0,0,1],frequency=123)
pillar.excitation_list.append(excitation)
excitation = ExcitationWrapper(centre=P_centre,size=template_radius,plane_direction='x',type='1D',excitation_direction=[0,1,0],frequency=123)
pillar.excitation_list.append(excitation)
excitation = ExcitationWrapper(centre=P_centre,size=template_radius,plane_direction='x',type='2D',excitation_direction=[0,0,1],frequency=123)
pillar.excitation_list.append(excitation)
  
# write
DSTDIR = os.getenv('TESTDIR')
BASENAME = 'prismtest'
pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
