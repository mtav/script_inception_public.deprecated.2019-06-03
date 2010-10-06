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
        self.first = entry.data[idx]; idx = idx+1;
        self.repetition = entry.data[idx]; idx = idx+1;
        self.plane = entry.data[idx]; idx = idx+1;
        self.P1 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.P2 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.E = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.H = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.J = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.power = entry.data[idx]; idx = idx+1;
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
        self.first = entry.data[idx]; idx = idx+1;
        self.repetition = entry.data[idx]; idx = idx+1;
        self.interpolate = entry.data[idx]; idx = idx+1;
        self.real_dft = entry.data[idx]; idx = idx+1;
        self.mod_only = entry.data[idx]; idx = idx+1;
        self.mod_all = entry.data[idx]; idx = idx+1;
        self.plane = entry.data[idx]; idx = idx+1;
        self.P1 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.P2 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.frequency = entry.data[idx]; idx = idx+1;
        self.starting_sample = entry.data[idx]; idx = idx+1;
        self.E = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.H = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.J = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        return(0);

class Snapshot:
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
        self.power = 0;
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
        'J = ' + str(self.J) + '\n' +\
        'power = ' + str(self.power);
        return ret;
    def read_entry(self,entry):
        if entry.type == 'FREQUENCY_SNAPSHOT':
            idx = 0;
            self.first = entry.data[idx]; idx = idx+1;
            self.repetition = entry.data[idx]; idx = idx+1;
            self.interpolate = entry.data[idx]; idx = idx+1;
            self.real_dft = entry.data[idx]; idx = idx+1;
            self.mod_only = entry.data[idx]; idx = idx+1;
            self.mod_all = entry.data[idx]; idx = idx+1;
            self.plane = entry.data[idx]; idx = idx+1;
            self.P1 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.P2 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.frequency = entry.data[idx]; idx = idx+1;
            self.starting_sample = entry.data[idx]; idx = idx+1;
            self.E = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.H = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.J = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.power = -1;
        elif entry.type == 'SNAPSHOT':
            idx = 0;
            self.first = entry.data[idx]; idx = idx+1;
            self.repetition = entry.data[idx]; idx = idx+1;
            self.interpolate = -1;
            self.real_dft = -1;
            self.mod_only = -1;
            self.mod_all = -1;
            self.plane = entry.data[idx]; idx = idx+1;
            self.P1 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.P2 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.frequency = -1;
            self.starting_sample = -1;
            self.E = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.H = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.J = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
            self.power = entry.data[idx]; idx = idx+1;
        else:
            print 'Sense, it makes none.'; sys.exit(-1);
        return(0);

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
        self.current_source = entry.data[idx]; idx = idx+1;
        self.P1 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.P2 = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.E = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.H = [entry.data[idx], entry.data[idx+1], entry.data[idx+2]]; idx = idx+3;
        self.type = entry.data[idx]; idx = idx+1;
        self.time_constant = entry.data[idx]; idx = idx+1;
        self.amplitude = entry.data[idx]; idx = idx+1;
        self.time_offset = entry.data[idx]; idx = idx+1;
        self.frequency = entry.data[idx]; idx = idx+1;
        self.param1 = entry.data[idx]; idx = idx+1;
        self.param2 = entry.data[idx]; idx = idx+1;
        self.param3 = entry.data[idx]; idx = idx+1;
        self.param4 = entry.data[idx]; idx = idx+1;
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
        print '===entry_to_boundary START==='
        print entry.type;
        print entry.data;
        for i in range(6):
            self.type[i] = entry.data[4*i];
            self.p[i] = entry.data[1+4*i:4+4*i];
        print self.type[i];
        print self.p[i];
        print '===entry_to_boundary END==='
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
        self.iMethod = entry.data[0];
        self.propCons = entry.data[1];
        self.flagOne = entry.data[2];
        self.flagTwo = entry.data[3];
        self.numSteps = entry.data[4];
        self.stabFactor = entry.data[5];
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
        self.lower = entry.data[0:3];
        self.upper = entry.data[3:6];
    
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

    print fulltext;

    # remove comments
    pattern_stripcomments = re.compile("\*\*.*\n")
    cleantext = pattern_stripcomments.sub("\n", fulltext);

    print cleantext;
    
	# extract blocks
    # pattern_blocks = re.compile("^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}");
    pattern_blocks = re.compile("(?P<type>\w+)\s*{(?P<data>[^{}]*)}",re.DOTALL)
    blocks = [m.groupdict() for m in pattern_blocks.finditer(cleantext)]

    # [tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_blocks, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

    # blocks =  pattern_blocks.findall(cleantext);
    
    print blocks;
	
    time_snapshot_list = [];
    frequency_snapshot_list = [];
    snapshot_list = [];
    excitation_list = [];

    xmesh = [];
    ymesh = [];
    zmesh = [];
    flag = Flag();
    boundaries = Boundaries();
    box = Box();

    entries = [];
	# process blocks
    for i in range(len(blocks)):
        type = blocks[i]['type'];
        data = blocks[i]['data'];
        
        # convert type to upper case and strip it
        type = type.upper().strip();
        # split data by spaces and new lines
        data = re.split('\s+',data);
        # remove empty lines from data
        data = filter(None, data);
        
        print 'type = ',type;
        print 'data = ',data;

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

        if entry.type in ['FREQUENCY_SNAPSHOT','SNAPSHOT']:
            snapshot = Snapshot()
            snapshot.read_entry(entry);
            snapshot_list.append(snapshot);
            if entry.type == 'FREQUENCY_SNAPSHOT':
                print 'FREQUENCY_SNAPSHOT';
                frequency_snapshot = Frequency_snapshot();
                frequency_snapshot.read_entry(entry);
                frequency_snapshot_list.append(frequency_snapshot);
            elif entry.type == 'SNAPSHOT':
                print 'SNAPSHOT';
                time_snapshot = Time_snapshot()
                time_snapshot.read_entry(entry);
                time_snapshot_list.append(time_snapshot);
            else:
                print('Sense, it makes none.'); sys.exit(-1);
        elif entry.type == 'EXCITATION':
            print 'EXCITATION';
            current_excitation = Excitation();
            current_excitation.read_entry(entry);
            excitation_list.append(current_excitation);
        elif entry.type == 'XMESH':
            print 'XMESH';
            xmesh = entry.data;
            xmesh_read = True;
        elif entry.type == 'YMESH':
            print 'YMESH';
            ymesh = entry.data;
        elif entry.type == 'ZMESH':
            print 'ZMESH';
            zmesh = entry.data;
        elif entry.type == 'FLAG':
            print 'FLAG';
            flag.read_entry(entry);
        elif entry.type == 'BOUNDARY':
            print 'BOUNDARY';
            boundaries.read_entry(entry);
        elif entry.type == 'BOX':
            box.read_entry(entry);
            box_read = True;
        else:
            print('Unknown type.');

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
        print filename;
        subfile = os.path.join(os.path.dirname(filename),line.strip());
        print subfile;
        print os.path.dirname(filename);
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
