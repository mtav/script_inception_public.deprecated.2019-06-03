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

# constants
n_air = 1; n_diamond = 2.4
Lambda_mum = 0.637
delta = Lambda_mum/(10*n_diamond)
freq = get_c0()/Lambda_mum
k=1; radius = k*Lambda_mum/(4*n_diamond)
Nbottom = 30; Ntop = 30
h_air = Lambda_mum/(4*n_air)
h_diamond = Lambda_mum/(4*n_diamond)
h_cavity = Lambda_mum/(n_diamond)
height = Nbottom*(h_air+h_diamond) + h_cavity + Ntop*(h_air+h_diamond)
buffer = 0.25
FullBox_upper = [ height+2*buffer, 2*(radius+buffer), 2*(radius+buffer) ]
P_centre = [ buffer + Nbottom*(h_air+h_diamond) + 0.5*h_cavity, 0.5*FullBox_upper[1], 0.5*FullBox_upper[2] ]

# define flag
pillar.flag.iterations = 100000

# define boundary conditions
pillar.boundaries.Xpos_bc = 2
pillar.boundaries.Ypos_bc = 1 #2
pillar.boundaries.Zpos_bc = 2

# define box
pillar.box.lower = [0,0,0]
if pillar.boundaries.Ypos_bc == 2:
  pillar.box.upper = FullBox_upper
else:
  pillar.box.upper = [ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ]

## define geometry
#prism = TriangularPrism()
##prism = SpecialTriangularPrism()
#prism.lower = [ P_centre[0]-0.5*height, P_centre[1]-radius, P_centre[2]-radius ]
#prism.upper = [ P_centre[0]+0.5*height, P_centre[1]+radius, P_centre[2]+radius ]
##prism.lower = [1,1,1]
##prism.upper = [1,10,1]
##prism.lower = [1,2,3]
##prism.upper = [3,7,13]
#prism.orientation = [2,0,1]
##prism.orientation = [2,1,0]
#prism.permittivity = pow(n_diamond,2)
#prism.conductivity = 0
#pillar.geometry_object_list.append(prism)

#prism = TriangularPrism()
prism = SpecialTriangularPrism()
prism.lower = [ P_centre[0]-0.5*height, P_centre[1]-radius, P_centre[2]-radius ]
prism.upper = [ P_centre[0]+0.5*height, P_centre[1]+radius, P_centre[2]+radius ]
#prism.lower = [1,1,1]
#prism.upper = [1,10,1]
#prism.lower = [1,2,3]
#prism.upper = [3,7,13]
prism.orientation = [2,0,1]
#prism.orientation = [2,1,0]
prism.permittivity = pow(n_diamond,2)
prism.conductivity = 0
prism.NvoxelsX = 30
prism.NvoxelsY = 30
prism.NvoxelsZ = 30
pillar.geometry_object_list.append(prism)

L = [1,2,3]
U = numpy.add(L,[1,2,3])

#prism = SpecialTriangularPrism()
#prism.lower = L
#prism.upper = U
#prism.orientation = [0,1,2]
#prism.permittivity = pow(n_diamond,2)
#prism.conductivity = 0
#print 'center = ',prism.getCenter()
#pillar.geometry_object_list.append(prism)

#prism = SpecialTriangularPrism()
#prism.lower = L
#prism.upper = U
#prism.orientation = [0,2,1]
#prism.permittivity = pow(n_diamond,2)
#prism.conductivity = 0
#print 'center = ',prism.getCenter()
#pillar.geometry_object_list.append(prism)

#prism = SpecialTriangularPrism()
#prism.lower = L
#prism.upper = U
#prism.orientation = [1,0,2]# -> 3,2,4
#prism.permittivity = pow(n_diamond,2)
#prism.conductivity = 0
#print 'center = ',prism.getCenter()
#pillar.geometry_object_list.append(prism)

#prism = SpecialTriangularPrism()
#prism.lower = L
#prism.upper = U
#prism.orientation = [1,2,0]# -> 3,4,0
#prism.permittivity = pow(n_diamond,2)
#prism.conductivity = 0
#print 'center = ',prism.getCenter()
#pillar.geometry_object_list.append(prism)

#prism = SpecialTriangularPrism()
#prism.lower = L
#prism.upper = U
#prism.orientation = [2,0,1]
#prism.permittivity = pow(n_diamond,2)
#prism.conductivity = 0
#print 'center = ',prism.getCenter()
#pillar.geometry_object_list.append(prism)

