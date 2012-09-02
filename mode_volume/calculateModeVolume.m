function mode_volume_mum3 = calculateModeVolume(folder, inpfile, snapDirection)

  % read the input files
  
  snap_plane = 'z'
  probe_ident = 'a'
  snap_time_number = 1
  
  % convert snapDirection='x','y','z' to 1,2,3
  snapDirInt = (snapDirection - double('x')) + 1;

  FsnapFiles = dir([folder, filesep, snapDirection, '*00.prn']);

  size(FsnapFiles)

  %inpfile = dir([folder,'\*.inp']);
  %inpfile = [folder, filesep, inpfile(1).name];
  [inpEntries, structured_entries] = GEO_INP_reader({inpfile});

  Snaps = {};
  for m = 1:length(inpEntries)
     data = inpEntries{m}.data;
     if strcmp(lower(inpEntries{m}.type), 'frequency_snapshot')
         % Findout which plane it is
         snapNo = length(Snaps)+1;
         m
         data
         snapDirInt
         % check if the direction of the snapshot corresponds to snapDirection
         if data{7+snapDirInt} == data{10+snapDirInt}
         
              % This way of getting the filename seems a bit dangerous... Does dir() return correctly ordered files?
             filename = FsnapFiles(snapNo).name;
             fileNumStr = filename(2:end-7);
             fileNumStr = fileNumStr - 96*ones(1,length(fileNumStr));
             val = fileNumStr*fliplr([1:25:length(fileNumStr)*25])';
             
             SnapEntry.fileName = [folder, filesep, filename];
             SnapEntry.pos = data{7+snapDirInt};
             
             [ epsfilename, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(val, snap_plane, probe_ident, snap_time_number)
             
             %[folder, filesep, snapDirection, num2str(val), 'a*.prn']
             %epsFile = dir([folder, filesep, snapDirection, num2str(val), 'a*.prn']);
             %epsFile(1)
             SnapEntry.epsFile = [folder, filesep, epsfilename];
             Snaps{snapNo} = SnapEntry;  
         end
     %elseif strcmp(lower(inpEntries{m}.type), 'xmesh')
         %data
         %m
         %error('bleuargh')
         %mesh{1} = data;
     %elseif strcmp(lower(inpEntries{m}.type), 'ymesh')
         %mesh{2} = data;
     %elseif strcmp(lower(inpEntries{m}.type), 'zmesh')
         %mesh{3} = data;
     end
  end

  mesh{1} = structured_entries.xmesh;
  mesh{2} = structured_entries.ymesh;
  mesh{3} = structured_entries.zmesh;

  % calculate the mode volume
  currMax = 0;
  Nom = 0;
  vv = [];

  for m = 1:length(Snaps)
      disp(m)
      [header, data, ui, uj] = readPrnFile(Snaps{m}.fileName);
      if m == length(Snaps)
          thickness = Snaps{m}.pos-Snaps{m-1}.pos;
      else
          thickness = Snaps{m+1}.pos-Snaps{m}.pos;
      end
      Exmod = data(:,:,1);
      Eymod = data(:,:,4);
      Ezmod = data(:,:,7);
      
      v = 1:3;
      ind = find(v~=snapDirInt);

      vi = mesh{ind(1)};
      vj = mesh{ind(2)};
      
      areaM = vj*vi';
      
      [header, eps, ui, uj] = readPrnFile(Snaps{m}.epsFile);
      
      nom = (Exmod.^2+Eymod.^2+Ezmod.^2).*eps(:,:);
      
      % TODO: shouldn't this be:
      % maxVal = max(nom);
      maxVal = max(sum(sum(nom)));
      vv = [vv,maxVal];
      
      if (maxVal>currMax)
          currMax = maxVal;
      end
          
      Nom = Nom + sum(sum(nom.*areaM*thickness));
      
  %     figure(1)
  %     imagesc(ui(2:end),uj(2:end),nom);
  %     figure(2)
  %     imagesc(eps)
  end
      
  mode_volume_mum3 = Nom/currMax;

  % Which of those 2 is correct?
  Lambda_mum = get_c0()/structured_entries.frequency_snapshots_Z(1).frequency
  % n = 3.3;
  % Foptn = mode_volume/(Lambda/(n))^3
  % Foptn = mode_volume/((Lambda/1000)/(2*n))^3
  % Foptn = mode_volume_mum3/(Lambda_mum/(2*n))^3;
  disp(['mode_volume_mum3 = ',num2str(mode_volume_mum3)]);
end
