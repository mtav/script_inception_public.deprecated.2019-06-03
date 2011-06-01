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
n_Diamond = 2.4
Lambda_mum = 0.637
delta = Lambda_mum/(16*n_Diamond)
freq = get_c0()/Lambda_mum
radius = 0.25
height = 2.*40.*Lambda_mum/(2.*n_Diamond) + Lambda_mum/n_Diamond

#########
# define box
#########
pillar.box.lower = [0,0,0]
pillar.box.upper = [height+2*radius,4*radius,4*radius]

#########
# define block
#########
block = Block()
block.lower = [ pillar.box.getCenter()[0]-0.5*height, pillar.box.getCenter()[1]-radius, pillar.box.getCenter()[2]-radius ]
block.upper = [ pillar.box.getCenter()[0]+0.5*height, pillar.box.getCenter()[1]+radius, pillar.box.getCenter()[2]+radius ]
block.permittivity = pow(n_Diamond,2)
block.conductivity = 0

pillar.geometry_object_list = [ block ]

#########
# define flag
#########
pillar.flag.name = 'flag'
pillar.flag.iterationMethod = 5
pillar.flag.propagationConstant = 0
pillar.flag.flagOne = 0
pillar.flag.flagTwo = 0
pillar.flag.iterations = 100000
pillar.flag.timeStep = 0.9; #mus
pillar.flag.id = 'id'

#########
# define excitation
#########
P_center = 0.5*add(block.lower,block.upper)
P_Ym1 = [ P_center[0], P_center[1]-1*delta, P_center[2] ]

excitation = Excitation()
excitation.name = 'excitation'
excitation.current_source = 7
excitation.P1 = P_Ym1
excitation.P2 = P_center

E = subtract(excitation.P2,excitation.P1)
E = list(E/linalg.norm(E))
print 'E = ', E

excitation.E = E
excitation.H = [ 0, 0, 0 ]
excitation.Type = 10
excitation.time_constant = 4.000000E-09; #mus
excitation.amplitude = 1.000000E+01; #V/mum???
excitation.time_offset = 2.700000E-08; #mus
excitation.frequency = freq
excitation.param1 = 0
excitation.param2 = 0
excitation.param3 = 0
excitation.param4 = 0

pillar.excitation_list = [ excitation ]

#########
# define probe
#########
probe = Probe()
probe.name = 'probe'
probe.position = [ block.upper[0]+delta, P_center[1], P_center[2] ]
probe.step=10
probe.E=[1,1,1]
probe.H=[1,1,1]
probe.J=[0,0,0]
probe.power = 0

pillar.probe_list = [ probe ]

#########
# define frequency snapshots
#########
first = min(65400,pillar.flag.iterations)
repetition = 524200
interpolate = 1
real_dft = 0
mod_only = 0
mod_all = 1
frequency_vector = [freq]
starting_sample = 0
E=[1,1,1]
H=[1,1,1]
J=[0,0,0]

# central snapshot planes
plane = 1
P1 = [block.getCenter()[0], pillar.box.lower[1], pillar.box.lower[2]]
P2 = [block.getCenter()[0], pillar.box.upper[1], pillar.box.upper[2]]
F = Frequency_snapshot('X frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
pillar.snapshot_list.extend([F])

plane = 2
P1 = [pillar.box.lower[0], block.getCenter()[1], pillar.box.lower[2]]
P2 = [pillar.box.upper[0], block.getCenter()[1], pillar.box.upper[2]]
F = Frequency_snapshot('Y frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
pillar.snapshot_list.extend([F])

plane = 3
P1 = [pillar.box.lower[0], pillar.box.lower[1], block.getCenter()[2]]
P2 = [pillar.box.upper[0], pillar.box.upper[1], block.getCenter()[2]]
F = Frequency_snapshot('Z frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
pillar.snapshot_list.extend([F])

# snapshot box
P1 = [pillar.box.lower[0], pillar.box.lower[1], pillar.box.lower[2]]
P2 = [pillar.box.upper[0], pillar.box.upper[1], pillar.box.upper[2]]
F = Frequency_snapshot('Box frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
pillar.snapshot_list.extend([F])

#########
# define mesh
#########
max_delta_Vector_X = [ delta, delta, delta, delta ]
max_delta_Vector_Y = [ delta, delta, delta, delta, delta, delta ]
max_delta_Vector_Z = [ delta, delta, delta, delta ]

thicknessVector_X = LimitsToThickness([ pillar.box.lower[0], block.lower[0], block.upper[0], block.upper[0]+delta, pillar.box.upper[0] ])
thicknessVector_Y = [ block.lower[1]-pillar.box.lower[1], (block.getCenter()[1]-delta)-block.lower[1], delta, delta, block.upper[1]-(block.getCenter()[1]+delta), pillar.box.upper[1]-block.upper[1] ]
thicknessVector_Z = LimitsToThickness([ pillar.box.lower[2], block.lower[2], block.getCenter()[2], block.upper[2], pillar.box.upper[2] ])

pillar.delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X,thicknessVector_X)
print 'max_delta_Vector_Y = ', max_delta_Vector_Y
print 'thicknessVector_Y = ', thicknessVector_Y
pillar.delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y,thicknessVector_Y)
pillar.delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z,thicknessVector_Z)

#########
# write
#########
DSTDIR = os.getenv('DATADIR')
BASENAME = 'simple_pillar'
WALLTIME = 360

pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)

sh_filename = DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh';
probe_col = 0
if pillar.excitation_list[0].E == [1,0,0]:
  probe_col = 2
elif pillar.excitation_list[0].E == [0,1,0]:
  probe_col = 3
elif pillar.excitation_list[0].E == [0,0,1]:
  probe_col = 4
else:
  print('ERROR : Unknown Excitation type')
  sys.exit(-1)
GEOshellscript_advanced(sh_filename, BASENAME, probe_col,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME)
