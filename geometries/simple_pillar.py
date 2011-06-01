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
delta = Lambda_mum/(10*n_Diamond)
freq = get_c0()/Lambda_mum
radius = 0.25
height = 2.*20.*Lambda_mum/(2.*n_Diamond) + Lambda_mum/n_Diamond

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
pillar.flag.iterations = 25000

#########
# define excitation
#########
excitation = Excitation()
excitation.P1 = [ block.getCenter()[0], block.getCenter()[1]-1*delta, block.getCenter()[2] ]
excitation.P2 = block.getCenter()
excitation.frequency = freq

E = subtract(excitation.P2,excitation.P1)
E = list(E/linalg.norm(E))
excitation.E = E

pillar.excitation_list = [ excitation ]

#########
# define probe
#########
probe = Probe()
probe.name = 'probe'
probe.position = [ block.upper[0]+delta, block.getCenter()[1], block.getCenter()[2] ]
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
#repetition = 524200
#interpolate = 1
#real_dft = 0
#mod_only = 0
#mod_all = 1
frequency_vector = [freq]
#starting_sample = 0
#E=[1,1,1]
#H=[1,1,1]
#J=[0,0,0]

# central snapshot planes
#plane = 1
#P1 = [block.getCenter()[0], pillar.box.lower[1], pillar.box.lower[2]]
#P2 = [block.getCenter()[0], pillar.box.upper[1], pillar.box.upper[2]]
#F = Frequency_snapshot('X frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
#pillar.snapshot_list.extend([F])

#plane = 2
#P1 = [pillar.box.lower[0], block.getCenter()[1], pillar.box.lower[2]]
#P2 = [pillar.box.upper[0], block.getCenter()[1], pillar.box.upper[2]]
#F = Frequency_snapshot('Y frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
#pillar.snapshot_list.extend([F])

#plane = 3
#P1 = [pillar.box.lower[0], pillar.box.lower[1], block.getCenter()[2]]
#P2 = [pillar.box.upper[0], pillar.box.upper[1], block.getCenter()[2]]
#F = Frequency_snapshot('Z frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
#pillar.snapshot_list.extend([F])

#plane = 1
#P1 = [self.getPillarCenterX(), 0, 0]
#P2 = [self.getPillarCenterX(), self.getYlim(), self.getZlim()]
#F = Frequency_snapshot('X frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
#T = Time_snapshot('X time snapshot', first, repetition, plane, P1, P2, E, H, J, power, 0)
#self.snapshot_list.extend([F,T])

#plane = 2
#P1 = [0, self.Ymax/2-self.getYoffset(), 0]
#P2 = [self.Xmax, self.Ymax/2-self.getYoffset(), self.getZlim()]
#F = Frequency_snapshot('Y frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
#T = Time_snapshot('Y time snapshot', first, repetition, plane, P1, P2, E, H, J, power, 0)
#self.snapshot_list.extend([F,T])

#plane = 3
#P1 = [0, 0, self.Zmax/2-self.getZoffset()]
#P2 = [self.Xmax, self.getYlim(), self.Zmax/2-self.getZoffset()]
#F = Frequency_snapshot('Z frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
#T = Time_snapshot('Z time snapshot', first, repetition, plane, P1, P2, E, H, J, power, 0)
#self.snapshot_list.extend([F,T])

#####################
# box
#P1 = [0,0,0]
#P2 = [self.Xmax, self.getYlim(), self.getZlim()]
#F = Frequency_snapshot('Box frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
#self.snapshot_list.extend([F])

# snapshot box
F = pillar.addBoxFrequencySnapshots()
F.frequency_vector = frequency_vector
F.first = first

#P1 = [pillar.box.lower[0], pillar.box.lower[1], pillar.box.lower[2]]
#P2 = [pillar.box.upper[0], pillar.box.upper[1], pillar.box.upper[2]]
#F = Frequency_snapshot('Box frequency snapshot', first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, frequency_vector, starting_sample, E, H, J)
#pillar.snapshot_list.extend([F])

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
#DSTDIR = os.getenv('DATADIR')
DSTDIR = os.getenv('TESTDIR')
BASENAME = 'simple_pillar_2'
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

print pillar.getNcells()
