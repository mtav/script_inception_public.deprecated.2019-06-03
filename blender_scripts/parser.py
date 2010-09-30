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

def read_input_file(filename):
    print 'Processing ', filename;
    box_read=False;
    xmesh_read=False;
    
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
	
    time_snapshots = Time_snapshots();
    frequency_snapshots = Frequency_snapshots();
    all_snapshots = All_snapshots();
    excitations = Excitations();
    boundaries = Boundaries();

    xmesh = [];
    ymesh = [];
    zmesh = [];
    flag=[];
    boundaries=[];

    entries={};
	# process blocks
    for i in range(len(blocks)):
        type = blocks[i]['type'];
        data = blocks[i]['data'];
        data = re.split('\s+',data);
        data = filter(None, data);
        
        print 'type=',type;
        print 'data=',data;
        
        dataV=[];
        # remove empty lines
        lines = strread(data,'%s','delimiter','\r');
        cellFlag=0;
        for L=1:length(lines)
            if ~length(lines{L})
                continue;

            dd=str2num(lines{L});

            if cellFlag:
                if length(dd)  # dd is num
                    dataV{length(dataV)+1}=dd;
                else           # dd is not num
                    dataV{length(dataV)+1}=lines{L};
                end
            else:
               if length(dd):  # dd is num
                    dataV=[dataV,dd];
                else:           # dd is not num
                    cellFlag=1;
                    dataV=num2cell(dataV);
                    dataV{length(dataV)+1}=lines{L};

        entry.type=type;
        entry.data=dataV';
        entries{length(entries)+1}=entry;

        switch upper(entry.type)
            case {'FREQUENCY_SNAPSHOT','SNAPSHOT'}
                snapshot = add_snapshot(entry);
                all_snapshots = [ all_snapshots snapshot ];
                if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
                    snapshot = add_frequency_snapshot(entry);
                    frequency_snapshots = [ frequency_snapshots snapshot ];
                elseif strcmpi(entry.type,'SNAPSHOT')
                    snapshot = add_time_snapshot(entry);
                    time_snapshots = [ time_snapshots snapshot ];                    
                else
                    print('Sense, it makes none.'); exit(-1);
                end
            case {'EXCITATION'}
                current_excitation = add_excitation(entry);
                excitations = [ excitations current_excitation ];
            case {'XMESH'}
                xmesh = entry.data;
            case {'YMESH'}
                ymesh = entry.data;
            case {'ZMESH'}
                zmesh = entry.data;
            case {'FLAG'}
                flag = add_flag(entry);
            case {'BOUNDARY'}
                boundaries = add_boundary(entry);
            otherwise
                print('Unknown type.');

	# structured_entries.all_snapshots = all_snapshots;
	# structured_entries.time_snapshots = time_snapshots;
	# structured_entries.frequency_snapshots = frequency_snapshots;
	# structured_entries.excitations = excitations;
	# structured_entries.xmesh = xmesh;
	# structured_entries.ymesh = ymesh;
	# structured_entries.zmesh = zmesh;
    # structured_entries.flag=flag;
    # structured_entries.boundaries=boundaries;
    
    return [ xmesh_read, box_read ];

def getname(filename, default_extension):
    
    extension = getExtension(filename);
    if extension == 'geo' or extension == 'inp':
        return filename;
    else:
        return filename + '.' + default_extension;
    
def read_inputs(filename):

    box_read=False;
    xmesh_read=False;
    
    f=open(filename, 'r');
    for line in f:
        print filename;
        subfile = os.path.join(os.path.dirname(filename),line.strip());
        print subfile;
        print os.path.dirname(filename);
        if (not xmesh_read):
            subfile = getname(subfile,'inp');
        else:
            subfile = getname(subfile,'geo');
        [ xmesh_read, box_read ] = read_input_file(subfile);
    f.close();
    if (not xmesh_read):
        print 'WARNING: mesh not found';
    if (not box_read):
        print 'WARNING: box not found';
    
def getExtension(filename):
    return filename.split(".")[-1];
    
def readBristolFDTD(filename):
    # should read .in (=>.inp+.geo), .geo or .inp
    extension = getExtension(filename);
    if extension == 'in':
        print '.in file detected';
        read_inputs(filename);
    elif extension == 'inp':
        print '.inp file detected';
        read_input_file(filename);
    elif extension == 'geo':
        print '.geo file detected';
        read_input_file(filename);
    elif extension == 'prn':
        print '.prn file detected: Not supported yet';
    else:
        print 'Unknown file format:', extension;
    
    # extList = ["swf", "html", "exe"]
    # filename = "python.exe"
    # splitFilename = 
    # if filename.split(".")[-1] == '.in'in extList: return True
    # else: return False

    # in_file = file(filename, "r");
    # line = in_file.readline();

    # Nobjects = int(line)
    # #print "Nobjects=", Nobjects
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
