#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from bfdtd.bfdtd_parser import *

import sys
  
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

  def writeDatFile(self,fileName,mesh):
    '''Generate template .dat file for a plane excitation'''
    x_list = mesh.getXmesh()
    y_list = mesh.getYmesh()
    z_list = mesh.getZmesh()
    
    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(x_list)*len(y_list)))
    for x in x_list:
      for y in y_list:
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
          if self.column_titles[idx_col+2] == self.out_col_name:
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

  def writeDatFile(self,fileName,mesh):
    '''Generate template .dat file for a plane excitation'''
    x_list = mesh.getXmesh()
    y_list = mesh.getYmesh()
    z_list = mesh.getZmesh()
    
    x_col = []
    y_col = []
    out_col = []
    
    print('Generating template N='+str(len(x_list)*len(y_list)))
    for x in x_list:
      for y in y_list:
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
          if self.column_titles[idx_col+2] == self.out_col_name:
            FILE.write("\t%15.6E" % out_col[idx_row])
          else:
            FILE.write("\t%15.6E" % 0)
        FILE.write('\n')

    return
