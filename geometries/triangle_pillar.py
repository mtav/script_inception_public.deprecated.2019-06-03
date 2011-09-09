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

def ExcitationWrapper(Ysym,centre,size,plane_direction,type,excitation_direction,frequency,template_filename='template.dat'):
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
    if not(Ysym):
      excitation.setExtension(centre,centre + size*array(excitation_direction))
    else:
      excitation.setExtension(centre,centre - size*array(excitation_direction))
  else:
    excitation.current_source = 11
    diagonal = (array(plane_direction_vector)^array([1,1,1]))
    if not(Ysym):
      excitation.setExtension(centre - size*diagonal, centre + size*diagonal)
    else:
      excitation.setExtension(centre - size*diagonal, centre)

  if excitation_direction==[1,0,0]:
    out_col_name = 'Exre'
  if excitation_direction==[0,1,0]:
    out_col_name = 'Eyre'
  if excitation_direction==[0,0,1]:
    out_col_name = 'Ezre'

  if plane_direction_alpha=='x':
    column_titles = ['y','z','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']
    x = centre[1]
    y = centre[2]
  if plane_direction_alpha=='y':
    column_titles = ['x','z','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']
    x = centre[0]
    y = centre[2]
  if plane_direction_alpha=='z':
    column_titles = ['x','y','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']
    x = centre[0]
    y = centre[1]
    
    #template1 = ExcitationGaussian1(amplitude = 1, beam_centre_x = centre, beam_centre_y = 2.00, sigma_x = 0.1, sigma_y = 0.9, fileName='template.dat')
    #pillar.excitation_template_list.append(template1)
    #template1.writeDatFile('template1.dat',x_list,y_list, out_col_name, column_titles)
  template = ExcitationGaussian2(amplitude = 1, beam_centre_x = x, beam_centre_y = y, c = 0, sigma = size, fileName='template.dat')
  template.out_col_name = out_col_name
  template.column_titles = column_titles
  
    #pillar.excitation_template_list.append(template2)
    #template2.writeDatFile('template2.dat',x_list,y_list, out_col_name, column_titles)

  return(excitation, template)
  #return excitation

def QuadrupleExcitation(Ysym,pillar,P,direction,delta,template_radius,freq,exc):
  if direction == 'x':
    E1=[0,1,0]
    E2=[0,0,1]
  elif direction == 'y':
    E1=[1,0,0]
    E2=[0,0,1]
  elif direction == 'z':
    E1=[1,0,0]
    E2=[0,1,0]
  else:
    sys.exit(-1)

  if exc == 0:
    # E1 1D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=delta,plane_direction=direction,type='1D',excitation_direction=E1,frequency=freq)
    pillar.excitation_list.append(excitation)
  elif exc == 1:
    # E2 1D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=delta,plane_direction=direction,type='1D',excitation_direction=E2,frequency=freq)
    pillar.excitation_list.append(excitation)
  elif exc == 2:
    # E1 2D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=template_radius,plane_direction=direction,type='2D',excitation_direction=E1,frequency=freq)
    pillar.excitation_list.append(excitation)
    pillar.excitation_template_list.append(template)
  elif exc == 3:
    # E2 2D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=template_radius,plane_direction=direction,type='2D',excitation_direction=E2,frequency=freq)
    pillar.excitation_list.append(excitation)
    pillar.excitation_template_list.append(template)
  else:
    sys.exit(-1)

