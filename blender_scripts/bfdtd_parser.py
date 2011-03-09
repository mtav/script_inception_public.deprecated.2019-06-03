#!/usr/bin/env python
# -*- coding: utf-8 -*-
# parses BFDTD files

import math;
import os;
import sys;
import re;

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
        self.iMethod = 0;
        self.propCons = 0;
        self.flagOne = 0;
        self.flagTwo = 0;
        self.numSteps = 0;
        self.stabFactor = 0;
        self.id = '_id_';
    def __str__(self):
        ret = 'iMethod = ' + str(self.iMethod) + '\n' +\
        'propCons = ' + str(self.propCons) + '\n' +\
        'flagOne = ' + str(self.flagOne) + '\n' +\
        'flagTwo = ' + str(self.flagTwo) + '\n' +\
        'numSteps = ' + str(self.numSteps) + '\n' +\
        'stabFactor = ' + str(self.stabFactor) + '\n' +\
        'id = ' + self.id;
        return ret;
    def read_entry(self, entry):
        self.iMethod = float(entry.data[0]);
        self.propCons = float(entry.data[1]);
        self.flagOne = float(entry.data[2]);
        self.flagTwo = float(entry.data[3]);
        self.numSteps = float(entry.data[4]);
        self.stabFactor = float(entry.data[5]);
        self.id = entry.data[6];

class Boundaries:
    def __init__(self):
        self.type = [0,0,0,0,0,0];
        self.position = [0,0,0,0,0,0];
    def __str__(self):
        ret  = 'X+: type = '+str(self.type[0])+' position = '+str(self.position[0])+'\n';
        ret += 'Y+: type = '+str(self.type[1])+' position = '+str(self.position[1])+'\n';
        ret += 'Z+: type = '+str(self.type[2])+' position = '+str(self.position[2])+'\n';
        ret += 'X-: type = '+str(self.type[3])+' position = '+str(self.position[3])+'\n';
        ret += 'Y-: type = '+str(self.type[4])+' position = '+str(self.position[4])+'\n';
        ret += 'Z-: type = '+str(self.type[5])+' position = '+str(self.position[5]);
        return ret;
    def read_entry(self,entry):
        for i in range(6):
            self.type[i] = entry.data[4*i];
            self.position[i] = entry.data[1+4*i:4+4*i];
        return(0);

class Box:
    def __init__(self):
        self.lower = [0,0,0];
        self.upper = [0,0,0];
    def __str__(self):
        ret  = 'lower = '+str(self.lower)+'\n';
        ret += 'upper = '+str(self.upper);
        return ret;
    def read_entry(self,entry):
        self.lower = float_array(entry.data[0:3]);
        self.upper = float_array(entry.data[3:6]);


# geometry objects
class Geometry_object:
    def __init__(self):
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
        self.center = [0,0,0];
        self.outer_radius = 0;
        self.inner_radius = 0;
        self.permittivity = 0;
        self.conductivity = 0;
    def __str__(self):
        ret = 'center = ' + str(self.center) + '\n' +\
        'outer_radius = ' + str(self.outer_radius) + '\n' +\
        'inner_radius = ' + str(self.inner_radius) + '\n' +\
        'permittivity = ' + str(self.permittivity) + '\n' +\
        'conductivity = ' + str(self.conductivity)+'\n';
        ret += Geometry_object.__str__(self)
        return ret;
    def read_entry(self,entry):
        self.center = float_array([entry.data[0],entry.data[1],entry.data[2]]);
        self.outer_radius = float(entry.data[3]);
        self.inner_radius = float(entry.data[4]);
        self.permittivity = float(entry.data[5]);
        self.conductivity = float(entry.data[6]);
        return(0);

class Block(Geometry_object):
    def __init__(self):
        Geometry_object.__init__(self)
        self.lower = [0,0,0];
        self.upper = [0,0,0];
        self.permittivity = 0;
        self.conductivity = 0;
    def __str__(self):
        ret  = 'lower = '+str(self.lower)+'\n';
        ret += 'upper = '+str(self.upper)+'\n';
        ret += 'permittivity = '+str(self.permittivity)+'\n';
        ret += 'conductivity = '+str(self.conductivity)+'\n';
        ret += Geometry_object.__str__(self)
        return ret;
    def read_entry(self,entry):
        self.lower = float_array(entry.data[0:3]);
        self.upper = float_array(entry.data[3:6]);
        self.permittivity = float(entry.data[6]);
        self.conductivity = float(entry.data[7]);

class Cylinder(Geometry_object):
    def __init__(self):
        Geometry_object.__init__(self)
        self.center = [0,0,0];
        self.inner_radius = 0;
        self.outer_radius = 0;
        self.height = 0;
        self.permittivity = 0;
        self.conductivity = 0;
        self.angle = 0;
    def __str__(self):
        ret = 'center = ' + str(self.center) + '\n' +\
        'inner_radius = ' + str(self.inner_radius) + '\n' +\
        'outer_radius = ' + str(self.outer_radius) + '\n' +\
        'height = ' + str(self.height) + '\n' +\
        'permittivity = ' + str(self.permittivity) + '\n' +\
        'conductivity = ' + str(self.conductivity) + '\n' +\
        'angle = ' + str(self.angle) + '\n';
        ret += Geometry_object.__str__(self)
        return ret;
    def read_entry(self,entry):
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
        self.axis_point = [0,0,0];
        self.axis_direction = [0,0,0];
        self.angle_degrees = 0;
    def __str__(self):
        ret = 'axis_point = ' + str(self.axis_point) + '\n';
        ret += 'axis_direction = ' + str(self.axis_direction) + '\n';
        ret += 'angle_degrees = ' + str(self.angle_degrees);
        return ret;
    def read_entry(self,entry):
        self.axis_point = float_array(entry.data[0:3]);
        self.axis_direction = float_array(entry.data[3:6]);
        self.angle_degrees = float(entry.data[6]);
    

# excitation objects
class Excitation:
    def __init__(self):
        self.current_source = 0;
        self.P1 = [0,0,0];
        self.P2 = [0,0,0];
        self.E = 0;
        self.H = 0;
        self.type = 0;
        self.time_constant = 0;
        self.amplitude = 0;
        self.time_offset = 0;
        self.frequency = 0;
        self.param1 = 0;
        self.param2 = 0;
        self.param3 = 0;
        self.param4 = 0;
    def __str__(self):
        ret = 'current_source = ' + str(self.current_source) + '\n' +\
        'P1 = ' + str(self.P1) + '\n' +\
        'P2 = ' + str(self.P2) + '\n' +\
        'E = ' + str(self.E) + '\n' +\
        'H = ' + str(self.H) + '\n' +\
        'type = ' + str(self.type) + '\n' +\
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
        idx = 0;
        self.current_source = float(entry.data[idx]); idx = idx+1;
        self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.type = float(entry.data[idx]); idx = idx+1;
        self.time_constant = float(entry.data[idx]); idx = idx+1;
        self.amplitude = float(entry.data[idx]); idx = idx+1;
        self.time_offset = float(entry.data[idx]); idx = idx+1;
        self.frequency = float(entry.data[idx]); idx = idx+1;
        self.param1 = float(entry.data[idx]); idx = idx+1;
        self.param2 = float(entry.data[idx]); idx = idx+1;
        self.param3 = float(entry.data[idx]); idx = idx+1;
        self.param4 = float(entry.data[idx]); idx = idx+1;
        return(0);


# measurement objects
class Time_snapshot:
    def __init__(self):
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
        ret = 'first = ' + str(self.first) + '\n' +\
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
        idx = 0;
        self.first = float(entry.data[idx]); idx = idx+1;
        self.repetition = float(entry.data[idx]); idx = idx+1;
        self.plane = float(entry.data[idx]); idx = idx+1;
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
        ret = 'first = ' + str(self.first) + '\n' +\
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
        self.position = [0,0,0];
        self.step = 0;
        self.E = [0,0,0];
        self.H = [0,0,0];
        self.J = [0,0,0];
        self.pow = 0;
    def __str__(self):
        ret = 'position = ' + str(self.position) + '\n' +\
        'step = ' + str(self.step) + '\n' +\
        'E = ' + str(self.E) + '\n' +\
        'H = ' + str(self.H) + '\n' +\
        'J = ' + str(self.J) + '\n' +\
        'pow = ' + str(self.pow);
        return ret;
    def read_entry(self,entry):
        self.position = float_array([entry.data[0],entry.data[1],entry.data[2]]);
        self.step = float(entry.data[3]);
        self.E = float_array([entry.data[4],entry.data[5],entry.data[6]]);
        self.H = float_array([entry.data[7],entry.data[8],entry.data[9]]);
        self.J = float_array([entry.data[10],entry.data[11],entry.data[12]]);
        self.pow = float(entry.data[13]);
    


class Entry:
  def __init__(self):
    self.type = '';
    self.data = [];

class Structured_entries:
  def __init__(self):
    # mandatory objects
    self.xmesh = [];
    self.ymesh = [];
    self.zmesh = [];
    self.flag = Flag();
    self.boundaries = Boundaries();
    self.box = Box();
            
    # geometry objects
    self.geometry_object_list = [];
    self.sphere_list = [];
    self.block_list = [];
    self.cylinder_list = [];
    self.global_rotation_list = [];
    
    # excitation objects
    self.excitation_list = [];
    
    # measurement objects
    self.snapshot_list = [];
    self.time_snapshot_list = [];
    self.frequency_snapshot_list = [];
    self.probe_list = [];

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
      pattern_stripcomments = re.compile("\*\*.*\n")
      cleantext = pattern_stripcomments.sub("\n", fulltext);
  
      # pattern_objects = re.compile("^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}");
      pattern_objects = re.compile("(?P<type>\w+)\s*{(?P<data>[^{}]*)}",re.DOTALL)
      objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]
    
      entries = [];
      # process objects
      for i in range(len(objects)):
          type = objects[i]['type'];
          data = objects[i]['data'];
          
          # convert type to upper case and strip it
          type = type.upper().strip();
          # split data by spaces and new lines
          data = re.split('\s+',data);
          # remove empty lines from data
          data = filter(None, data);
          
          entry = Entry();
          entry.type = type;
          entry.data = data;
          entries.append(entry);
          
          # mandatory objects
          if entry.type == 'XMESH':
              self.xmesh = float_array(entry.data);
              xmesh_read = True;
          elif entry.type == 'YMESH':
              self.ymesh = float_array(entry.data);
          elif entry.type == 'ZMESH':
              self.zmesh = float_array(entry.data);
          elif entry.type == 'FLAG':
              self.flag.read_entry(entry);
          elif entry.type == 'BOUNDARY':
              self.boundaries.read_entry(entry);
          elif entry.type == 'BOX':
              self.box.read_entry(entry);
              box_read = True;
                  
          # geometry objects
          elif entry.type == 'SPHERE':
              sphere = Sphere();
              sphere.read_entry(entry);
              self.sphere_list.append(sphere);
              self.geometry_object_list.append(sphere);
          elif entry.type == 'BLOCK':
              block = Block();
              block.read_entry(entry);
              self.block_list.append(block);
              self.geometry_object_list.append(block);
          elif entry.type == 'CYLINDER':
              cylinder = Cylinder();
              cylinder.read_entry(entry);
              self.cylinder_list.append(cylinder);
              self.geometry_object_list.append(cylinder);
          elif entry.type == 'ROTATION':
              rotation = Rotation();
              rotation.read_entry(entry);
              self.global_rotation_list.append(rotation);
              self.geometry_object_list[-1].rotation_list.append(rotation);
          
          # excitation objects
          elif entry.type == 'EXCITATION':
              current_excitation = Excitation();
              current_excitation.read_entry(entry);
              self.excitation_list.append(current_excitation);
          
          # measurement objects
          elif entry.type == 'FREQUENCY_SNAPSHOT':
              frequency_snapshot = Frequency_snapshot();
              frequency_snapshot.read_entry(entry);
              self.frequency_snapshot_list.append(frequency_snapshot);
              self.snapshot_list.append(frequency_snapshot);
          elif entry.type == 'SNAPSHOT':
              time_snapshot = Time_snapshot();
              time_snapshot.read_entry(entry);
              self.time_snapshot_list.append(time_snapshot);
              self.snapshot_list.append(time_snapshot);
          elif entry.type == 'PROBE':
              probe = Probe();
              probe.read_entry(entry);
              self.probe_list.append(probe);
  
          else:
              print 'Unknown type: ', entry.type;

      return [ xmesh_read, box_read ];

  def read_inputs(self,filename):
      ''' read .in file '''
      print '->Processing .in file : ', filename;
      
      box_read = False;
      xmesh_read = False;
      
      f = open(filename, 'r');
      for line in f:
          print 'os.path.dirname(filename): ', os.path.dirname(filename);
          print 'line.strip()=', line.strip();
          subfile = os.path.join(os.path.dirname(filename),os.path.basename(line.strip()));
          print 'subfile: ', subfile;
          if (not xmesh_read):
              subfile = getname(subfile,'inp');
          else:
              subfile = getname(subfile,'geo');
          [ xmesh_read_loc, box_read_loc ] = self.read_input_file(subfile);
          if xmesh_read_loc:
              xmesh_read = True;
          if box_read_loc:
              box_read = True;
      f.close();
      if (not xmesh_read):
          print 'WARNING: mesh not found';
      if (not box_read):
          print 'WARNING: box not found';
    
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
    
    print '================';
    print structured_entries;
    print '================';
    return structured_entries;
    

# for testing
#~ print '----->Importing bristol FDTD geometry...';
#~ structured_entries = readBristolFDTD(sys.argv[1]);
#~ print '...done';
