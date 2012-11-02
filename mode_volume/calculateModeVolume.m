function mode_volume_mum3 = calculateModeVolume(folder, inpfile, snapDirection)

  % read the input files
  
  snap_plane = snapDirection %'z'
  probe_ident = 'a' % (should be gotten from parsing input files)
  snap_time_number = 1 % (should be gotten from parsing input files)
  
  % convert snapDirection='x','y','z' to 1,2,3
  snapDirInt = (snapDirection - double('x')) + 1;

  FsnapFiles = dir([folder, filesep, snapDirection, '*00.prn']);

  size(FsnapFiles)

  %inpfile = dir([folder,'\*.inp']);
  %inpfile = [folder, filesep, inpfile(1).name];
  [inpEntries, structured_entries] = GEO_INP_reader({ [folder, filesep, inpfile] });

  Snaps = {};
  for m = 1:length(inpEntries)
     data = inpEntries{m}.data;
     if strcmp(lower(inpEntries{m}.type), 'frequency_snapshot')
         % Findout which plane it is
         snapNo = length(Snaps)+1;
         %m
         %data
         disp(['snapDirInt = ',num2str(snapDirInt)])
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
      [header_fsnap, data_fsnap, ui_fsnap, uj_fsnap] = readPrnFile(Snaps{m}.fileName);
      [header_esnap, data_esnap, ui_esnap, uj_esnap] = readPrnFile(Snaps{m}.epsFile);
      
      disp(['==> size(data_fsnap) = ',num2str(size(data_fsnap))]);
      disp(['==> size(ui_fsnap) = ',num2str(size(ui_fsnap))]);
      disp(['==> size(uj_fsnap) = ',num2str(size(uj_fsnap))]);

      disp(['==> size(data_esnap) = ',num2str(size(data_esnap))]);
      disp(['==> size(ui_esnap) = ',num2str(size(ui_esnap))]);
      disp(['==> size(uj_esnap) = ',num2str(size(uj_esnap))]);

      % TODO: I really don't think this should be like this... Looks like a dirty hack...
      if m == length(Snaps)
        thickness = Snaps{m}.pos-Snaps{m-1}.pos;
      else
        thickness = Snaps{m+1}.pos-Snaps{m}.pos;
      end
      
      % get size of full mesh
      v = 1:3;
      ind = find(v~=snapDirInt);
      
      if( length(ui_esnap) == length(mesh{ind(1)}) )
        % full snapshot
        vi = mesh{ind(1)};
      else
        % partial snapshot
        vi = diff(ui_esnap);
        data_fsnap = data_fsnap(1:end-1, :, :);
        data_esnap = data_esnap(1:end-1, :, :);
      end

      if( length(uj_esnap) == length(mesh{ind(2)}) )
        % full snapshot
        vj = mesh{ind(2)};
      else
        % partial snapshot
        vj = diff(uj_esnap);
        data_fsnap = data_fsnap(:, 1:end-1, :);
        data_esnap = data_esnap(:, 1:end-1, :);
      end

      Exmod = data_fsnap(:,:,1);
      Eymod = data_fsnap(:,:,4);
      Ezmod = data_fsnap(:,:,7);

      %vi = diff(ui_esnap);
      %vj = diff(uj_esnap);

      %vi = mesh{ind(1)};
      %vj = mesh{ind(2)};

      disp(['==> size(vi) = ',num2str(size(vi))]);
      disp(['==> size(vj) = ',num2str(size(vj))]);

      areaM = vj*vi';
      
      nom = (Exmod.^2+Eymod.^2+Ezmod.^2).*data_esnap(:,:);
      
      % TODO: shouldn't this be:
      % maxVal = max(nom);
      maxVal = max(sum(sum(nom)));
      vv = [vv,maxVal];
      
      if (maxVal>currMax)
        currMax = maxVal;
      end

      disp(['==> size(nom) = ',num2str(size(nom))]);
      disp(['==> size(areaM) = ',num2str(size(areaM))]);
      disp(['==> size(thickness) = ',num2str(size(thickness))]);
      
      Nom = Nom + sum(sum(nom.*areaM*thickness));
      
  %     figure(1)
  %     imagesc(ui(2:end),uj(2:end),nom);
  %     figure(2)
  %     imagesc(eps)
  end
      
  mode_volume_mum3 = Nom/currMax;

  if snapDirection == 'x'
    Lambda_mum = get_c0()/structured_entries.frequency_snapshots_X(1).frequency
  elseif snapDirection == 'y'
    Lambda_mum = get_c0()/structured_entries.frequency_snapshots_Y(1).frequency
  elseif snapDirection == 'z'
    Lambda_mum = get_c0()/structured_entries.frequency_snapshots_Z(1).frequency
  else
    error(['Invalid snapDirection = ', num2str(snapDirection)])
  end    
  
  % Which of those is correct?
  % n = 3.3;
  % Foptn = mode_volume/(Lambda/(n))^3
  % Foptn = mode_volume/((Lambda/1000)/(2*n))^3
  % Foptn = mode_volume_mum3/(Lambda_mum/(2*n))^3;
  disp(['mode_volume_mum3 = ',num2str(mode_volume_mum3)]);
end
