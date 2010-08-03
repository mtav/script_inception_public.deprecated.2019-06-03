function [ entries, structured_entries ] = GEO_INP_reader(filename)

% ask for input file if not given
if exist('filename','var')==0
    disp('filename not given');
    [file,path] = uigetfile({'*.geo *.inp'},'Select a GEO or INP file');
    filename=[path,file];
end

% read the whole file as one string
fulltext = fileread(filename);

% remove comments
pattern_stripcomments = '\*\*.*$';
cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');

% extract blocks
pattern_blocks = '^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}';
[tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_blocks, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

entries={};
% process blocks
for i=1:length(names_blocks)

    type = names_blocks(:,i).type;
    data = names_blocks(:,i).data;
%     disp(['===>type=',type]);

    dataV=[];
    % remove empty lines
    lines = strread(data,'%s','delimiter','\r');
    cellFlag=0;
    for L=1:length(lines)
        if ~length(lines{L})
            continue;
        end

        dd=str2num(lines{L});
        
        if cellFlag
            if length(dd)  %% dd is num
                dataV{length(dataV)+1}=dd;
            else           %% dd is not num
                dataV{length(dataV)+1}=lines{L};
            end
        else
           if length(dd)  %% dd is num
                dataV=[dataV,dd];
            else           %% dd is not num
                cellFlag=1;
                dataV=num2cell(dataV);
                dataV{length(dataV)+1}=lines{L};
            end
        end
    end
    entry.type=type;
    entry.data=dataV';
    entries{length(entries)+1}=entry;
	
	all_snapshots = struct('hoop', {}, 'target', {})
	time_snapshots = struct('hoop', {}, 'target', {})
	frequency_snapshots = struct('hoop', {}, 'target', {})
	
	entry.type
	entry.data(1)
	switch upper(entry.type)
		case {'FREQUENCY_SNAPSHOT','SNAPSHOT'}
			disp('Adding snapshot...');
			if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
			
			elseif strcmpi(entry.type,'SNAPSHOT')
			
			else
				error('Sense, it makes none.');
			end
		otherwise
			disp('Unknown type.');
	end
	
end %end of loop through blocks

structured_entries.all_snapshots = all_snapshots;
structured_entries.time_snapshots = time_snapshots;
structured_entries.frequency_snapshots = frequency_snapshots;

	idx = 1;
	snapshot.first = entry.data(idx);idx = idx+1;
	snapshot.repetition = entry.data(idx); idx = idx+1;
	snapshot.plane = entry.data(idx); idx = idx+1;
	snapshot.P1(1) = entry.data(idx); idx = idx+1;
	snapshot.P1(2) = entry.data(idx); idx = idx+1;
	snapshot.P1(3) = entry.data(idx); idx = idx+1;
	snapshot.P2(1) = entry.data(idx); idx = idx+1;
	snapshot.P2(2) = entry.data(idx); idx = idx+1;
	snapshot.P2(3) = entry.data(idx); idx = idx+1;
	snapshot.E(1) = entry.data(idx); idx = idx+1;
	snapshot.E(2) = entry.data(idx); idx = idx+1;
	snapshot.E(3) = entry.data(idx); idx = idx+1;
	snapshot.H(1) = entry.data(idx); idx = idx+1;
	snapshot.H(2) = entry.data(idx); idx = idx+1;
	snapshot.H(3) = entry.data(idx); idx = idx+1;
	snapshot.J(1) = entry.data(idx); idx = idx+1;
	snapshot.J(2) = entry.data(idx); idx = idx+1;
	snapshot.J(3) = entry.data(idx); idx = idx+1;
	snapshot.power = entry.data(idx); idx = idx+1;

	idx = 1;
	snapshot.first = entry.data(idx); idx = idx+1;
	snapshot.repetition = entry.data(idx); idx = idx+1;
	snapshot.interpolate = entry.data(idx); idx = idx+1;
	snapshot.real_dft = entry.data(idx); idx = idx+1;
	snapshot.mod_only = entry.data(idx); idx = idx+1;
	snapshot.mod_all = entry.data(idx); idx = idx+1;
	snapshot.plane = entry.data(idx); idx = idx+1;
	snapshot.P1(1) = entry.data(idx); idx = idx+1;
	snapshot.P1(2) = entry.data(idx); idx = idx+1;
	snapshot.P1(3) = entry.data(idx); idx = idx+1;
	snapshot.P2(1) = entry.data(idx); idx = idx+1;
	snapshot.P2(2) = entry.data(idx); idx = idx+1;
	snapshot.P2(3) = entry.data(idx); idx = idx+1;
	snapshot.frequency = entry.data(idx); idx = idx+1;
	snapshot.starting_sample = entry.data(idx); idx = idx+1;
	snapshot.E(1) = entry.data(idx); idx = idx+1;
	snapshot.E(2) = entry.data(idx); idx = idx+1;
	snapshot.E(3) = entry.data(idx); idx = idx+1;
	snapshot.H(1) = entry.data(idx); idx = idx+1;
	snapshot.H(2) = entry.data(idx); idx = idx+1;
	snapshot.H(3) = entry.data(idx); idx = idx+1;
	snapshot.J(1) = entry.data(idx); idx = idx+1;
	snapshot.J(2) = entry.data(idx); idx = idx+1;
	snapshot.J(3) = entry.data(idx); idx = idx+1;
