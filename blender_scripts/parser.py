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

class Time_snapshots:
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

class Frequency_snapshots:
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

class All_snapshots:
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

class Excitations:
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

class Boundaries:
    def __init__(self):
        self.type = 0;
        self.p = 0;

class Flag:
    def __init__(self):
        self.iMethod = 0;
        self.propCons = 0;
        self.flagOne = 0;
        self.flagTwo = 0;
        self.numSteps = 0;
        self.stabFactor = 0;
        self.id = 0;
    def entry_to_flag(self, entry):
        self.iMethod = entry.data[0];
        self.propCons = entry.data[1];
        self.flagOne = entry.data[2];
        self.flagTwo = entry.data[3];
        self.numSteps = entry.data[4];
        self.stabFactor = entry.data[5];
        self.id = entry.data[6];
        
class Structured_entries:
    def __init__(self):
        self.all_snapshots = [];
        self.time_snapshots = [];
        self.frequency_snapshots = [];
        self.excitations = [];
        self.xmesh = [];
        self.ymesh = [];
        self.zmesh = [];
        self.flag = Flag();
        self.boundaries = [];
        self.box = [];

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def add_flag(entry):
    # flag.iMethod = entry.data{1};
    # flag.propCons = entry.data{2};
    # flag.flagOne = entry.data{3};
    # flag.flagTwo = entry.data{4};
    # flag.numSteps = entry.data{5};
    # flag.stabFactor = entry.data{6};
    # flag.id = entry.data{7};
    return(0);

def add_boundary(entry):
	# M = reshape(entry.data,4,length(entry.data)/4)';
	# for i in range(6):
		# boundaries[i].type = M(i,1);
		# boundaries[i].p = M(i,2:4);
    return(0);

def add_frequency_snapshot(entry):
	# idx = 1;
	# snapshot.first = entry.data(idx); idx = idx+1;
	# snapshot.repetition = entry.data(idx); idx = idx+1;
	# snapshot.interpolate = entry.data(idx); idx = idx+1;
	# snapshot.real_dft = entry.data(idx); idx = idx+1;
	# snapshot.mod_only = entry.data(idx); idx = idx+1;
	# snapshot.mod_all = entry.data(idx); idx = idx+1;
	# snapshot.plane = entry.data(idx); idx = idx+1;
	# snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.frequency = entry.data(idx); idx = idx+1;
	# snapshot.starting_sample = entry.data(idx); idx = idx+1;
	# snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
    return(0);

def add_time_snapshot(entry):
	# idx = 1;
	# snapshot.first = entry.data(idx); idx = idx+1;
	# snapshot.repetition = entry.data(idx); idx = idx+1;
	# snapshot.plane = entry.data(idx); idx = idx+1;
	# snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# snapshot.power = entry.data(idx); idx = idx+1;
    return(0);

def add_snapshot(entry):
	# if entry.type == 'FREQUENCY_SNAPSHOT':
		# idx = 1;
		# snapshot.first = entry.data(idx); idx = idx+1;
		# snapshot.repetition = entry.data(idx); idx = idx+1;
		# snapshot.interpolate = entry.data(idx); idx = idx+1;
		# snapshot.real_dft = entry.data(idx); idx = idx+1;
		# snapshot.mod_only = entry.data(idx); idx = idx+1;
		# snapshot.mod_all = entry.data(idx); idx = idx+1;
		# snapshot.plane = entry.data(idx); idx = idx+1;
		# snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.frequency = entry.data(idx); idx = idx+1;
		# snapshot.starting_sample = entry.data(idx); idx = idx+1;
		# snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.power = -1;
	# elif entry.type == 'SNAPSHOT':
		# idx = 1;
		# snapshot.first = entry.data(idx); idx = idx+1;
		# snapshot.repetition = entry.data(idx); idx = idx+1;
		# snapshot.interpolate = -1;
		# snapshot.real_dft = -1;
		# snapshot.mod_only = -1;
		# snapshot.mod_all = -1;
		# snapshot.plane = entry.data(idx); idx = idx+1;
		# snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.frequency = -1;
		# snapshot.starting_sample = -1;
		# snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		# snapshot.power = entry.data(idx); idx = idx+1;
	# else:
		# error('Sense, it makes none.');
    return(0);

def add_excitation(entry):
	# idx = 1;
	# current_excitation.current_source = entry.data(idx); idx = idx+1;
	# current_excitation.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# current_excitation.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# current_excitation.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# current_excitation.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	# current_excitation.type = entry.data(idx); idx = idx+1;
	# current_excitation.time_constant = entry.data(idx); idx = idx+1;
	# current_excitation.amplitude = entry.data(idx); idx = idx+1;
	# current_excitation.time_offset = entry.data(idx); idx = idx+1;
	# current_excitation.frequency = entry.data(idx); idx = idx+1;
	# current_excitation.param1 = entry.data(idx); idx = idx+1;
	# current_excitation.param2 = entry.data(idx); idx = idx+1;
	# current_excitation.param3 = entry.data(idx); idx = idx+1;
	# current_excitation.param4 = entry.data(idx); idx = idx+1;
    return(0);
        
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
	
    time_snapshots = [];
    frequency_snapshots = [];
    all_snapshots = [];
    excitations = [];
    boundaries = [];

    xmesh = [];
    ymesh = [];
    zmesh = [];
    flag = [];
    boundaries = [];

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
            snapshot = add_snapshot(entry);
            all_snapshots.append(snapshot);
            if entry.type == 'FREQUENCY_SNAPSHOT':
                print 'FREQUENCY_SNAPSHOT';
                snapshot = add_frequency_snapshot(entry);
                frequency_snapshots.append(snapshot);
            elif entry.type == 'SNAPSHOT':
                print 'SNAPSHOT';
                snapshot = add_time_snapshot(entry);
                time_snapshots.append(snapshot);                    
            else:
                print('Sense, it makes none.'); sys.exit(-1);
        elif entry.type == 'EXCITATION':
            print 'EXCITATION';
            current_excitation = add_excitation(entry);
            excitations.append(current_excitation);
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
            flag = add_flag(entry);
        elif entry.type == 'BOUNDARY':
            print 'BOUNDARY';
            boundaries = add_boundary(entry);
        elif entry.type == 'BOX':
            box = entry.data;
            box_read = True;
        else:
            print('Unknown type.');

    structured_entries.all_snapshots.append(all_snapshots);
    structured_entries.time_snapshots.append(time_snapshots);
    structured_entries.frequency_snapshots.append(frequency_snapshots);
    structured_entries.excitations.append(excitations);
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
    
    structured_entries.print();
    
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
