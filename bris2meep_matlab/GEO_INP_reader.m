function [ entries, structured_entries ] = GEO_INP_reader(filename)
    % function [ entries, structured_entries ] = GEO_INP_reader(filename)
    % creates entries + structured_entries from filename

	% ask for input file if not given
	if exist('filename','var') == 0
		disp('filename not given');
		[file,path] = uigetfile({'*.geo *.inp'},'Select a GEO or INP file');
		filename = [path,file];
	end

	% read the whole file as one string
	fulltext = fileread(filename);

	% remove comments
	pattern_stripcomments = '\*\*.*$';
	cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');

	% extract blocks
	pattern_blocks = '^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}';
	[tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_blocks, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

	time_snapshots = struct('first',{},'repetition',{},'plane',{},'P1',{},'P2',{},'E',{},'H',{},'J',{},'power',{});
	frequency_snapshots = struct('first',{},'repetition',{},'interpolate',{},'real_dft',{},'mod_only',{},'mod_all',{},'plane',{},'P1',{},'P2',{},'frequency',{},'starting_sample',{},'E',{},'H',{},'J',{});
	all_snapshots = struct('first',{},'repetition',{},'interpolate',{},'real_dft',{},'mod_only',{},'mod_all',{},'plane',{},'P1',{},'P2',{},'frequency',{},'starting_sample',{},'E',{},'H',{},'J',{},'power',{});
	excitations = struct('current_source',{},'P1',{},'P2',{},'E',{},'H',{},'type',{},'time_constant',{},'amplitude',{},'time_offset',{},'frequency',{},'param1',{},'param2',{},'param3',{},'param4',{});
	boundaries = struct('type',{},'p',{});
	
	xmesh = [];
	ymesh = [];
	zmesh = [];
    flag = [];
    boundaries = [];

	entries = {};
	% process blocks
	for i = 1:length(names_blocks)

		type = names_blocks(:,i).type;
		data = names_blocks(:,i).data;
		% disp(['===>type = ',type]);

		dataV = [];
		% remove empty lines
		lines = strread(data,'%s','delimiter','\r');
		cellFlag = 0;
		for L = 1:length(lines)
			if ~length(lines{L})
				continue;
			end

			dd = str2num(lines{L});

			if cellFlag
				if length(dd)  %% dd is num
					dataV{length(dataV)+1} = dd;
				else           %% dd is not num
					dataV{length(dataV)+1} = lines{L};
				end
			else
			   if length(dd)  %% dd is num
					dataV = [dataV,dd];
				else           %% dd is not num
					cellFlag = 1;
					dataV = num2cell(dataV);
					dataV{length(dataV)+1} = lines{L};
				end
			end
		end % end of loop through lines

		entry.type = type;
		entry.data = dataV';
		entries{length(entries)+1} = entry;

		% entry.type
		% entry.data(1)
		switch upper(entry.type)
			case {'FREQUENCY_SNAPSHOT','SNAPSHOT'}
				% disp('Adding snapshot...');
				snapshot = add_snapshot(entry);
				all_snapshots = [ all_snapshots snapshot ];
				if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
					snapshot = add_frequency_snapshot(entry);
					frequency_snapshots = [ frequency_snapshots snapshot ];
				elseif strcmpi(entry.type,'SNAPSHOT')
					snapshot = add_time_snapshot(entry);
					time_snapshots = [ time_snapshots snapshot ];                    
				else
					error('Sense, it makes none.');
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
				% disp('Unknown type.');
		end % end of switch

	end %end of loop through blocks

	structured_entries.all_snapshots = all_snapshots;
	structured_entries.time_snapshots = time_snapshots;
	structured_entries.frequency_snapshots = frequency_snapshots;
	structured_entries.excitations = excitations;
	structured_entries.xmesh = xmesh;
	structured_entries.ymesh = ymesh;
	structured_entries.zmesh = zmesh;
    structured_entries.flag = flag;
    structured_entries.boundaries = boundaries;
    structured_entries.box = box;

end % end of function

function flag = add_flag(entry)
    flag.iMethod = entry.data{1};
    flag.propCons = entry.data{2};
    flag.flagOne = entry.data{3};
    flag.flagTwo = entry.data{4};
    flag.numSteps = entry.data{5};
    flag.stabFactor = entry.data{6};
    flag.id = entry.data{7};
end

function boundaries = add_boundary(entry)
	M = reshape(entry.data,4,length(entry.data)/4)';
	for i = 1:6
		boundaries(i).type = M(i,1);
		boundaries(i).p = M(i,2:4);
	end
end

function snapshot = add_frequency_snapshot(entry)
	idx = 1;
	snapshot.first = entry.data(idx); idx = idx+1;
	snapshot.repetition = entry.data(idx); idx = idx+1;
	snapshot.interpolate = entry.data(idx); idx = idx+1;
	snapshot.real_dft = entry.data(idx); idx = idx+1;
	snapshot.mod_only = entry.data(idx); idx = idx+1;
	snapshot.mod_all = entry.data(idx); idx = idx+1;
	snapshot.plane = entry.data(idx); idx = idx+1;
	snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.frequency = entry.data(idx); idx = idx+1;
	snapshot.starting_sample = entry.data(idx); idx = idx+1;
	snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
end

function snapshot = add_time_snapshot(entry)
	idx = 1;
	snapshot.first = entry.data(idx); idx = idx+1;
	snapshot.repetition = entry.data(idx); idx = idx+1;
	snapshot.plane = entry.data(idx); idx = idx+1;
	snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	snapshot.power = entry.data(idx); idx = idx+1;
end

function snapshot = add_snapshot(entry)
	if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
		idx = 1;
		snapshot.first = entry.data(idx); idx = idx+1;
		snapshot.repetition = entry.data(idx); idx = idx+1;
		snapshot.interpolate = entry.data(idx); idx = idx+1;
		snapshot.real_dft = entry.data(idx); idx = idx+1;
		snapshot.mod_only = entry.data(idx); idx = idx+1;
		snapshot.mod_all = entry.data(idx); idx = idx+1;
		snapshot.plane = entry.data(idx); idx = idx+1;
		snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.frequency = entry.data(idx); idx = idx+1;
		snapshot.starting_sample = entry.data(idx); idx = idx+1;
		snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.power = -1;
	elseif strcmpi(entry.type,'SNAPSHOT')
		idx = 1;
		snapshot.first = entry.data(idx); idx = idx+1;
		snapshot.repetition = entry.data(idx); idx = idx+1;
		snapshot.interpolate = -1;
		snapshot.real_dft = -1;
		snapshot.mod_only = -1;
		snapshot.mod_all = -1;
		snapshot.plane = entry.data(idx); idx = idx+1;
		snapshot.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.frequency = -1;
		snapshot.starting_sample = -1;
		snapshot.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.J = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
		snapshot.power = entry.data(idx); idx = idx+1;
	else
		error('Sense, it makes none.');
	end
end

function current_excitation = add_excitation(entry)
	idx = 1;
	current_excitation.current_source = entry.data(idx); idx = idx+1;
	current_excitation.P1 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	current_excitation.P2 = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	current_excitation.E = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	current_excitation.H = [entry.data(idx), entry.data(idx+1), entry.data(idx+2)]; idx = idx+3;
	current_excitation.type = entry.data(idx); idx = idx+1;
	current_excitation.time_constant = entry.data(idx); idx = idx+1;
	current_excitation.amplitude = entry.data(idx); idx = idx+1;
	current_excitation.time_offset = entry.data(idx); idx = idx+1;
	current_excitation.frequency = entry.data(idx); idx = idx+1;
	current_excitation.param1 = entry.data(idx); idx = idx+1;
	current_excitation.param2 = entry.data(idx); idx = idx+1;
	current_excitation.param3 = entry.data(idx); idx = idx+1;
	current_excitation.param4 = entry.data(idx); idx = idx+1;
end