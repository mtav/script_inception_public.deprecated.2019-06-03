function [ entries ] = reader_draft(filename)
  entries = {};

  % read the whole file as one string
  fulltext = fileread(filename);

  % remove comments
  pattern_stripcomments = '\*\*(?!name=).*\n';
  %cleantext = pattern_stripcomments.sub("\n", fulltext);
  
  %pattern_stripcomments = '\*\*.*$';
  cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');

  % extract blocks
  pattern_blocks = '^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}';
  [tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_blocks, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

  pattern_objects = '(?P<Type>\w+)\s*(?P<nameblob>[^{}]+)?\{(?P<data>[^\{\}]*)\}'
  objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]
    
  % xmesh = [];
  % ymesh = [];
  % zmesh = [];
    % flag = [];
    % boundaries = [];

  % process blocks
  disp(['length(names_blocks) = ', num2str(length(names_blocks))]);
  for i = 1:length(names_blocks)

    type = names_blocks(:,i).type;
    data = names_blocks(:,i).data;
    % disp(['===>type = ',type]);

    dataV = [];
    % remove empty lines
    lines = strread(data,'%s','delimiter','\n');
    cellFlag = 0;
    for L = 1:length(lines)
      if ~length(lines{L})
        continue;
      end

      num_val = str2num(lines{L});
      %L
      %num_val
            
      str_val = strtrim(lines{L}); % trim string
      str_val = str_val(str_val ~= '"');% remove double quotes

      % TODO: Check if this can't be simplified, or if it's even necessary.
      if cellFlag
        if length(num_val)  %% num_val is num
          dataV{length(dataV)+1} = num_val;
        else           %% num_val is not num
          dataV{length(dataV)+1} = str_val;
        end
      else
         if length(num_val)  %% num_val is num
          dataV = [dataV,num_val];
        else           %% num_val is not num
          cellFlag = 1;
          dataV = num2cell(dataV);
          dataV{length(dataV)+1} = str_val;
        end
      end
    end % end of loop through lines

    entry.type = type;
    entry.data = dataV';
    entries{length(entries)+1} = entry;
end


      %# open file
      %input = open(filename)
      %# read the whole file as one string
      %fulltext = input.read()
      %# close file
      %input.close()
  
      %# print fulltext
  
      %# remove comments
      %# TODO: Add more generic system for functional comments (to add layer, scene and group for example)
      %pattern_stripcomments = re.compile("\*\*(?!name=).*\n")
      %cleantext = pattern_stripcomments.sub("\n", fulltext)
      %#print(cleantext)
  
      %# pattern_objects = re.compile("^(?<Type>\w+).*?\{(?<data>[^\{\}]*?)\}")
      %#pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<name>(?<=\*\*name=)[^{}]*)?{(?P<data>[^{}]*)}",re.DOTALL)
      %pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<nameblob>[^{}]+)?{(?P<data>[^{}]*)}",re.DOTALL)
      %objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]
    
      %entries = []
      %# process objects
      %for i in range(len(objects)):
          %Type = objects[i]['Type']
          %name = ''
          %if 'nameblob' in objects[i].keys():
            %#print objects[i]['nameblob']
            %if objects[i]['nameblob']:
              %#print 'OK'
              %pattern_nameblob = re.compile("\*\*name=(.*)")
              %m = pattern_nameblob.match(objects[i]['nameblob'])
              %if m:
                %name = m.group(1).strip()
            %#else:
              %#print 'NOT OK'
              %#name = ''
          %#else:
            %#print 'NO NAME'
            %#name = ''
          %data = objects[i]['data']
          
          %# convert Type to upper case and strip it
          %Type = Type.upper().strip()
          %# split data by spaces and new lines
          %data = re.split('\s+',data)
          %# remove empty lines from data
          %data = filter(None, data)
          
          %entry = Entry()
          %entry.Type = Type
          %entry.name = name
          %entry.data = data
          %entries.append(entry)
