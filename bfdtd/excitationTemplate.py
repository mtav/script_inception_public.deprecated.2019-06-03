#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from bfdtd.bfdtd_parser import *

import sys

'''
Excitation template objects, used to generate the template files.
'''

# TODO: Create template parent class, improve class names of excitations and templates, review the whole excitation+template system
#TODO: Add .dat file reading

# gaussian excitation template object which creates a 2D gaussian surface with a central maximum point
class ExcitationGaussian1(object):
  def __init__(self,amplitude = 1, beam_centre_x = 0, beam_centre_y = 0, sigma_x = 1, sigma_y = 1, out_col_name='z', column_titles=['x','y','z'], fileName='template.dat'):
    self.amplitude = amplitude
    self.beam_centre_x = beam_centre_x
    self.beam_centre_y = beam_centre_y
    self.sigma_x = sigma_x
    self.sigma_y = sigma_y
    self.out_col_name = out_col_name
    self.column_titles = column_titles
    self.fileName = fileName
    self.x_list = [-1,0,1]
    self.y_list = [-1,0,1]
  
  def writeDatFile(self,fileName,mesh):
    print('ERROR: This function is deprecated.')
    sys.exit(-1)
    
  def writeDatFile(self,fileName):
    '''Generate template .dat file for a plane excitation'''
    #self.x_list = mesh.getXmesh()
    #self.y_list = mesh.getYmesh()
    #self.z_list = mesh.getZmesh()
    
    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(self.x_list)*len(self.y_list)))
    for x in self.x_list:
      for y in self.y_list:
        x_col.append(x)
        y_col.append(y)
        X = x-self.beam_centre_x
        Y = y-self.beam_centre_y
        R = abs(numpy.sqrt( pow((X),2) + pow((Y),2) ))
        #out = self.amplitude * numpy.exp( -pow((R-self.c),2) / (2*pow(self.sigma,2)) )
        out = self.amplitude * numpy.exp( -( pow(X,2)/(2*pow(self.sigma_x,2)) + pow(Y,2)/(2*pow(self.sigma_y,2)) ) )
        out_col.append(out)
    
    # write file
    with open(fileName, 'w') as FILE:
      print('Writing excitation template to '+fileName)
      for idx_col in range(len(self.column_titles)):
        if idx_col>0:
          FILE.write('\t')
        FILE.write(self.column_titles[idx_col])
      FILE.write('\n')
      for idx_row in range(len(out_col)):
        #print(x_col[idx_row])
        FILE.write("%15.6E\t%15.6E" % (x_col[idx_row], y_col[idx_row]))
        for idx_col in range(len(self.column_titles)-2):
          if self.column_titles[idx_col+2].lower() in [ x.lower() for x in self.out_col_name ]:
            FILE.write("\t%15.6E" % out_col[idx_row])
          else:
            FILE.write("\t%15.6E" % 0)
        FILE.write('\n')

    return

# gaussian excitation template object which creates a 2D gaussian surface with a circular maximum of radius c
class ExcitationGaussian2(object):
  def __init__(self,amplitude = 1, beam_centre_x = 0, beam_centre_y = 0, c = 1, sigma = 2, out_col_name='z', column_titles=['x','y','z'], fileName='template.dat'):
    self.amplitude = amplitude
    self.beam_centre_x = beam_centre_x
    self.beam_centre_y = beam_centre_y
    self.c = c
    self.sigma = sigma
    self.out_col_name = out_col_name
    self.column_titles = column_titles
    self.fileName = fileName
    self.x_list = [-1,0,1]
    self.y_list = [-1,0,1]

  def writeDatFile(self,fileName,mesh):
    print('ERROR: This function is deprecated.')
    sys.exit(-1)

  def writeDatFile(self,fileName):
    '''Generate template .dat file for a plane excitation'''
    #self.x_list = mesh.getXmesh()
    #self.y_list = mesh.getYmesh()
    #self.z_list = mesh.getZmesh()
    
    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(self.x_list)*len(self.y_list)))
    for x in self.x_list:
      for y in self.y_list:
        x_col.append(x)
        y_col.append(y)
        X = x-self.beam_centre_x
        Y = y-self.beam_centre_y
        R = abs(numpy.sqrt( pow((X),2) + pow((Y),2) ))
        out = self.amplitude * numpy.exp( -pow((R-self.c),2) / (2*pow(self.sigma,2)) )
        #out = self.amplitude * numpy.exp( -( pow(X,2)/(2*pow(self.sigma_x,2)) + pow(Y,2)/(2*pow(self.sigma_y,2)) ) )
        out_col.append(out)
    
    # write file
    with open(fileName, 'w') as FILE:
      print('Writing excitation template to '+fileName)
      for idx_col in range(len(self.column_titles)):
        if idx_col>0:
          FILE.write('\t')
        FILE.write(self.column_titles[idx_col])
      FILE.write('\n')
      for idx_row in range(len(out_col)):
        #print(x_col[idx_row])
        FILE.write("%15.6E\t%15.6E" % (x_col[idx_row], y_col[idx_row]))
        for idx_col in range(len(self.column_titles)-2):
          if self.column_titles[idx_col+2].lower() in [ x.lower() for x in self.out_col_name ]:
            FILE.write("\t%15.6E" % out_col[idx_row])
          else:
            FILE.write("\t%15.6E" % 0)
        FILE.write('\n')

    return

# gaussian excitation template object which creates a 2D gaussian surface with a circular maximum of radius c
class ExcitationUniform(object):
  def __init__(self,
   amplitude = None,
   out_col_name = None,
   column_titles = None,
   fileName = None,
   x_list = None,
   y_list = None):
    
    if amplitude is None: amplitude = 1
    if out_col_name is None: out_col_name = 'z'
    if column_titles is None: column_titles = ['x','y','z']
    if fileName is None: fileName = 'template.dat'
    if x_list is None: x_list = [-1,0,1]
    if y_list is None: y_list = [-1,0,1]
    
    self.amplitude = amplitude
    self.out_col_name = out_col_name
    self.column_titles = column_titles
    self.fileName = fileName
    self.x_list = x_list
    self.y_list = y_list

  def writeDatFile(self,fileName):
    '''Generate template .dat file for a plane excitation'''
    #self.x_list = mesh.getXmesh()
    #self.y_list = mesh.getYmesh()
    #self.z_list = mesh.getZmesh()
    
    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(self.x_list)*len(self.y_list)))
    for x in self.x_list:
      for y in self.y_list:
        x_col.append(x)
        y_col.append(y)
        out_col.append(self.amplitude)
    
    # write file
    with open(fileName, 'w') as FILE:
      print('Writing excitation template to '+fileName)
      for idx_col in range(len(self.column_titles)):
        if idx_col>0:
          FILE.write('\t')
        FILE.write(self.column_titles[idx_col])
      FILE.write('\n')
      for idx_row in range(len(out_col)):
        #print(x_col[idx_row])
        FILE.write("%15.6E\t%15.6E" % (x_col[idx_row], y_col[idx_row]))
        for idx_col in range(len(self.column_titles)-2):
          if self.column_titles[idx_col+2].lower() in [ x.lower() for x in self.out_col_name ]:
            FILE.write("\t%15.6E" % out_col[idx_row])
          else:
            FILE.write("\t%15.6E" % 0)
        FILE.write('\n')

    return
