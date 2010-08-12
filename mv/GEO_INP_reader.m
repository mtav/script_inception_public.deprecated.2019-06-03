function entries = GEO_INP_reader(filename)

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
end
