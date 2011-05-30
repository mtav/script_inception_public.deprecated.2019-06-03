#!/usr/bin/env python
# -*- coding: utf-8 -*-
# parses BFDTD files

import math;
import os;
import sys;
import re;
from utilities.common import *
from bfdtd.bristolFDTD_generator_functions import *

#==== UTILITIES START ====#
def float_array(A):
    ''' convert string array to float array '''
    for i in range(len(A)):
        A[i]=float(A[i]);
    return(A);
  
def int_array(A):
    ''' convert string array to int array '''
    for i in range(len(A)):
        A[i]=int(float(A[i]));
    return(A);


def is_number(s):
    ''' returns true if s can be converted to a float, otherwise false '''
    try:
        float(s)
        return True;
    except ValueError:
        return False;

def getname(filename, default_extension):
    ''' add default_extension if the file does not end in .geo or .inp '''
    
    extension = getExtension(filename);
    if extension == 'geo' or extension == 'inp':
        return filename;
    else:
        return filename + '.' + default_extension;

def getExtension(filename):
    ''' returns extension of filename '''
    return filename.split(".")[-1];

#==== UTILITIES END ====#

#==== CLASSES START ====#

# mandatory objects
class Flag:
    def __init__(self):
        self.name = 'flag'
        self.iMethod = 0;
        self.propCons = 0;
        self.flagOne = 0;
        self.flagTwo = 0;
        self.numSteps = 0;
        self.stabFactor = 0;
        self.id = '_id_';
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'iMethod = ' + str(self.iMethod) + '\n' +\
        'propCons = ' + str(self.propCons) + '\n' +\
        'flagOne = ' + str(self.flagOne) + '\n' +\
        'flagTwo = ' + str(self.flagTwo) + '\n' +\
        'numSteps = ' + str(self.numSteps) + '\n' +\
        'stabFactor = ' + str(self.stabFactor) + '\n' +\
        'id = ' + self.id;
        return ret;
    def read_entry(self, entry):
        if entry.name:
          self.name = entry.name
        self.iMethod = float(entry.data[0]);
        self.propCons = float(entry.data[1]);
        self.flagOne = float(entry.data[2]);
        self.flagTwo = float(entry.data[3]);
        self.numSteps = float(entry.data[4]);
        self.stabFactor = float(entry.data[5]);
        self.id = entry.data[6];

class Boundaries:
    def __init__(self):
        self.name = 'boundary'
        self.Type = [0,0,0,0,0,0];
        self.position = [0,0,0,0,0,0];
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'X+: Type = '+str(self.Type[0])+' position = '+str(self.position[0])+'\n';
        ret += 'Y+: Type = '+str(self.Type[1])+' position = '+str(self.position[1])+'\n';
        ret += 'Z+: Type = '+str(self.Type[2])+' position = '+str(self.position[2])+'\n';
        ret += 'X-: Type = '+str(self.Type[3])+' position = '+str(self.position[3])+'\n';
        ret += 'Y-: Type = '+str(self.Type[4])+' position = '+str(self.position[4])+'\n';
        ret += 'Z-: Type = '+str(self.Type[5])+' position = '+str(self.position[5]);
        return ret;
    def read_entry(self,entry):
        if entry.name:
          self.name = entry.name
        for i in range(6):
            self.Type[i] = entry.data[4*i];
            self.position[i] = entry.data[1+4*i:4+4*i];
        return(0);

