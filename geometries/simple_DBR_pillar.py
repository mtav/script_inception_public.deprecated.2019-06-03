#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bfdtd.bfdtd_parser import *
from numpy import *
from utilities.common import *
from constants.constants import *
from meshing.subGridMultiLayer import *
import os

for k in [1,2,3,4,5,6,7,8]:
  pillar = BFDTDobject()
  
  # constants
  n_air = 1; n_diamond = 2.4
  Lambda_mum = 0.637
  delta = Lambda_mum/(10*n_diamond)
  freq = get_c0()/Lambda_mum
  #k=8;
  radius = k*Lambda_mum/(4*n_diamond)
  Nbottom = 40; Ntop = 20
  h_air = Lambda_mum/(4*n_air)
  h_diamond = Lambda_mum/(4*n_diamond)
  h_cavity = Lambda_mum/(n_diamond)
  height = Nbottom*(h_air+h_diamond) + h_cavity + Ntop*(h_air+h_diamond)
  buffer = 0.25
  subbuffer = 4*delta
  FullBox_upper = [ height+2*buffer, 2*(radius+buffer), 2*(radius+buffer) ]
  P_centre = [ buffer + Nbottom*(h_air+h_diamond) + 0.5*h_cavity, 0.5*FullBox_upper[1], 0.5*FullBox_upper[2] ]
  
  # define flag
  pillar.flag.iterations = 100000
  
  # define boundary conditions
  pillar.boundaries.Xpos_bc = 2
  pillar.boundaries.Ypos_bc = 1
  pillar.boundaries.Zpos_bc = 2
  
  # define box
  pillar.box.lower = [0,0,0]
  if pillar.boundaries.Ypos_bc == 2:
    pillar.box.upper = FullBox_upper
  else:
    pillar.box.upper = [ FullBox_upper[0], 0.5*FullBox_upper[1], FullBox_upper[2] ]
  
  # define geometry
  Ymin=P_centre[1]-radius
  Ymax=P_centre[1]+radius
  Zmin=P_centre[2]-radius
  Zmax=P_centre[2]+radius
  
  X_current = buffer
  
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
  thicknessVector_X = [ buffer ]
  thicknessVector_X.extend([h_diamond,h_air]*Nbottom)
  thicknessVector_X.extend([0.5*h_cavity,0.5*h_cavity])
  thicknessVector_X.extend([h_air,h_diamond]*Ntop)
  thicknessVector_X.extend([delta,buffer-delta])
  max_delta_Vector_X = [ delta ]*len(thicknessVector_X)
  
  thicknessVector_Y = [ (block.lower[1]-subbuffer)-pillar.box.lower[1], subbuffer, (P_centre[1]-delta)-block.lower[1], delta ]
  max_delta_Vector_Y = [ h_air, delta, delta, delta ]
  if pillar.boundaries.Ypos_bc == 2:
    thicknessVector_Y = symmetrifyEven(thicknessVector_Y)
    max_delta_Vector_Y = symmetrifyEven(max_delta_Vector_Y)
  
  thicknessVector_Z = LimitsToThickness([ pillar.box.lower[2], block.lower[2]-subbuffer, block.lower[2], P_centre[2], block.upper[2], block.upper[2]+subbuffer, pillar.box.upper[2] ])
  max_delta_Vector_Z = [ h_air, delta, delta, delta, delta, h_air ]
  
  pillar.delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X, thicknessVector_X)
  pillar.delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y, thicknessVector_Y)
  pillar.delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z, thicknessVector_Z)
  
  # write
  #DSTDIR = os.getenv('DATADIR')
  #DSTDIR = os.getenv('TESTDIR')
  DSTDIR = os.getenv('DATADIR')+os.sep+'run_20110602'
  BASENAME = 'simple_DBR_pillar.k_'+str(k)
  pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
  GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  print pillar.getNcells()
  
