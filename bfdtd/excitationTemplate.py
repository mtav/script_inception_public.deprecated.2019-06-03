#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from bfdtd.bfdtd_parser import *

import sys

# excitation template object
#class ExcitationTemplate:
  #def __init__(self):
    #x_min_mum = 0.0;
    #x_max_mum = 4.00;
    #z_min_mum = 0.0;
    #z_max_mum = 4.00;
    #step_x_mum = 2.00e-2;
    #step_z_mum = 2.00e-2;
    #beam_centre_x_mum = 2.1732;
    #beam_centre_z_mum = 2.00;
    #c_mum = 0;
    #sigma_mum = 0.5;
  #def __str__(self):
    #ret = '--->object rotation_list'
    #for i in range(len(self.rotation_list)):
      #ret += '\n'
      #ret += '-->object rotation '+str(i)+':\n'
      #ret += self.rotation_list[i].__str__()
    #return(ret)

  #def writeDatFile(self,fileName):
    #'''Generate template .dat file for a plane excitation'''
    ## open file
    #with open(fileName, 'w') as out:
      #for obj in self.excitation_template_list:
        #obj.write_entry(out)
    #return

def drange(start, stop, step):
  r = start
  while r < stop:
    yield r
    r += step

x_min = 0.0
x_max = 4.00
y_min = 0.0
y_max = 4.00
step_x = 2.00e-1
step_y = 2.00e-1
beam_centre_x = 2.1732
beam_centre_y = 2.00
c = 0
sigma = 0.5

print(step_x)
x_list = arange(x_min,x_max,step_x)
y_list = arange(y_min,y_max,step_y)

print(x_list)

x_col = []
y_col = []
out_col = []

for x in x_list:
  for z in y_list:
    x_col.append(x)
    y_col.append(z)
    r = abs(sqrt( pow((x-beam_centre_x),2) + pow((z-beam_centre_y),2) ))
    out_col.append( exp( -pow((r-c),2) / (2*pow(sigma,2)) ) )

fileName = sys.argv[1]
E = [1,1,1]
H = [1,1,1]
out_col_name = 'Exre'

column_titles = ['x','z','Exre','Exim','Eyre','Eyim','Ezre','Ezim','Hxre','Hxim','Hyre','Hyim','Hzre','Hzim']
with open(fileName, 'w') as FILE:
  for idx_col in range(len(column_titles)):
    if idx_col>0:
      FILE.write('\t')
    FILE.write(column_titles[idx_col])
  FILE.write('\n')
  for idx_row in range(len(out_col)):
    #print(x_col[idx_row])
    FILE.write("%15.6E\t%15.6E" % (x_col[idx_row], y_col[idx_row]))
    for idx_col in range(len(column_titles)-2):
      if column_titles[idx_col+2] == out_col_name:
        FILE.write("\t%15.6E" % out_col[idx_row])
      else:
        FILE.write("\t%15.6E" % 0)
    FILE.write('\n')
