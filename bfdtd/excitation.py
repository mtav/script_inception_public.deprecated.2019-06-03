#!/usr/bin/env python

from __future__ import division
from bfdtd.meshingparameters import *
from utilities.common import *

# excitation objects
class Excitation:
  def __init__(self,
                name = 'excitation',
                current_source = 7,
                P1 = [0,0,0],
                P2 = [0,0,0],
                E = [0,0,0],
                H = [0,0,0],
                Type = 10,
                time_constant = 4.000000E-09, #mus
                amplitude = 1.000000E+01, #V/mum???
                time_offset = 2.700000E-08, #mus
                frequency = 0,
                param1 = 0,
                param2 = 0,
                template_filename = 'template.dat',
                template_source_plane = 'x',
                template_target_plane = 'x',
                template_direction = 0,
                template_rotation = 0,
                layer = 'excitation',
                group = 'excitation'):
                
    self.name = name
    self.layer = layer
    self.group = group
    self.current_source = current_source
    self.P1 = P1
    self.P2 = P2
    self.E = E
    self.H = H
    self.Type = Type
    self.time_constant = time_constant
    self.amplitude = amplitude
    self.time_offset = time_offset
    self.frequency = frequency
    self.param1 = param1
    self.param2 = param2
    self.template_filename = template_filename
    self.template_source_plane = template_source_plane
    self.template_target_plane = template_target_plane
    self.template_direction = template_direction
    self.template_rotation = template_rotation

    self.meshing_parameters = MeshingParameters()

  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'current_source = ' + str(self.current_source) + '\n' +\
    'P1 = ' + str(self.P1) + '\n' +\
    'P2 = ' + str(self.P2) + '\n' +\
    'E = ' + str(self.E) + '\n' +\
    'H = ' + str(self.H) + '\n' +\
    'Type = ' + str(self.Type) + '\n' +\
    'time_constant = ' + str(self.time_constant) + '\n' +\
    'amplitude = ' + str(self.amplitude) + '\n' +\
    'time_offset = ' + str(self.time_offset) + '\n' +\
    'frequency = ' + str(self.frequency) + '\n' +\
    'param1 = ' + str(self.param1) + '\n' +\
    'param2 = ' + str(self.param2) + '\n' +\
    'template_filename = ' + self.template_filename + '\n' +\
    'template_source_plane = ' + self.template_source_plane
    'template_target_plane = ' + self.template_target_plane
    'template_direction = ' + str(self.template_direction)
    'template_rotation = ' + str(self.template_rotation)
    return ret
    
  def setExtension(self,P1,P2):
    self.P1, self.P2 = fixLowerUpper(P1, P2)
    
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    idx = 0
    self.current_source = float(entry.data[idx]); idx = idx+1
    self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.Type = float(entry.data[idx]); idx = idx+1
    self.time_constant = float(entry.data[idx]); idx = idx+1
    self.amplitude = float(entry.data[idx]); idx = idx+1
    self.time_offset = float(entry.data[idx]); idx = idx+1
    self.frequency = float(entry.data[idx]); idx = idx+1
    self.param1 = float(entry.data[idx]); idx = idx+1
    self.param2 = float(entry.data[idx]); idx = idx+1
    self.template_filename = entry.data[idx]; idx = idx+1
    self.template_source_plane = entry.data[idx]; idx = idx+1
    if idx<len(entry.data):
      self.template_target_plane = entry.data[idx]; idx = idx+1
    if idx<len(entry.data):
      self.template_direction = int(entry.data[idx]); idx = idx+1
    if idx<len(entry.data):
      self.template_rotation = int(entry.data[idx]); idx = idx+1
    return(0)
    
  def write_entry(self, FILE):
    if self.current_source != 11:
      self.P1, self.P2 = fixLowerUpper(self.P1, self.P2)
      FILE.write('EXCITATION **name='+self.name+'\n')
      FILE.write('{\n')
      FILE.write("%d ** CURRENT SOURCE \n" % self.current_source)
      FILE.write("%E **X1\n" % self.P1[0])
      FILE.write("%E **Y1\n" % self.P1[1])
      FILE.write("%E **Z1\n" % self.P1[2])
      FILE.write("%E **X2\n" % self.P2[0])
      FILE.write("%E **Y2\n" % self.P2[1])
      FILE.write("%E **Z2\n" % self.P2[2])
      FILE.write("%d **EX\n" % self.E[0])
      FILE.write("%d **EY\n" % self.E[1])
      FILE.write("%d **EZ\n" % self.E[2])
      FILE.write("%d **HX\n" % self.H[0])
      FILE.write("%d **HY\n" % self.H[1])
      FILE.write("%d **HZ\n" % self.H[2])
      FILE.write("%d **GAUSSIAN MODULATED SINUSOID\n" % self.Type)
      FILE.write("%E **TIME CONSTANT\n" % self.time_constant)
      FILE.write("%E **AMPLITUDE\n" % self.amplitude)
      FILE.write("%E **TIME OFFSET\n" % self.time_offset)
      FILE.write("%E **FREQ (HZ)\n" % self.frequency)
      FILE.write("%d **UNUSED PARAMETER\n" % self.param1)
      FILE.write("%d **UNUSED PARAMETER\n" % self.param2)
      FILE.write('"'+str(self.template_filename)+'" ** TEMPLATE FILENAME\n')
      FILE.write('"'+str(self.template_source_plane)+'" ** TEMPLATE SOURCE PLANE\n')
      FILE.write('}\n')
      FILE.write('\n')
    else:
      self.E = [1,1,1]
      self.H = [1,1,1]
      self.P1, self.P2 = fixLowerUpper(self.P1, self.P2)
      FILE.write('EXCITATION **name='+self.name+'\n')
      FILE.write('{\n')
      FILE.write("%d ** CURRENT SOURCE \n" % self.current_source)
      FILE.write("%E **X1\n" % self.P1[0])
      FILE.write("%E **Y1\n" % self.P1[1])
      FILE.write("%E **Z1\n" % self.P1[2])
      FILE.write("%E **X2\n" % self.P2[0])
      FILE.write("%E **Y2\n" % self.P2[1])
      FILE.write("%E **Z2\n" % self.P2[2])
      FILE.write("%d **EX\n" % self.E[0])
      FILE.write("%d **EY\n" % self.E[1])
      FILE.write("%d **EZ\n" % self.E[2])
      FILE.write("%d **HX\n" % self.H[0])
      FILE.write("%d **HY\n" % self.H[1])
      FILE.write("%d **HZ\n" % self.H[2])
      FILE.write("%d **GAUSSIAN MODULATED SINUSOID\n" % self.Type)
      FILE.write("%E **TIME CONSTANT\n" % self.time_constant)
      FILE.write("%E **AMPLITUDE\n" % self.amplitude)
      FILE.write("%E **TIME OFFSET\n" % self.time_offset)
      FILE.write("%E **FREQ (HZ)\n" % self.frequency)
      FILE.write("%d **UNUSED PARAMETER\n" % self.param1)
      FILE.write("%d **UNUSED PARAMETER\n" % self.param2)
      # template specific
      FILE.write('"'+self.template_filename+'" ** TEMPLATE FILENAME\n')
      FILE.write('"'+self.template_source_plane+'" ** TEMPLATE SOURCE PLANE\n')
      FILE.write('"'+self.template_target_plane+'" ** TEMPLATE TARGET PLANE\n')
      FILE.write("%d ** DIRECTION 0=-ve 1=+ve\n" % self.template_direction)
      FILE.write("%d ** ROTATE 0=no, 1=yes\n" % self.template_rotation)
      FILE.write('}\n')
      FILE.write('\n')

  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = sort([self.P1[0],self.P2[0]])
    objy = sort([self.P1[1],self.P2[1]])
    objz = sort([self.P1[2],self.P2[2]])
    eps = 1
    xvec = vstack([xvec,objx])
    yvec = vstack([yvec,objy])
    zvec = vstack([zvec,objz])
    epsx = vstack([epsx,eps])
    epsy = vstack([epsy,eps])
    epsz = vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz
