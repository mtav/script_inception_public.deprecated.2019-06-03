#!BPY

"""
Name: 'Bristol FDTD (*.geo)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from Bristol FDTD'
"""

import math;
import os;
import sys;
import re;

def float_array(A):
    for i in range(len(A)):
        A[i]=float(A[i]);
    return(A);
    
def int_array(A):
    for i in range(len(A)):
        A[i]=int(A[i]);
    return(A);

class Entry:
    def __init__(self):
        self.type = '';
        self.data = [];

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
    def __str__(self):
        ret = 'first = ' + str(self.first) + '\n' +\
        'repetition = ' + str(self.repetition) + '\n' +\
        'plane = ' + str(self.plane) + '\n' +\
        'P1 = ' + str(self.P1) + '\n' +\
        'P2 = ' + str(self.P2) + '\n' +\
        'E = ' + str(self.E) + '\n' +\
        'H = ' + str(self.H) + '\n' +\
        'J = ' + str(self.J) + '\n' +\
        'power = ' + str(self.power);
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
        self.plane = float(entry.data[idx]); idx = idx+1;
        self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.frequency = float(entry.data[idx]); idx = idx+1;
        self.starting_sample = float(entry.data[idx]); idx = idx+1;
        self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
        return(0);

# class Snapshot:
    # def __init__(self):
        # self.first = 0;
        # self.repetition = 0;
        # self.interpolate = 0;
        # self.real_dft = 0;
        # self.mod_only = 0;
        # self.mod_all = 0;
        # self.plane = 0;
        # self.P1 = 0;
        # self.P2 = 0;
        # self.frequency = 0;
        # self.starting_sample = 0;
        # self.E = 0;
        # self.H = 0;
        # self.J = 0;
        # self.power = 0;
    # def __str__(self):
        # ret = 'first = ' + str(self.first) + '\n' +\
        # 'repetition = ' + str(self.repetition) + '\n' +\
        # 'interpolate = ' + str(self.interpolate) + '\n' +\
        # 'real_dft = ' + str(self.real_dft) + '\n' +\
        # 'mod_only = ' + str(self.mod_only) + '\n' +\
        # 'mod_all = ' + str(self.mod_all) + '\n' +\
        # 'plane = ' + str(self.plane) + '\n' +\
        # 'P1 = ' + str(self.P1) + '\n' +\
        # 'P2 = ' + str(self.P2) + '\n' +\
        # 'frequency = ' + str(self.frequency) + '\n' +\
        # 'starting_sample = ' + str(self.starting_sample) + '\n' +\
        # 'E = ' + str(self.E) + '\n' +\
        # 'H = ' + str(self.H) + '\n' +\
        # 'J = ' + str(self.J) + '\n' +\
        # 'power = ' + str(self.power);
        # return ret;
    # def read_entry(self,entry):
        # if entry.type == 'FREQUENCY_SNAPSHOT':
            # idx = 0;
            # self.first = float(entry.data[idx]); idx = idx+1;
            # self.repetition = float(entry.data[idx]); idx = idx+1;
            # self.interpolate = float(entry.data[idx]); idx = idx+1;
            # self.real_dft = float(entry.data[idx]); idx = idx+1;
            # self.mod_only = float(entry.data[idx]); idx = idx+1;
            # self.mod_all = float(entry.data[idx]); idx = idx+1;
            # self.plane = float(entry.data[idx]); idx = idx+1;
            # self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.frequency = float(entry.data[idx]); idx = idx+1;
            # self.starting_sample = float(entry.data[idx]); idx = idx+1;
            # self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.power = -1;
        # elif entry.type == 'SNAPSHOT':
            # idx = 0;
            # self.first = float(entry.data[idx]); idx = idx+1;
            # self.repetition = float(entry.data[idx]); idx = idx+1;
            # self.interpolate = -1;
            # self.real_dft = -1;
            # self.mod_only = -1;
            # self.mod_all = -1;
            # self.plane = float(entry.data[idx]); idx = idx+1;
            # self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.frequency = -1;
            # self.starting_sample = -1;
            # self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3;
            # self.power = float(entry.data[idx]); idx = idx+1;
        # else:
            # print 'Sense, it makes none.'; sys.exit(-1);
        # return(0);

class Excitation:
    def __init__(self):
        self.current_source = 0;
        self.P1 = 0;
        self.P2 = 0;
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

class Boundaries:
    def __init__(self):
        self.type = [0,0,0,0,0,0];
        self.p = [0,0,0,0,0,0];
    def __str__(self):
        ret  = 'X+: type = '+str(self.type[0])+' p = '+str(self.p[0])+'\n';
        ret += 'Y+: type = '+str(self.type[1])+' p = '+str(self.p[1])+'\n';
        ret += 'Z+: type = '+str(self.type[2])+' p = '+str(self.p[2])+'\n';
        ret += 'X-: type = '+str(self.type[3])+' p = '+str(self.p[3])+'\n';
        ret += 'Y-: type = '+str(self.type[4])+' p = '+str(self.p[4])+'\n';
        ret += 'Z-: type = '+str(self.type[5])+' p = '+str(self.p[5]);
        return ret;
    def read_entry(self,entry):
        # print '===entry_to_boundary START==='
        # print entry.type;
        # print entry.data;
        for i in range(6):
            self.type[i] = entry.data[4*i];
            self.p[i] = entry.data[1+4*i:4+4*i];
        # print self.type[i];
        # print self.p[i];
        # print '===entry_to_boundary END==='
        return(0);

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

class Block:
    def __init__(self):
        self.lower = [0,0,0];
        self.upper = [0,0,0];
        self.permittivity = 0;
        self.conductivity = 0;
    def __str__(self):
        ret  = 'lower = '+str(self.lower)+'\n';
        ret += 'upper = '+str(self.upper)+'\n';
        ret += 'permittivity = '+str(self.permittivity)+'\n';
        ret += 'conductivity = '+str(self.conductivity);
        return ret;
    def read_entry(self,entry):
        self.lower = float_array(entry.data[0:3]);
        self.upper = float_array(entry.data[3:6]);
        self.permittivity = float(entry.data[6]);
        self.conductivity = float(entry.data[7]);

class Sphere:
    def __init__(self):
        self.XC = 0;
        self.YC = 0;
        self.ZC = 0;
        self.R1 = 0;
        self.R2 = 0;
        self.permittivity = 0;
        self.conductivity = 0;
    def __str__(self):
        ret = 'XC = ' + str(self.XC) + '\n' +\
        'YC = ' + str(self.YC) + '\n' +\
        'ZC = ' + str(self.ZC) + '\n' +\
        'R1 = ' + str(self.R1) + '\n' +\
        'R2 = ' + str(self.R2) + '\n' +\
        'permittivity = ' + str(self.permittivity) + '\n' +\
        'conductivity = ' + str(self.conductivity);
        return ret;
    def read_entry(self,entry):
        self.XC = float(entry.data[0]);
        self.YC = float(entry.data[1]);
        self.ZC = float(entry.data[2]);
        self.R1 = float(entry.data[3]);
        self.R2 = float(entry.data[4]);
        self.permittivity = float(entry.data[5]);
        self.conductivity = float(entry.data[6]);
        return(0);

class Cylinder:
    def __init__(self):
        self.Xc = 0;
        self.Yc = 0;
        self.Zc = 0;
        self.R1 = 0;
        self.R2 = 0;
        self.height = 0;
        self.permittivity = 0;
        self.conductivity = 0;
        self.angle = 0;
    def __str__(self):
        ret = 'Xc = ' + str(self.Xc) + '\n' +\
        'Yc = ' + str(self.Yc) + '\n' +\
        'Zc = ' + str(self.Zc) + '\n' +\
        'R1 = ' + str(self.R1) + '\n' +\
        'R2 = ' + str(self.R2) + '\n' +\
        'height = ' + str(self.height) + '\n' +\
        'permittivity = ' + str(self.permittivity) + '\n' +\
        'conductivity = ' + str(self.conductivity) + '\n' +\
        'angle = ' + str(self.angle);
        return ret;
    def read_entry(self,entry):
        # print entry.data;
        self.Xc = float(entry.data[0]);
        self.Yc = float(entry.data[1]);
        self.Zc = float(entry.data[2]);
        self.R1 = float(entry.data[3]);
        self.R2 = float(entry.data[4]);
        self.height = float(entry.data[5]);
        self.permittivity = float(entry.data[6]);
        self.conductivity = float(entry.data[7]);
        if(len(entry.data)>8): self.angle = float(entry.data[8]);
        return(0);

class Probe:
    def __init__(self):
        self.X = 0;
        self.Y = 0;
        self.Z = 0;
        self.step = 0;
        self.Ex = 0;
        self.Ey = 0;
        self.Ez = 0;
        self.Hx = 0;
        self.Hy = 0;
        self.Hz = 0;
        self.Jx = 0;
        self.Jy = 0;
        self.Jz = 0;
        self.pow = 0;
    def __str__(self):
        ret = 'X = ' + str(self.X) + '\n' +\
        'Y = ' + str(self.Y) + '\n' +\
        'Z = ' + str(self.Z) + '\n' +\
        'step = ' + str(self.step) + '\n' +\
        'Ex = ' + str(self.Ex) + '\n' +\
        'Ey = ' + str(self.Ey) + '\n' +\
        'Ez = ' + str(self.Ez) + '\n' +\
        'Hx = ' + str(self.Hx) + '\n' +\
        'Hy = ' + str(self.Hy) + '\n' +\
        'Hz = ' + str(self.Hz) + '\n' +\
        'Jx = ' + str(self.Jx) + '\n' +\
        'Jy = ' + str(self.Jy) + '\n' +\
        'Jz = ' + str(self.Jz) + '\n' +\
        'pow = ' + str(self.pow);
        return ret;
    def read_entry(self,entry):
        self.X = float(entry.data[0]);
        self.Y = float(entry.data[1]);
        self.Z = float(entry.data[2]);
        self.step = float(entry.data[3]);
        self.Ex = float(entry.data[4]);
        self.Ey = float(entry.data[5]);
        self.Ez = float(entry.data[6]);
        self.Hx = float(entry.data[7]);
        self.Hy = float(entry.data[8]);
        self.Hz = float(entry.data[9]);
        self.Jx = float(entry.data[10]);
        self.Jy = float(entry.data[11]);
        self.Jz = float(entry.data[12]);
        self.pow = float(entry.data[13]);
    
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
    
class Structured_entries:
    def __init__(self):
        self.snapshot_list = [];
        self.time_snapshot_list = [];
        self.frequency_snapshot_list = [];
        self.excitation_list = [];
        self.xmesh = [];
        self.ymesh = [];
        self.zmesh = [];
        self.flag = Flag();
        self.boundaries = Boundaries();
        self.box = [];
        self.probe_list = [];
        self.sphere_list = [];
        self.block_list = [];
        self.cylinder_list = [];
        self.rotation_list = [];
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
        '--->box\n'+self.box.__str__();
        
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

        ret += '--->rotation_list';
        for i in range(len(self.rotation_list)):
            ret += '\n';
            ret += '-->rotation '+str(i)+':\n';
            ret += self.rotation_list[i].__str__();
            
        return ret;

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_input_file(filename, structured_entries):
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

    # print cleantext;
    
	# extract objects
    # pattern_objects = re.compile("^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}");
    pattern_objects = re.compile("(?P<type>\w+)\s*{(?P<data>[^{}]*)}",re.DOTALL)
    objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]

    # [tokens_objects match_objects names_objects] =  regexp(cleantext, pattern_objects, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

    # objects =  pattern_objects.findall(cleantext);
    
    # print objects;
	
    time_snapshot_list = [];
    frequency_snapshot_list = [];
    snapshot_list = [];
    excitation_list = [];
    probe_list = [];
    sphere_list = [];
    block_list = [];
    cylinder_list = [];
    rotation_list = [];

    xmesh = [];
    ymesh = [];
    zmesh = [];
    flag = Flag();
    boundaries = Boundaries();
    box = Box();

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
        
        # print 'type = ',type;
        # print 'data = ',data;

        #################################################################
        # # code to store the data in a cell array of strings and numbers
        # dataV = [];
        
        # # split data by lines
        # lines = strread(data,'%s','delimiter','\r');

        # cellFlag = 0;
        # for L in range(len(lines)):
            # if ~len(lines{L}): #if line is empty
                # continue;

            # # Convert string to number
            # dd = str2num(lines{L});

            # if cellFlag:
                # if len(dd):  # dd is num
                    # dataV{len(dataV)+1} = dd; # store number
                # else:           # dd is not num
                    # dataV{len(dataV)+1} = lines{L}; # store string
            # else:
                # if len(dd):  # dd is num
                    # dataV = [dataV,dd]; # store number
                # else:           # dd is not num
                    # # Convert numeric array to cell array
                    # dataV = num2cell(dataV);
                    # cellFlag = 1;
                    # dataV{len(dataV)+1} = lines{L}; #store string
        #################################################################

        entry = Entry();
        entry.type = type;
        entry.data = data;
        entries.append(entry);

        # if entry.type in ['FREQUENCY_SNAPSHOT','SNAPSHOT']:
            # snapshot = Snapshot()
            # snapshot.read_entry(entry);
            # snapshot_list.append(snapshot);
        if entry.type == 'FREQUENCY_SNAPSHOT':
            # print 'FREQUENCY_SNAPSHOT';
            frequency_snapshot = Frequency_snapshot();
            frequency_snapshot.read_entry(entry);
            frequency_snapshot_list.append(frequency_snapshot);
            snapshot_list.append(frequency_snapshot);
        elif entry.type == 'SNAPSHOT':
            # print 'SNAPSHOT';
            time_snapshot = Time_snapshot();
            time_snapshot.read_entry(entry);
            time_snapshot_list.append(time_snapshot);
            snapshot_list.append(time_snapshot);
            # else:
                # print('Sense, it makes none.'); sys.exit(-1);
        elif entry.type == 'EXCITATION':
            # print 'EXCITATION';
            current_excitation = Excitation();
            current_excitation.read_entry(entry);
            excitation_list.append(current_excitation);
        elif entry.type == 'XMESH':
            # print 'XMESH';
            xmesh = entry.data;
            xmesh_read = True;
        elif entry.type == 'YMESH':
            # print 'YMESH';
            ymesh = entry.data;
        elif entry.type == 'ZMESH':
            # print 'ZMESH';
            zmesh = entry.data;
        elif entry.type == 'FLAG':
            # print 'FLAG';
            flag.read_entry(entry);
        elif entry.type == 'BOUNDARY':
            # print 'BOUNDARY';
            boundaries.read_entry(entry);
        elif entry.type == 'BOX':
            box.read_entry(entry);
            box_read = True;
        elif entry.type == 'PROBE':
            probe = Probe();
            probe.read_entry(entry);
            probe_list.append(probe);
        elif entry.type == 'SPHERE':
            sphere = Sphere();
            sphere.read_entry(entry);
            sphere_list.append(sphere);
        elif entry.type == 'BLOCK':
            block = Block();
            block.read_entry(entry);
            block_list.append(block);
        elif entry.type == 'CYLINDER':
            cylinder = Cylinder();
            cylinder.read_entry(entry);
            cylinder_list.append(cylinder);
        elif entry.type == 'ROTATION':
            rotation = Rotation();
            rotation.read_entry(entry);
            rotation_list.append(rotation);
        else:
            print 'Unknown type: ', entry.type;

    structured_entries.snapshot_list += snapshot_list;
    structured_entries.time_snapshot_list += time_snapshot_list;
    structured_entries.frequency_snapshot_list += frequency_snapshot_list;
    structured_entries.excitation_list += excitation_list;
    structured_entries.xmesh = xmesh;
    structured_entries.ymesh = ymesh;
    structured_entries.zmesh = zmesh;
    structured_entries.flag = flag;
    structured_entries.boundaries = boundaries;
    structured_entries.box = box;
    structured_entries.probe_list += probe_list;
    structured_entries.sphere_list += sphere_list;
    structured_entries.block_list += block_list;
    structured_entries.cylinder_list += cylinder_list;
    structured_entries.rotation_list += rotation_list;
    
    return [ xmesh_read, box_read ];

def getname(filename, default_extension):
    
    extension = getExtension(filename);
    if extension == 'geo' or extension == 'inp':
        return filename;
    else:
        return filename + '.' + default_extension;
    
def read_inputs(filename,structured_entries):

    box_read = False;
    xmesh_read = False;
    
    f = open(filename, 'r');
    for line in f:
        # print filename;
        subfile = os.path.join(os.path.dirname(filename),line.strip());
        # print subfile;
        # print os.path.dirname(filename);
        if (not xmesh_read):
            subfile = getname(subfile,'inp');
        else:
            subfile = getname(subfile,'geo');
        [ xmesh_read, box_read ] = read_input_file(subfile, structured_entries);
    f.close();
    if (not xmesh_read):
        print 'WARNING: mesh not found';
    if (not box_read):
        print 'WARNING: box not found';
    
def getExtension(filename):
    return filename.split(".")[-1];
    
def readBristolFDTD(filename):

    structured_entries = Structured_entries();
    
    # should read .in (=>.inp+.geo), .geo or .inp
    extension = getExtension(filename);
    if extension == 'in':
        print '.in file detected';
        read_inputs(filename,structured_entries);
    elif extension == 'inp':
        print '.inp file detected';
        read_input_file(filename, structured_entries);
    elif extension == 'geo':
        print '.geo file detected';
        read_input_file(filename, structured_entries);
    elif extension == 'prn':
        print '.prn file detected: Not supported yet';
    else:
        print 'Unknown file format:', extension;
    
    print '================';
    print structured_entries;
    print '================';
    # a= Excitation();
    # b= Excitation();
    # c = [a,b]
    # r='';
    # for t in c:
        # r+= t.__str__();
    # print r;
    # print '================';
    
    # extList = ["swf", "html", "exe"]
    # filename = "python.exe"
    # splitFilename = 
    # if filename.split(".")[-1] == '.in'in extList: return True
    # else: return False

    # in_file = file(filename, "r");
    # line = in_file.readline();

    # Nobjects = int(line)
    # #print "Nobjects = ", Nobjects
    # object_names = []
    # for i in range(0, Nobjects):
        # line = in_file.readline()
        # object_names.append(line.strip())

    # in_file.close()
    
print '----->Importing bristol FDTD geometry...';

# readBristolFDTD('rotated_cylinder.in');
# getname('tettte.in','.in');
readBristolFDTD('rotated_cylinder.in');
# readBristolFDTD('H:\\DATA\\rotated_cylinder\\rotated_cylinder.in');
# readBristolFDTD('H:\\DATA\\rotated_cylinder\\rotated_cylinder.inp');
# readBristolFDTD('H:\\DATA\\rotated_cylinder\\rotated_cylinder.geo');

# TestObjects();

print '...done';