#prism = SpecialTriangularPrism()
#prism.lower = L
#prism.upper = U
#prism.orientation = [2,1,0]
#prism.permittivity = pow(n_diamond,2)
#prism.conductivity = 0
#print 'center = ',prism.getCenter()
#pillar.geometry_object_list.append(prism)

# define excitation
P_centre = prism.getCenter()
excitation = Excitation()

excitation.current_source = 11

excitation.P1 = [ P_centre[0], P_centre[1]-1*delta, P_centre[2] ]
excitation.P2 = P_centre
excitation.frequency = freq
excitation.E = list(Unit(subtract(excitation.P2,excitation.P1)))

excitation.template_filename = 'template.dat'
excitation.template_source_plane = 'y'
excitation.template_target_plane = 'z'
excitation.template_direction = 0
excitation.template_rotation = 0

pillar.excitation_list = [ excitation ]

# create template
x_min = 0.0
x_max = 4.00
y_min = 0.0
y_max = 4.00
step_x = 2.00e-2
step_y = 2.00e-1
x_list = arange(x_min,x_max,step_x)
y_list = arange(y_min,y_max,step_y)

out_col_name = 'Exre'
column_titles = ['x','z','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']

template1 = ExcitationGaussian1(amplitude = 1, beam_centre_x = 2.1732, beam_centre_y = 2.00, sigma_x = 0.1, sigma_y = 0.9)
pillar.excitation_template_list.append(template1)
#template1.writeDatFile('template1.dat',x_list,y_list, out_col_name, column_titles)
template2 = ExcitationGaussian2(amplitude = 1, beam_centre_x = 2.1732, beam_centre_y = 2.00, c = 0.5, sigma = 0.5)
pillar.excitation_template_list.append(template2)
#template2.writeDatFile('template2.dat',x_list,y_list, out_col_name, column_titles)

# define probe
if pillar.boundaries.Ypos_bc == 2:
  probe = Probe(position = [ buffer+height+delta, P_centre[1], P_centre[2] ])
else:
  probe = Probe(position = [ buffer+height+delta, P_centre[1]-delta, P_centre[2] ])
pillar.probe_list = [ probe ]

# define frequency snapshots
first = min(65400,pillar.flag.iterations)
frequency_vector = [freq]
F = pillar.addFrequencySnapshot(1,P_centre[0]); F.first = first; F.frequency_vector = frequency_vector
if pillar.boundaries.Ypos_bc == 2:
  F = pillar.addFrequencySnapshot(2,P_centre[1]); F.first = first; F.frequency_vector = frequency_vector
else:
  F = pillar.addFrequencySnapshot(2,P_centre[1]-delta); F.first = first; F.frequency_vector = frequency_vector
F = pillar.addFrequencySnapshot(3,P_centre[2]); F.first = first; F.frequency_vector = frequency_vector
F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector

## define mesh
#thicknessVector_X = [ prism.lower[0]-pillar.box.lower[0], P_centre[0]-prism.lower[0], prism.upper[0]-P_centre[0], delta, pillar.box.upper[0]-(prism.upper[0]+delta) ]
#if pillar.boundaries.Ypos_bc == 2:
  #thicknessVector_Y = [ prism.lower[1]-pillar.box.lower[1], (P_centre[1]-delta)-prism.lower[1], delta, delta, prism.upper[1]-(P_centre[1]+delta), pillar.box.upper[1]-prism.upper[1] ]
#else:
  #thicknessVector_Y = [ prism.lower[1]-pillar.box.lower[1], (P_centre[1]-delta)-prism.lower[1], delta ]
#thicknessVector_Z = LimitsToThickness([ pillar.box.lower[2], prism.lower[2], P_centre[2], prism.upper[2], pillar.box.upper[2] ])
#max_delta_Vector_X = [ delta ]*len(thicknessVector_X)
#max_delta_Vector_Y = [ delta ]*len(thicknessVector_Y)
#max_delta_Vector_Z = [ delta ]*len(thicknessVector_Z)
#pillar.delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X, thicknessVector_X)
#pillar.delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y, thicknessVector_Y)
#pillar.delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z, thicknessVector_Z)

pillar.autoMeshGeometry(0.1*0.637/16)

# write
#DSTDIR = os.getenv('DATADIR')
#DSTDIR = os.getenv('TESTDIR')
DSTDIR = os.getenv('TESTDIR')
BASENAME = 'triangle_pillar'
pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
print pillar.getNcells()
