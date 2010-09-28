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

def read_input_file(filename):
    print 'Processing ', filename;
    box_read=False;
    xmesh_read=False;
    
    # open file
    input = open(filename);
    # read the whole file as one string
    fulltext = input.read();

    print fulltext;

    # remove comments
    pattern_stripcomments = re.compile("\*\*.*\n")
    cleantext = pattern_stripcomments.sub("\n", fulltext);

    print cleantext;
    
    # close file
    input.close();

	# # extract blocks
	# pattern_blocks = '^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}';
	# [tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_blocks, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

	# time_snapshots=struct('first',{},'repetition',{},'plane',{},'P1',{},'P2',{},'E',{},'H',{},'J',{},'power',{});
	# frequency_snapshots=struct('first',{},'repetition',{},'interpolate',{},'real_dft',{},'mod_only',{},'mod_all',{},'plane',{},'P1',{},'P2',{},'frequency',{},'starting_sample',{},'E',{},'H',{},'J',{});
	# all_snapshots=struct('first',{},'repetition',{},'interpolate',{},'real_dft',{},'mod_only',{},'mod_all',{},'plane',{},'P1',{},'P2',{},'frequency',{},'starting_sample',{},'E',{},'H',{},'J',{},'power',{});
	# excitations=struct('current_source',{},'P1',{},'P2',{},'E',{},'H',{},'type',{},'time_constant',{},'amplitude',{},'time_offset',{},'frequency',{},'param1',{},'param2',{},'param3',{},'param4',{});
	# boundaries=struct('type',{},'p',{});
	
	# xmesh = [];
	# ymesh = [];
	# zmesh = [];
    # flag=[];
    # boundaries=[];

	# entries={};
	# # process blocks
	# for i=1:length(names_blocks)

		# type = names_blocks(:,i).type;
		# data = names_blocks(:,i).data;
		# # disp(['===>type=',type]);

		# dataV=[];
		# # remove empty lines
		# lines = strread(data,'%s','delimiter','\r');
		# cellFlag=0;
		# for L=1:length(lines)
			# if ~length(lines{L})
				# continue;
			# end

			# dd=str2num(lines{L});

			# if cellFlag
				# if length(dd)  %% dd is num
					# dataV{length(dataV)+1}=dd;
				# else           %% dd is not num
					# dataV{length(dataV)+1}=lines{L};
				# end
			# else
			   # if length(dd)  %% dd is num
					# dataV=[dataV,dd];
				# else           %% dd is not num
					# cellFlag=1;
					# dataV=num2cell(dataV);
					# dataV{length(dataV)+1}=lines{L};
				# end
			# end
		# end % end of loop through lines

		# entry.type=type;
		# entry.data=dataV';
		# entries{length(entries)+1}=entry;

		# switch upper(entry.type)
			# case {'FREQUENCY_SNAPSHOT','SNAPSHOT'}
				# snapshot = add_snapshot(entry);
				# all_snapshots = [ all_snapshots snapshot ];
				# if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
					# snapshot = add_frequency_snapshot(entry);
					# frequency_snapshots = [ frequency_snapshots snapshot ];
				# elseif strcmpi(entry.type,'SNAPSHOT')
					# snapshot = add_time_snapshot(entry);
					# time_snapshots = [ time_snapshots snapshot ];                    
				# else
					# error('Sense, it makes none.');
				# end
			# case {'EXCITATION'}
				# current_excitation = add_excitation(entry);
				# excitations = [ excitations current_excitation ];
			# case {'XMESH'}
				# xmesh = entry.data;
			# case {'YMESH'}
				# ymesh = entry.data;
			# case {'ZMESH'}
				# zmesh = entry.data;
            # case {'FLAG'}
				# flag = add_flag(entry);
            # case {'BOUNDARY'}
                # boundaries = add_boundary(entry);
			# otherwise
				# % disp('Unknown type.');
		# end # end of switch

	# end #end of loop through blocks

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
