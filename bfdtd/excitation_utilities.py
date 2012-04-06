#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utilities.common import *
from bfdtd.excitation import *
from bfdtd.excitationTemplate import *

def ExcitationWrapper(Ysym, centre, size, plane_direction, type,excitation_direction, frequency, template_filename='template.dat'):
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
      excitation.setExtension(centre,centre + size*numpy.array(excitation_direction))
    else:
      excitation.setExtension(centre,centre - size*numpy.array(excitation_direction))
  else:
    excitation.current_source = 11
    diagonal = (numpy.array(plane_direction_vector)^numpy.array([1,1,1]))
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

def QuadrupleExcitation(Ysym,pillar,P,propagation_direction,delta,template_radius,freq,exc):
  if propagation_direction == 'x':
    E1=[0,1,0]
    E2=[0,0,1]
  elif propagation_direction == 'y':
    E1=[1,0,0]
    E2=[0,0,1]
  elif propagation_direction == 'z':
    E1=[1,0,0]
    E2=[0,1,0]
  else:
    sys.exit(-1)

  if exc == 0:
    # E1 1D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=delta,plane_direction=propagation_direction,type='1D',excitation_direction=E1,frequency=freq)
    pillar.excitation_list.append(excitation)
  elif exc == 1:
    # E2 1D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=delta,plane_direction=propagation_direction,type='1D',excitation_direction=E2,frequency=freq)
    pillar.excitation_list.append(excitation)
  elif exc == 2:
    # E1 2D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=template_radius,plane_direction=propagation_direction,type='2D',excitation_direction=E1,frequency=freq)
    pillar.excitation_list.append(excitation)
    pillar.excitation_template_list.append(template)
  elif exc == 3:
    # E2 2D
    excitation, template = ExcitationWrapper(Ysym,centre=P,size=template_radius,plane_direction=propagation_direction,type='2D',excitation_direction=E2,frequency=freq)
    pillar.excitation_list.append(excitation)
    pillar.excitation_template_list.append(template)
  else:
    sys.exit(-1)
