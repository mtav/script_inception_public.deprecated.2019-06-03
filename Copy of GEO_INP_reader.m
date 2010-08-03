function data = GEO_INP_reader(filename)
	% regexp fun! :D
	if exist('filename','var')==0
		disp('filename not given');
		filename = uigetfile({'*.geo';'*.inp'},'Select a GEO or INP file');
	end
	
	fulltext = fileread(filename);
	
	% example pattern from python:
	% "segment \d+(\n.*?)+?segment end"

	% pattern_1 = fileread('GEO_INP_reader.pattern');
	
	pattern_stripcomments = '\*\*.*$';
	cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');

	% match_stripcomments{:}
	% fulltext
	% cleantext
	
	% return
	
	pattern_cleantext = '^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}';
	[tokens_cleantext match_cleantext names_cleantext] =  regexp(cleantext, pattern_cleantext, 'tokens', 'match', 'names', 'lineanchors', 'warnings');
	% tokens_cleantext{:}
	% match_cleantext{:}
	% length(match_cleantext)
	% names_cleantext(:,1)
	% names_cleantext(1,:).type
	
	% return
		
	for i=1:length(names_cleantext)
	% for i=1:1
		
		type = names_cleantext(:,i).type;
		data = names_cleantext(:,i).data;
		disp(['===>type=',type]);
		% disp(['data=',data]);
		% pat2 = regexptranslate('escape', data)
		% return

		% pattern_data = '\w+\n';
		% [tokens_data match_data names_data] =  regexp(data, pattern_data, 'tokens', 'match', 'names', 'dotexceptnewline', 'lineanchors', 'warnings')
		% tokens_data{:}
		% match_data{:}
		% data.class
		% idxstrfind(str,char(10))
		% regexp(data,char(10),'split','dotexceptnewline');
		lines = strread(data,'%s','delimiter',['\r']);
		% lines
		
		for L=1:length(lines)
			if length(lines{L}) ~= 0
				disp(lines{L});
			end
		end
	end
	
end