class Box:
  def __init__(self):
      self.name = 'box'
      self.layer = 'box'
      self.group = 'box'
      self.lower = [0,0,0];
      self.upper = [0,0,0];
  def __str__(self):
      ret  = 'name = '+self.name+'\n';
      ret += 'lower = '+str(self.lower)+'\n';
      ret += 'upper = '+str(self.upper);
      return ret;
  def read_entry(self,entry):
      if entry.name:
        self.name = entry.name
      self.lower = float_array(entry.data[0:3]);
      self.upper = float_array(entry.data[3:6]);
  def write_entry(self, FILE):
    self.lower, self.upper = fixLowerUpper(self.lower, self.upper)
    FILE.write('BOX  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XL\n" % self.lower[0])
    FILE.write("%E **YL\n" % self.lower[1])
    FILE.write("%E **ZL\n" % self.lower[2])
    FILE.write("%E **XU\n" % self.upper[0])
    FILE.write("%E **YU\n" % self.upper[1])
    FILE.write("%E **ZU\n" % self.upper[2])
    FILE.write('}\n')
    FILE.write('\n')

# geometry objects
class Geometry_object:
    def __init__(self):
        self.name = 'geometry object'
        self.rotation_list = [];
    def __str__(self):
        ret = '--->object rotation_list';
        for i in range(len(self.rotation_list)):
            ret += '\n'
            ret += '-->object rotation '+str(i)+':\n';
            ret += self.rotation_list[i].__str__();
        return(ret)

class Sphere(Geometry_object):
    def __init__(self):
        Geometry_object.__init__(self)
        self.name = 'sphere'
        self.center = [0,0,0];
        self.outer_radius = 0;
        self.inner_radius = 0;
        self.permittivity = 0;
        self.conductivity = 0;
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'center = ' + str(self.center) + '\n' +\
        'outer_radius = ' + str(self.outer_radius) + '\n' +\
        'inner_radius = ' + str(self.inner_radius) + '\n' +\
        'permittivity = ' + str(self.permittivity) + '\n' +\
        'conductivity = ' + str(self.conductivity)+'\n';
        ret += Geometry_object.__str__(self)
        return ret;
    def read_entry(self,entry):
        if entry.name:
          self.name = entry.name
        self.center = float_array([entry.data[0],entry.data[1],entry.data[2]]);
        self.outer_radius = float(entry.data[3]);
        self.inner_radius = float(entry.data[4]);
        self.permittivity = float(entry.data[5]);
        self.conductivity = float(entry.data[6]);
        return(0);

class Block(Geometry_object):
  def __init__(self):
      Geometry_object.__init__(self)

      self.name = 'block'
      self.layer = 'block'
      self.group = 'block'

      self.lower = [0,0,0];
      self.upper = [0,0,0];
      self.permittivity = 0;
      self.conductivity = 0;
  def __str__(self):
      ret  = 'name = '+self.name+'\n';
      ret += 'lower = '+str(self.lower)+'\n';
      ret += 'upper = '+str(self.upper)+'\n';
      ret += 'permittivity = '+str(self.permittivity)+'\n';
      ret += 'conductivity = '+str(self.conductivity)+'\n';
      ret += Geometry_object.__str__(self)
      return ret;
  def read_entry(self,entry):
      if entry.name:
        self.name = entry.name
      self.lower = float_array(entry.data[0:3]);
      self.upper = float_array(entry.data[3:6]);
      self.permittivity = float(entry.data[6]);
      self.conductivity = float(entry.data[7]);
  def write_entry(self, FILE):
    self.lower, self.upper = fixLowerUpper(self.lower, self.upper)
    FILE.write('BLOCK **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XL\n" % self.lower[0])
    FILE.write("%E **YL\n" % self.lower[1])
    FILE.write("%E **ZL\n" % self.lower[2])
    FILE.write("%E **XU\n" % self.upper[0])
    FILE.write("%E **YU\n" % self.upper[1])
    FILE.write("%E **ZU\n" % self.upper[2])
    FILE.write("%E **relative Permittivity\n" % self.permittivity)
    FILE.write("%E **Conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')

class Cylinder(Geometry_object):
    def __init__(self):
        Geometry_object.__init__(self)
        self.name = 'cylinder'
        self.center = [0,0,0];
        self.inner_radius = 0;
        self.outer_radius = 0;
        self.height = 0;
        self.permittivity = 0;
        self.conductivity = 0;
        self.angle = 0;
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'center = ' + str(self.center) + '\n' +\
        'inner_radius = ' + str(self.inner_radius) + '\n' +\
        'outer_radius = ' + str(self.outer_radius) + '\n' +\
        'height = ' + str(self.height) + '\n' +\
        'permittivity = ' + str(self.permittivity) + '\n' +\
        'conductivity = ' + str(self.conductivity) + '\n' +\
        'angle = ' + str(self.angle) + '\n';
        ret += Geometry_object.__str__(self)
        return ret;
    def read_entry(self,entry):
        if entry.name:
          self.name = entry.name
        self.center = float_array([entry.data[0],entry.data[1],entry.data[2]]);
        self.inner_radius = float(entry.data[3]);
        self.outer_radius = float(entry.data[4]);
        self.height = float(entry.data[5]);
        self.permittivity = float(entry.data[6]);
        self.conductivity = float(entry.data[7]);
        if(len(entry.data)>8): self.angle = float(entry.data[8]);
        return(0);

class Rotation:
    def __init__(self):
        self.name = 'rotation'
        self.axis_point = [0,0,0];
        self.axis_direction = [0,0,0];
        self.angle_degrees = 0;
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'axis_point = ' + str(self.axis_point) + '\n';
        ret += 'axis_direction = ' + str(self.axis_direction) + '\n';
        ret += 'angle_degrees = ' + str(self.angle_degrees);
        return ret;
    def read_entry(self,entry):
        if entry.name:
          self.name = entry.name
        self.axis_point = float_array(entry.data[0:3]);
        self.axis_direction = float_array(entry.data[3:6]);
        self.angle_degrees = float(entry.data[6]);
    

# excitation objects
class Excitation:
  def __init__(self,
                name = 'excitation',
                current_source = 0,
                P1 = [0,0,0],
                P2 = [0,0,0],
                E = [0,0,0],
                H = [0,0,0],
                Type = 0,
                time_constant = 0,
                amplitude = 0,
                time_offset = 0,
                frequency = 0,
                param1 = 0,
                param2 = 0,
                param3 = 0,
                param4 = 0):
    self.name = name
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
    self.param3 = param3
    self.param4 = param4
  def __str__(self):
    ret  = 'name = '+self.name+'\n';
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
    'param3 = ' + str(self.param3) + '\n' +\
    'param4 = ' + str(self.param4);
    return ret;
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    idx = 0;
    self.current_source = float(entry.data[idx]); idx = idx+1;
    self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
    self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
    self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
    self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
    self.Type = float(entry.data[idx]); idx = idx+1;
    self.time_constant = float(entry.data[idx]); idx = idx+1;
    self.amplitude = float(entry.data[idx]); idx = idx+1;
    self.time_offset = float(entry.data[idx]); idx = idx+1;
    self.frequency = float(entry.data[idx]); idx = idx+1;
    self.param1 = float(entry.data[idx]); idx = idx+1;
    self.param2 = float(entry.data[idx]); idx = idx+1;
    self.param3 = float(entry.data[idx]); idx = idx+1;
    self.param4 = float(entry.data[idx]); idx = idx+1;
    return(0);
  def write_entry(self, FILE):
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
    FILE.write("%d **UNUSED PARAMETER\n" % self.param3)
    FILE.write("%d **UNUSED PARAMETER\n" % self.param4)
    FILE.write('}\n')
    FILE.write('\n')

# measurement objects
class Time_snapshot:
    def __init__(self):
        self.name = 'time snapshot'
        self.first = 0;
        self.repetition = 0;
        self.plane = 0;
        self.P1 = 0;
        self.P2 = 0;
        self.E = 0;
        self.H = 0;
        self.J = 0;
        self.power = 0;
        self.eps = 0;
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'first = ' + str(self.first) + '\n' +\
        'repetition = ' + str(self.repetition) + '\n' +\
        'plane = ' + str(self.plane) + '\n' +\
        'P1 = ' + str(self.P1) + '\n' +\
        'P2 = ' + str(self.P2) + '\n' +\
        'E = ' + str(self.E) + '\n' +\
        'H = ' + str(self.H) + '\n' +\
        'J = ' + str(self.J) + '\n' +\
        'power = ' + str(self.power) + '\n' +\
        'eps = ' + str(self.eps);
        return ret;
    def read_entry(self,entry):
        if entry.name:
          self.name = entry.name
        idx = 0;
        if entry.name:
          self.name = entry.name
        self.first = float(entry.data[idx]); idx = idx+1;
        self.repetition = float(entry.data[idx]); idx = idx+1;
        self.plane = int(float(entry.data[idx])); idx = idx+1;
        self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.power = float(entry.data[idx]); idx = idx+1;
        if(len(entry.data)>idx): self.eps = int(float(entry.data[idx])); idx = idx+1;
        return(0);

class Frequency_snapshot:
    def __init__(self):
        self.name = 'frequency snapshot'
        self.first = 0;
        self.repetition = 0;
        self.interpolate = 0;
        self.real_dft = 0;
        self.mod_only = 0;
        self.mod_all = 0;
        self.plane = 0;
        self.P1 = 0;
        self.P2 = 0;
        self.frequency = 0;
        self.starting_sample = 0;
        self.E = 0;
        self.H = 0;
        self.J = 0;
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'first = ' + str(self.first) + '\n' +\
        'repetition = ' + str(self.repetition) + '\n' +\
        'interpolate = ' + str(self.interpolate) + '\n' +\
        'real_dft = ' + str(self.real_dft) + '\n' +\
        'mod_only = ' + str(self.mod_only) + '\n' +\
        'mod_all = ' + str(self.mod_all) + '\n' +\
        'plane = ' + str(self.plane) + '\n' +\
        'P1 = ' + str(self.P1) + '\n' +\
        'P2 = ' + str(self.P2) + '\n' +\
        'frequency = ' + str(self.frequency) + '\n' +\
        'starting_sample = ' + str(self.starting_sample) + '\n' +\
        'E = ' + str(self.E) + '\n' +\
        'H = ' + str(self.H) + '\n' +\
        'J = ' + str(self.J);
        return ret;
    def read_entry(self,entry):
        if entry.name:
          self.name = entry.name
        idx = 0;
        self.first = float(entry.data[idx]); idx = idx+1;
        self.repetition = float(entry.data[idx]); idx = idx+1;
        self.interpolate = float(entry.data[idx]); idx = idx+1;
        self.real_dft = float(entry.data[idx]); idx = idx+1;
        self.mod_only = float(entry.data[idx]); idx = idx+1;
        self.mod_all = float(entry.data[idx]); idx = idx+1;
        self.plane = int(float(entry.data[idx])); idx = idx+1;
        self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.frequency = float(entry.data[idx]); idx = idx+1;
        self.starting_sample = float(entry.data[idx]); idx = idx+1;
        self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        return(0);

class Probe:
    def __init__(self):
        self.name = 'probe'
        self.position = [0,0,0]
        self.step = 0
        self.E = [0,0,0]
        self.H = [0,0,0]
        self.J = [0,0,0]
        self.pow = 0
    def __str__(self):
        ret  = 'name = '+self.name+'\n';
        ret += 'position = ' + str(self.position) + '\n' +\
        'step = ' + str(self.step) + '\n' +\
        'E = ' + str(self.E) + '\n' +\
        'H = ' + str(self.H) + '\n' +\
        'J = ' + str(self.J) + '\n' +\
        'pow = ' + str(self.pow)
        return ret;
    def read_entry(self,entry):
        if entry.name:
          self.name = entry.name
        self.position = float_array([entry.data[0],entry.data[1],entry.data[2]])
        self.step = float(entry.data[3])
        self.E = float_array([entry.data[4],entry.data[5],entry.data[6]])
        self.H = float_array([entry.data[7],entry.data[8],entry.data[9]])
        self.J = float_array([entry.data[10],entry.data[11],entry.data[12]])
        self.pow = float(entry.data[13])

class Entry:
  def __init__(self):
    self.name = 'default_entry'
    self.layer = 'default_layer'
    self.scene = 'default_scene'
    self.group = 'default_group'
    self.Type = ''
    self.data = []

class Structured_entries:
  def __init__(self):
    # mandatory objects
    self.xmesh = []
    self.ymesh = []
    self.zmesh = []
    self.flag = Flag()
    self.boundaries = Boundaries()
    self.box = Box()
            
    # geometry objects
    self.geometry_object_list = []
    self.sphere_list = []
    self.block_list = []
    self.cylinder_list = []
    self.global_rotation_list = []
    
    # excitation objects
    self.excitation_list = []
    
    # measurement objects
    self.snapshot_list = [];
    self.time_snapshot_list = [];
    self.frequency_snapshot_list = [];
    self.probe_list = [];

    # special
    self.fileList = []
    
  def __str__(self):
      ret = '--->snapshot_list\n';
      for i in range(len(self.snapshot_list)):
          ret += '-->snapshot '+str(i)+':\n';
          ret += self.snapshot_list[i].__str__()+'\n';

      ret += '--->time_snapshot_list\n';
      for i in range(len(self.time_snapshot_list)):
          ret += '-->time_snapshot '+str(i)+':\n';
          ret += self.time_snapshot_list[i].__str__()+'\n';

      ret += '--->frequency_snapshot_list\n';
      for i in range(len(self.frequency_snapshot_list)):
          ret += '-->frequency_snapshot '+str(i)+':\n';
          ret += self.frequency_snapshot_list[i].__str__()+'\n';

      ret += '--->excitation_list\n';
      for i in range(len(self.excitation_list)):
          ret += '-->excitation '+str(i)+':\n';
          ret += self.excitation_list[i].__str__()+'\n';
      
      ret += '--->xmesh\n'+self.xmesh.__str__()+'\n'+\
      '--->ymesh\n'+self.ymesh.__str__()+'\n'+\
      '--->zmesh\n'+self.zmesh.__str__()+'\n'+\
      '--->flag\n'+self.flag.__str__()+'\n'+\
      '--->boundaries\n'+self.boundaries.__str__()+'\n'+\
      '--->box\n'+self.box.__str__()+'\n';
      
      ret += '--->probe_list\n';
      for i in range(len(self.probe_list)):
          ret += '-->probe '+str(i)+':\n';
          ret += self.probe_list[i].__str__()+'\n';

      ret += '--->sphere_list\n';
      for i in range(len(self.sphere_list)):
          ret += '-->sphere '+str(i)+':\n';
          ret += self.sphere_list[i].__str__()+'\n';
      
      ret += '--->block_list\n';
      for i in range(len(self.block_list)):
          ret += '-->block '+str(i)+':\n';
          ret += self.block_list[i].__str__()+'\n';

      ret += '--->cylinder_list\n';
      for i in range(len(self.cylinder_list)):
          ret += '-->cylinder '+str(i)+':\n';
          ret += self.cylinder_list[i].__str__()+'\n';

      ret += '--->global_rotation_list\n';
      for i in range(len(self.global_rotation_list)):
          # ret += '\n';
          ret += '-->rotation '+str(i)+':\n';
          ret += self.global_rotation_list[i].__str__()+'\n';

      ret += '--->geometry_object_list\n';
      for i in range(len(self.geometry_object_list)):
          ret += '-->geometry_object '+str(i)+':\n';
          ret += self.geometry_object_list[i].__str__()+'\n';
          
      return ret;

  def read_input_file(self,filename):
      ''' read GEO or INP file '''
      print 'Processing ', filename;
      box_read = False;
      xmesh_read = False;
      
      # open file
      input = open(filename);
      # read the whole file as one string
      fulltext = input.read();
      # close file
      input.close();
  
      # print fulltext;
  
      # remove comments
      # TODO: Add more generic system for functional comments (to add layer, scene and group for example)
      pattern_stripcomments = re.compile("\*\*(?!name=).*\n")
      cleantext = pattern_stripcomments.sub("\n", fulltext)
      #print(cleantext)
  
      # pattern_objects = re.compile("^(?<Type>\w+).*?\{(?<data>[^\{\}]*?)\}");
      #pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<name>(?<=\*\*name=)[^{}]*)?{(?P<data>[^{}]*)}",re.DOTALL)
      pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<nameblob>[^{}]+)?{(?P<data>[^{}]*)}",re.DOTALL)
      objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]
    
      entries = [];
      # process objects
      for i in range(len(objects)):
          Type = objects[i]['Type'];
          name = ''
          if 'nameblob' in objects[i].keys():
            #print objects[i]['nameblob']
            if objects[i]['nameblob']:
              #print 'OK'
              pattern_nameblob = re.compile("\*\*name=(.*)")
              m = pattern_nameblob.match(objects[i]['nameblob'])
              if m:
                name = m.group(1).strip()
            #else:
              #print 'NOT OK'
              #name = ''
          #else:
            #print 'NO NAME'
            #name = ''
          data = objects[i]['data'];
          
          # convert Type to upper case and strip it
          Type = Type.upper().strip();
          # split data by spaces and new lines
          data = re.split('\s+',data);
          # remove empty lines from data
          data = filter(None, data);
          
          entry = Entry();
          entry.Type = Type;
          entry.name = name;
          entry.data = data;
          entries.append(entry);
          
          # mandatory objects
          if entry.Type == 'XMESH':
              self.xmesh = float_array(entry.data);
              xmesh_read = True;
          elif entry.Type == 'YMESH':
              self.ymesh = float_array(entry.data);
          elif entry.Type == 'ZMESH':
              self.zmesh = float_array(entry.data);
          elif entry.Type == 'FLAG':
              self.flag.read_entry(entry);
          elif entry.Type == 'BOUNDARY':
              self.boundaries.read_entry(entry);
          elif entry.Type == 'BOX':
              self.box.read_entry(entry);
              box_read = True;
                  
          # geometry objects
          elif entry.Type == 'SPHERE':
              sphere = Sphere();
              sphere.read_entry(entry);
              self.sphere_list.append(sphere);
              self.geometry_object_list.append(sphere);
          elif entry.Type == 'BLOCK':
              block = Block();
              block.read_entry(entry);
              self.block_list.append(block);
              self.geometry_object_list.append(block);
          elif entry.Type == 'CYLINDER':
              cylinder = Cylinder();
              cylinder.read_entry(entry);
              self.cylinder_list.append(cylinder);
              self.geometry_object_list.append(cylinder);
          elif entry.Type == 'ROTATION':
              rotation = Rotation();
              rotation.read_entry(entry);
              self.global_rotation_list.append(rotation);
              self.geometry_object_list[-1].rotation_list.append(rotation);
          
          # excitation objects
          elif entry.Type == 'EXCITATION':
              current_excitation = Excitation();
              current_excitation.read_entry(entry);
              self.excitation_list.append(current_excitation);
          
          # measurement objects
          elif entry.Type == 'FREQUENCY_SNAPSHOT':
              frequency_snapshot = Frequency_snapshot();
              frequency_snapshot.read_entry(entry);
              self.frequency_snapshot_list.append(frequency_snapshot);
              self.snapshot_list.append(frequency_snapshot);
          elif entry.Type == 'SNAPSHOT':
              time_snapshot = Time_snapshot();
              time_snapshot.read_entry(entry);
              self.time_snapshot_list.append(time_snapshot);
              self.snapshot_list.append(time_snapshot);
          elif entry.Type == 'PROBE':
              probe = Probe();
              probe.read_entry(entry);
              self.probe_list.append(probe);
  
          else:
              print 'Unknown Type: ', entry.Type;

      return [ xmesh_read, box_read ];

  def read_inputs(self,filename):
      ''' read .in file '''
      print '->Processing .in file : ', filename;
      
      box_read = False;
      xmesh_read = False;
      
      f = open(filename, 'r');
      for line in f:
          print 'os.path.dirname(filename): ', os.path.dirname(filename) # directory of .in file
          print 'line.strip()=', line.strip() # remove any \n or similar
          self.fileList.append(line.strip())
          # this is done so that you don't have to be in the directory containing the .geo/.inp files
          subfile = os.path.join(os.path.dirname(filename),os.path.basename(line.strip()))
          print 'subfile: ', subfile
          if (not xmesh_read): # as long as the mesh hasn't been read, .inp is assumed as the default extension
              subfile = getname(subfile,'inp')
          else:
              subfile = getname(subfile,'geo')
          [ xmesh_read_loc, box_read_loc ] = self.read_input_file(subfile)
          if xmesh_read_loc:
              xmesh_read = True
          if box_read_loc:
              box_read = True
      f.close();
      if (not xmesh_read):
          print 'WARNING: mesh not found';
      if (not box_read):
          print 'WARNING: box not found';
  
  def writeGeoFile(self,fileName):
    ''' Generate .geo file '''
    # open file
    with open(fileName, 'w') as out:
  
      # write header
      out.write('**GEOMETRY FILE\n')
      out.write('\n')

      # write geometry objects
      print 'len(self.geometry_object_list) = ', len(self.geometry_object_list)
      for obj in self.geometry_object_list:
        print obj.name
        print obj.__class__.__name__
        obj.write_entry(out)

      #write box
      self.box.write_entry(out)
      
      # write footer
      out.write('end\n'); #end the file
    
      # close file
      out.close()

    return

        

    
  def writeInpFile(self,fileName):
    ''' Generate .inp file '''
    return
    
  def writeFileList(self,fileName,fileList=None):
    ''' Generate .in file '''
    # leaving it external at the moment since it might be practical to use it without having to create a Bfdtd object
    if fileList is None:
      fileList = self.fileList
    print fileName
    print fileList
    GEOin(fileName,fileList)
    return
    
  def writeCondorScript(self,fileName, BASENAME=None):
    ''' Generate fileName.cmd file for Condor using BASENAME.in, BASENAME.geo, BASENAME.inp '''
    # leaving it external at the moment since it might be practical to use it without having to create a Bfdtd object
    if BASENAME is None:
      BASENAME = os.path.splitext(os.path.basename(fileName))[0]
    GEOcommand(fileName, BASENAME)
    return
    
  def writeShellScript(self,fileName, BASENAME=None, EXE='fdtd', WORKDIR='$JOBDIR', WALLTIME=12):
    ''' Generate .sh file '''
    if BASENAME is None:
      BASENAME = os.path.splitext(os.path.basename(fileName))[0]
    GEOshellscript(fileName, BASENAME, EXE, WORKDIR, WALLTIME)
    #probe_col = 0
    #if self.excitation.E == [1,0,0]:
      #probe_col = 2
    #elif self.excitation.E == [0,1,0]:
      #probe_col = 3
    #elif self.excitation.E == [0,0,1]:
      #probe_col = 4
    #else:
      #print('ERROR : Unknown Excitation type')
      #sys.exit(-1)
    #GEOshellscript_advanced(fileName, BASENAME, probe_col, EXE, WORKDIR, WALLTIME)
    return
    
  def writeAll(self, newDirName, fileBaseName=None):
    ''' Generate .in,.inp,.geo,.cmd,.sh files in directory newDirName (it will be created if it doesn't exist)'''
    newDirName = os.path.expanduser(newDirName).rstrip('/') # replace ~ or similar and remove any trailing '/'
    if not os.path.isdir(newDirName):
      os.mkdir(newDirName)

    if fileBaseName is None:
      fileBaseName = os.path.basename(newDirName)
    
    
    print 'fileBaseName = ', fileBaseName
    
    geoFileName = newDirName+os.sep+fileBaseName+'.geo'
    inpFileName = newDirName+os.sep+fileBaseName+'.inp'
    inFileName = newDirName+os.sep+fileBaseName+'.in'
    cmdFileName = newDirName+os.sep+fileBaseName+'.cmd'
    shFileName = newDirName+os.sep+fileBaseName+'.sh'

    if self.fileList is None:
      self.fileList = [fileBaseName+'.inp',fileBaseName+'.geo']
    
    self.writeGeoFile(geoFileName)
    self.writeInpFile(inpFileName)
    self.writeFileList(inFileName,self.fileList)
    #self.writeCondorScript(cmdFileName)
    #self.writeShellScript(shFileName)
    
#==== CLASSES END ====#

def readBristolFDTD(filename):
    ''' reads .in (=>.inp+.geo), .geo or .inp '''
    print '->Processing generic file : ', filename;

    structured_entries = Structured_entries();
    
    extension = getExtension(filename);
    if extension == 'in':
        print '.in file detected';
        structured_entries.read_inputs(filename);
    elif extension == 'inp':
        print '.inp file detected';
        structured_entries.read_input_file(filename);
    elif extension == 'geo':
        print '.geo file detected';
        structured_entries.read_input_file(filename);
    elif extension == 'prn':
        print '.prn file detected: Not supported yet';
    else:
        print 'Unknown file format:', extension;
        sys.exit(-1)
    
    #~ print '================';
    #~ print structured_entries;
    #~ print '================';
    return structured_entries;
    
def TestWriting():
    # more code, unchanged
    with open('tmp.txt', 'w') as FILE:
      delta_X_vector = [11.25,21.25,31.25]
      delta_Y_vector = [12.25,22.25,32.25]
      delta_Z_vector = [13.25,23.25,33.25]
      COMMENT = 'example comment'
      GEOmesh(FILE, COMMENT, delta_X_vector, delta_Y_vector, delta_Z_vector)
      GEOflag(FILE, COMMENT, 70, 12.34, 24, 42, 1000, 0.755025, '_id_')
      GEOboundary(FILE, COMMENT, 1.2, [3.4,3.4,3.4],\
                                  5.6, [7.8,7.8,6.2],\
                                  9.10, [11.12,1,2],\
                                  13.14, [15.16,3,4],\
                                  17.18, [19.20,5,6],\
                                  21.22, [23.24,7.8,5.4])
      GEObox(FILE, COMMENT, [1.2,3.4,5.6], [9.8,7.6,5.4])
      GEOsphere(FILE, COMMENT, [1,2,3], 9, 8, 7, 6)
      GEOblock(FILE, COMMENT, [1.1,2.2,3.3], [4.4,5.5,6.6], 600, 700)
      GEOcylinder(FILE, COMMENT, [1.2,3.4,5.6], 77, 88, 99, 100, 0.02, 47.42)
      GEOrotation(FILE, COMMENT, [1,2,3], [4,5,6], 56)
      excitation_obj = Excitation(COMMENT, 77, [1,2,3], [4,5,6], [7,8,9], [77,88,99], 69, 12.36, 45.54, 78.87, 456, 1, 22, 333, 4444)
      excitation_obj.write_entry(FILE)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'x', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'y', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'z', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'x', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'y', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'z', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOfrequency_snapshot(FILE, COMMENT, 369, 852, 147, 258, 369, 987, 'x', [1,2,3], [1,2,3], [852,741,963], 147, [7,8,9],[4,5,6],[1,2,3])
      GEOprobe(FILE, COMMENT, [1,2,3], 56, [5,6,7], [5,6,7], [5,6,7], 4564654 )
      GEOcommand('tmp.bat', 'BASENAME')
      GEOin('tmp.in', ['file','list'])
      GEOshellscript('tmp.sh', 'BASENAME', '/usr/bin/superexe', '/work/todo', 999)
  
def main(argv=None):
  if argv is None:
      argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
      raise Usage(msg)
    # main function
    # for testing
    print '----->Importing bristol FDTD geometry...';
    structured_entries = readBristolFDTD(sys.argv[1]);
    print structured_entries
    print '...done';
    
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
