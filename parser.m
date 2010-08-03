function parser(filename)

	% ask for input file if not given
	if exist('filename','var')==0
		disp('filename not given');
		filename = uigetfile({'*.txt'},'Select a file');
	end
	
	% read the whole file as one string
	fulltext = fileread(filename);
	
	% remove comments
	pattern_stripcomments = '\*\*.*$';
	cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');
	
	% extract blocks
	pattern_blocks = '^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}';
	[tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_blocks, 'tokens', 'match', 'names', 'lineanchors', 'warnings');
	
	% process blocks
	for i=1:length(names_blocks)
		
		type = names_blocks(:,i).type;
		data = names_blocks(:,i).data;
		disp(['===>type=',type]);
		
		% remove empty lines
		lines = strread(data,'%s','delimiter',['\r']);
		for L=1:length(lines)
			if length(lines{L}) ~= 0
				disp(lines{L});
			end
		end
	end
	
end