def prismPillar(DSTDIR,BASENAME,pos,exc):
  pillar = BFDTDobject()
  
  # constants
  n_air = 1; n_diamond = 2.4
  Lambda_mum = 0.637
  delta = Lambda_mum/(10*n_diamond)
  freq = get_c0()/Lambda_mum
  k=4; radius = k*Lambda_mum/(4*n_diamond)
  Nbottom = 3; Ntop = 3
  h_air = Lambda_mum/(4*n_air)
  h_diamond = Lambda_mum/(4*n_diamond)
  h_cavity = Lambda_mum/(n_diamond)
  height = Nbottom*(h_air+h_diamond) + h_cavity + Ntop*(h_air+h_diamond)
  print('height = ',height)
  buffer = 0.05
  FullBox_upper = [ height+2*buffer, 2*(radius+buffer), 2*(radius+buffer) ]
  
  P_centre = [ buffer + Nbottom*(h_air+h_diamond) + 0.5*h_cavity, 0.5*FullBox_upper[1], 0.5*FullBox_upper[2] ]
  
  # define flag
  pillar.flag.iterations = 100000
  #pillar.flag.iterations = 1
  
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
  
  #P_centre = pillar.box.getCenter()
  
  ## define geometry
  
  #prism = TriangularPrism()
  prism = SpecialTriangularPrism()
  prism.lower = [ 0, 0, 0 ]
  prism.upper = [ height, 2*3./2.*radius*1.0/sqrt(3), 3./2.*radius ]
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
  
  prismPos = copy(pillar.box.getCenter())
  if pillar.boundaries.Ypos_bc == 1:
    prismPos[1] = pillar.box.upper[1]
  prism.setGeoCentre(prismPos)
  #pillar.probe_list.append(Probe(position = prism.getGeoCentre()))
  #prism.setGeoCentre([0,0,0])
  #pillar.probe_list.append(Probe(position = prism.getGeoCentre()))
  
  pillar.geometry_object_list.append(prism)
  
  buffersize=10*delta
  n_meshblock = 2.4
  
  # X buffers
  block = Block(permittivity = pow(n_meshblock,2), conductivity = 0)
  block.lower = [ prism.lower[0]-buffersize, prism.lower[1], prism.lower[2] ]
  block.upper = [ prism.lower[0], prism.upper[1], prism.upper[2] ]
  pillar.mesh_object_list.append(block)
  
  block = Block(permittivity = pow(n_meshblock,2), conductivity = 0)
  block.lower = [ prism.upper[0], prism.lower[1], prism.lower[2] ]
  block.upper = [ prism.upper[0]+buffersize, prism.upper[1], prism.upper[2] ]
  pillar.mesh_object_list.append(block)
  
  # Y buffers
  block = Block(permittivity = pow(n_meshblock,2), conductivity = 0)
  block.lower = [ prism.lower[0], prism.lower[1]-buffersize, prism.lower[2] ]
  block.upper = [ prism.upper[0], prism.lower[1], prism.upper[2] ]
  pillar.mesh_object_list.append(block)
  
  block = Block(permittivity = pow(n_meshblock,2), conductivity = 0)
  block.lower = [ prism.lower[0], prism.upper[1], prism.lower[2] ]
  block.upper = [ prism.upper[0], prism.upper[1]+buffersize, prism.upper[2] ]
  pillar.mesh_object_list.append(block)
  
  # Z buffers
  block = Block(permittivity = pow(n_meshblock,2), conductivity = 0)
  block.lower = [ prism.lower[0], prism.lower[1], prism.lower[2]-buffersize ]
  block.upper = [ prism.upper[0], prism.upper[1], prism.lower[2] ]
  pillar.mesh_object_list.append(block)
  
  block = Block(permittivity = pow(n_meshblock,2), conductivity = 0)
  block.lower = [ prism.lower[0], prism.lower[1], prism.upper[2] ]
  block.upper = [ prism.upper[0], prism.upper[1], prism.upper[2]+buffersize ]
  pillar.mesh_object_list.append(block)
  
  #pillar.autoMeshGeometry(0.637/10)
  #print pillar.getNcells()
  
  ##################################
  # prepare some points
  
  (A1_global,B1_global,C1_global,A2_global,B2_global,C2_global) = prism.getGlobalEnvelopPoints()
  #pillar.probe_list.append(Probe(position = A1_global))
  #pillar.probe_list.append(Probe(position = B1_global))
  #pillar.probe_list.append(Probe(position = C1_global))
  #pillar.probe_list.append(Probe(position = A2_global))
  #pillar.probe_list.append(Probe(position = B2_global))
  #pillar.probe_list.append(Probe(position = C2_global))
  
  bottom_centre = (A1_global+B1_global+C1_global)/3.0
  print('bottom_centre = ',bottom_centre)
  top_centre = (A2_global+B2_global+C2_global)/3.0
  
  P_centre = prism.getGeoCentre()
  
  template_radius = prism.getInscribedSquarePlaneRadius(P_centre)
  print('template_radius = ',template_radius)
  
  P3 = array(P_centre)
  
  prism_height = prism.upper[0] - prism.lower[0]
  prism_bottom = prism.lower[1]
  
  P1 = copy(bottom_centre)
  P1[0] = A1_global[0] - delta
  P2 = copy(bottom_centre)
  P2[2] = A1_global[2] - delta
  
  P4 = copy(top_centre)
  P4[2] = A2_global[2] - delta
  P5 = copy(top_centre)
  P5[0] = A2_global[0] + delta
  
  pillar.autoMeshGeometry(0.637/10)
  # define excitation
  ################
  if pillar.boundaries.Ypos_bc == 2:
    Ysym = False
  else:
    Ysym = True

  if pos == 0:
    QuadrupleExcitation(Ysym,pillar,P1,'x',delta,template_radius,freq,exc)
  elif pos == 1:
    QuadrupleExcitation(Ysym,pillar,P2,'z',delta,template_radius,freq,exc)
  elif pos == 2:
    QuadrupleExcitation(Ysym,pillar,P3,'x',delta,template_radius,freq,exc)
  elif pos == 3:
    QuadrupleExcitation(Ysym,pillar,P4,'z',delta,template_radius,freq,exc)
  elif pos == 4:
    QuadrupleExcitation(Ysym,pillar,P5,'x',delta,template_radius,freq,exc)
  else:
    sys.exit(-1)
  ################
  
  # create template
  #x_min = 0.0
  #x_max = 4.00
  #y_min = 0.0
  #y_max = 4.00
  #step_x = 2.00e-2
  #step_y = 2.00e-1
  #x_list = arange(x_min,x_max,step_x)
  #y_list = arange(y_min,y_max,step_y)
  
  
  #probe_X = [ P_centre[0]-(0.5*height+delta), P_centre[0], P_centre[0]+(0.5*height+delta) ]
  
  #if pillar.boundaries.Ypos_bc == 2:
    #probe_Y = [ P_centre[1] ]
  #else:
    #probe_Y = [ P_centre[1]-delta ]
  
  #probe_Z = [ P_centre[2]-radius-delta, P_centre[2] ]
  
  #for x in probe_X:
    #for y in probe_Y:
      #for z in probe_Z:
        #probe = Probe(position = [ x,y,z ])
        #pillar.probe_list.append(probe)
  
  # define frequency snapshots and probes
  first = min(65400,pillar.flag.iterations)
  frequency_vector = [freq]
  
  P1_m = copy(P1)
  P2_m = copy(P2)
  P3_m = copy(P3)
  P4_m = copy(P4)
  P5_m = copy(P5)
  if pillar.boundaries.Ypos_bc == 1:
    voxeldim_global = prism.getVoxelDimensions()
    P1_m[1] = P1_m[1] - voxeldim_global[1]
    P2_m[1] = P2_m[1] - voxeldim_global[1]
    P3_m[1] = P3_m[1] - voxeldim_global[1]
    P4_m[1] = P4_m[1] - voxeldim_global[1]
    P5_m[1] = P5_m[1] - voxeldim_global[1]
  
  Plist = [P1_m,P2_m,P3_m,P4_m,P5_m]
  for idx in range(len(Plist)):
    P = Plist[idx]
    F = pillar.addFrequencySnapshot(1,P[0]); F.first = first; F.frequency_vector = frequency_vector; F.name='x_'+str(idx)
    F = pillar.addFrequencySnapshot(2,P[1]); F.first = first; F.frequency_vector = frequency_vector; F.name='y_'+str(idx)
    F = pillar.addFrequencySnapshot(3,P[2]); F.first = first; F.frequency_vector = frequency_vector; F.name='z_'+str(idx)
    probe = Probe(position = P); probe.name = 'p_'+str(idx)
    pillar.probe_list.append(probe)
  
  #F = pillar.addFrequencySnapshot(1,P_centre[0]); F.first = first; F.frequency_vector = frequency_vector
  #if pillar.boundaries.Ypos_bc == 2:
    #F = pillar.addFrequencySnapshot(2,P_centre[1]); F.first = first; F.frequency_vector = frequency_vector
  #else:
    #F = pillar.addFrequencySnapshot(2,P_centre[1]-delta); F.first = first; F.frequency_vector = frequency_vector
  #F = pillar.addFrequencySnapshot(3,P_centre[2]); F.first = first; F.frequency_vector = frequency_vector
  
  F = pillar.addBoxFrequencySnapshots(); F.first = first; F.frequency_vector = frequency_vector
  
  ## define mesh
  #pillar.addMeshingBox(lower,upper,)
  #pillar.autoMeshGeometry(0.637/10)
  
  # write
  #DSTDIR = os.getenv('DATADIR')
  #DSTDIR = os.getenv('TESTDIR')
  #DSTDIR = os.getenv('TESTDIR')+os.sep+'triangle_pillar'
  #DSTDIR = os.getenv('DATADIR')+os.sep+'triangle_pillar'
  pillar.writeAll(DSTDIR+os.sep+BASENAME, BASENAME)
  GEOshellscript(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  #GEOshellscript_advanced(DSTDIR+os.sep+BASENAME+os.sep+BASENAME+'.sh', BASENAME, getProbeColumnFromExcitation(excitation.E),'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)
  print pillar.getNcells()
  
if __name__ == "__main__":
  DSTDIR = sys.argv[1]
  if not os.path.isdir(DSTDIR):
      os.mkdir(DSTDIR)

  for pos in range(5):
    for exc in range(4):
      prismPillar(DSTDIR,'triangle_pillar_'+str(pos)+'_'+str(exc),pos,exc)
  #pos=0
  #exc=0
  #prismPillar('triangle_pillar_'+str(pos)+'_'+str(exc),pos,exc)
