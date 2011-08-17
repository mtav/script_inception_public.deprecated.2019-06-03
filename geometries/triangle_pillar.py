#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *
from numpy import *
from utilities.common import *
from constants.constants import *
from meshing.subGridMultiLayer import *
import os

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

# define geometry
block = Block()
block.lower = [ P_centre[0]-0.5*height, P_centre[1]-radius, P_centre[2]-radius ]
block.upper = [ P_centre[0]+0.5*height, P_centre[1]+radius, P_centre[2]+radius ]
block.permittivity = pow(n_diamond,2)
block.conductivity = 0
pillar.geometry_object_list = [ block ]

# define excitation
excitation = Excitation()
excitation.P1 = [ P_centre[0], P_centre[1]-1*delta, P_centre[2] ]
excitation.P2 = P_centre
excitation.frequency = freq
excitation.E = list(Unit(subtract(excitation.P2,excitation.P1)))
pillar.excitation_list = [ excitation ]

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

# define mesh
thicknessVector_X = [ block.lower[0]-pillar.box.lower[0], P_centre[0]-block.lower[0], block.upper[0]-P_centre[0], delta, pillar.box.upper[0]-(block.upper[0]+delta) ]
if pillar.boundaries.Ypos_bc == 2:
  thicknessVector_Y = [ block.lower[1]-pillar.box.lower[1], (P_centre[1]-delta)-block.lower[1], delta, delta, block.upper[1]-(P_centre[1]+delta), pillar.box.upper[1]-block.upper[1] ]
else:
  thicknessVector_Y = [ block.lower[1]-pillar.box.lower[1], (P_centre[1]-delta)-block.lower[1], delta ]
thicknessVector_Z = LimitsToThickness([ pillar.box.lower[2], block.lower[2], P_centre[2], block.upper[2], pillar.box.upper[2] ])
max_delta_Vector_X = [ delta ]*len(thicknessVector_X)
max_delta_Vector_Y = [ delta ]*len(thicknessVector_Y)
max_delta_Vector_Z = [ delta ]*len(thicknessVector_Z)
pillar.delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X, thicknessVector_X)
pillar.delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y, thicknessVector_Y)
pillar.delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z, thicknessVector_Z)

# write
#DSTDIR = os.getenv('DATADIR')
#DSTDIR = os.getenv('TESTDIR')
DSTDIR = os.getenv('TESTDIR')
BASENAME = 'triangle_pillar'
pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
print pillar.getNcells()

####################################
    elif self.HOLE_TYPE == 'triangular_yagi_voxel':
      voxel_Ymin = self.Ymax/2.0 - self.radius_Y_pillar_mum
      voxel_Ymax = self.Ymax/2.0 + self.radius_Y_pillar_mum
      voxel_radius_X = self.radius_X_hole/( 2.*self.Nvoxels + 1.)
      D = self.radius_Z_pillar_mum - self.radius_Z_hole
      R = self.radius_X_hole
      N = self.Nvoxels
      Z_left = self.Zmax/2.0 - self.radius_Z_pillar_mum
      Z_right = self.Zmax/2.0 + self.radius_Z_pillar_mum
      offset = X_current - self.radius_X_hole
      for i in range(self.Nvoxels):
        # bottom left blocks
        lower = [ offset+2*R*(i)/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
        upper = [ offset+2*R*(i + 1)/(2*N+1), voxel_Ymax, Z_left+D*(i + 1)/(N+1)]
        self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
        # top left blocks
        lower = [ offset+2*R*((2*N+1)-(i))/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
        upper = [ offset+2*R*((2*N+1)-(i + 1))/(2*N+1), voxel_Ymax, Z_left+D*(i + 1)/(N+1)]
        self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
        # bottom right blocks
        lower = [ offset+2*R*(i)/(2*N+1), voxel_Ymin, Z_right-D*(0)/(N+1)]
        upper = [ offset+2*R*(i + 1)/(2*N+1), voxel_Ymax, Z_right-D*(i + 1)/(N+1)]
        self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
        # top right blocks
        lower = [ offset+2*R*((2*N+1)-(i))/(2*N+1), voxel_Ymin, Z_right-D*(0)/(N+1)]
        upper = [ offset+2*R*((2*N+1)-(i + 1))/(2*N+1), voxel_Ymax, Z_right-D*(i + 1)/(N+1)]
        self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
      ## middle left block
      lower = [ offset+2*R*(N)/(2*N+1), voxel_Ymin, Z_left+D*(0)/(N+1)]
      upper = [ offset+2*R*(N + 1)/(2*N+1), voxel_Ymax, Z_left+D*(N + 1)/(N+1)]# - self.radius_Z_pillar_mum + D]
      self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
      ## middle right block
      lower = [ offset+2*R*(N)/(2*N+1), voxel_Ymin, Z_right-D*(0)/(N+1)]
      upper = [ offset+2*R*(N + 1)/(2*N+1), voxel_Ymax, Z_right-D*(N + 1)/(N+1)]# - self.radius_Z_pillar_mum + D]
      self.geometry_object_list.append(Block(name=COMMENT, lower=lower, upper=upper, permittivity=permittivity, conductivity=conductivity))
