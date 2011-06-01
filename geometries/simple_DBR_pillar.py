#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *
from numpy import *
from utilities.common import *
from constants.constants import *
from meshing.subGridMultiLayer import *
import os

pillar = BFDTDobject()

#########
# constants
#########
n_air = 1
n_diamond = 2.4
Lambda_mum = 0.637
delta = Lambda_mum/(10*n_diamond)
freq = get_c0()/Lambda_mum
k=1
radius = k*Lambda_mum/(4*n_diamond)
Nbottom = 40
Ntop = 20
h_air = Lambda_mum/(4*n_air)
h_diamond = Lambda_mum/(4*n_diamond)
h_cavity = Lambda_mum/(n_diamond)
height = Nbottom*(h_air+h_diamond) + h_cavity + Ntop*(h_air+h_diamond)

#########
# define box
#########
pillar.box.lower = [0,0,0]
pillar.box.upper = [height+2,2*(radius+1),2*(radius+1)]

#########
# define geometry
#########
Ymin=pillar.box.getCenter()[1]-radius
Ymax=pillar.box.getCenter()[1]+radius
Zmin=pillar.box.getCenter()[2]-radius
Zmax=pillar.box.getCenter()[2]+radius

X_current = 1

for i in range(Nbottom):
  block = Block(lower = [ X_current, Ymin, Zmin ], upper = [ X_current+h_diamond, Ymax, Zmax ], permittivity = pow(n_diamond,2), conductivity = 0)
  pillar.geometry_object_list.append(block)
  X_current = X_current+h_diamond
  block = Block(lower = [ X_current, Ymin, Zmin ], upper = [ X_current+h_air, Ymax, Zmax ], permittivity = pow(n_air,2), conductivity = 0)
  pillar.geometry_object_list.append(block)
  X_current = X_current+h_air

block = Block(lower = [ X_current, Ymin, Zmin ], upper = [ X_current+h_cavity, Ymax, Zmax ], permittivity = pow(n_diamond,2), conductivity = 0)
pillar.geometry_object_list.append(block)
X_current = X_current+h_cavity

for i in range(Ntop):
  block = Block(lower = [ X_current, Ymin, Zmin ], upper = [ X_current+h_air, Ymax, Zmax ], permittivity = pow(n_air,2), conductivity = 0)
  pillar.geometry_object_list.append(block)
  X_current = X_current+h_air
  block = Block(lower = [ X_current, Ymin, Zmin ], upper = [ X_current+h_diamond, Ymax, Zmax ], permittivity = pow(n_diamond,2), conductivity = 0)
  pillar.geometry_object_list.append(block)
  X_current = X_current+h_diamond

#########
# define flag
#########
pillar.flag.iterations = 25000

#########
# define excitation
#########
excitation = Excitation()
excitation.P1 = [ block.getCenter()[0], block.getCenter()[1]-1*delta, block.getCenter()[2] ]
excitation.P2 = block.getCenter()
excitation.frequency = freq
excitation.E = list(Unit(subtract(excitation.P2,excitation.P1)))
pillar.excitation_list = [ excitation ]

#########
# define probe
#########
probe = Probe(position = [ block.upper[0]+delta, block.getCenter()[1], block.getCenter()[2] ])
pillar.probe_list = [ probe ]

#########
# define frequency snapshots
#########
first = min(65400,pillar.flag.iterations)
frequency_vector = [freq]
F = pillar.addFrequencySnapshot(1,block.getCenter()[0]); F.first = first; F.frequency_vector = frequency_vector
F = pillar.addFrequencySnapshot(2,block.getCenter()[1]); F.first = first; F.frequency_vector = frequency_vector
F = pillar.addFrequencySnapshot(3,block.getCenter()[2]); F.first = first; F.frequency_vector = frequency_vector
F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector

#########
# define mesh
#########
#max_delta_Vector_X = [ delta, delta, delta, delta ]
#max_delta_Vector_Y = [ delta, delta, delta, delta, delta, delta ]
#max_delta_Vector_Z = [ delta, delta, delta, delta ]
#thicknessVector_X = LimitsToThickness([ pillar.box.lower[0], block.lower[0], block.upper[0], block.upper[0]+delta, pillar.box.upper[0] ])
#thicknessVector_Y = [ block.lower[1]-pillar.box.lower[1], (block.getCenter()[1]-delta)-block.lower[1], delta, delta, block.upper[1]-(block.getCenter()[1]+delta), pillar.box.upper[1]-block.upper[1] ]
#thicknessVector_Z = LimitsToThickness([ pillar.box.lower[2], block.lower[2], block.getCenter()[2], block.upper[2], pillar.box.upper[2] ])
#pillar.delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X,thicknessVector_X)
#pillar.delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y,thicknessVector_Y)
#pillar.delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z,thicknessVector_Z)

#########
# write
#########
#DSTDIR = os.getenv('DATADIR')
DSTDIR = os.getenv('TESTDIR')
BASENAME = 'simple_DBR_pillar'
pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
print pillar.getNcells()
