function mode_volume_mum3 = calculateModeVolume(folder, inpfile, snap_plane, snap_time_number, refractive_index_defect)
  % snap_plane is 'x','y' or 'z'
  % snap_time_number is the number of the snapshot (i.e. 02 in zaaid02.prn for example)
      
  % convert snap_plane='x','y','z' to 1,2,3
  snapDirInt = (snap_plane - double('x')) + 1;

  % problem 0: this pattern also matches epsilon files, and potentially any other non-mode-volume frequency snapshots
  %FsnapFiles = dir([folder, filesep, snap_plane, '*', sprintf('%02d',snap_time_number),'.prn']);

  %size(FsnapFiles);

  % read the input files
  [inpEntries, structured_entries] = GEO_INP_reader({ [folder, filesep, inpfile] });
  probe_ident = structured_entries.flag.id;

  Snaps = {};
  for numID = 1:length(structured_entries.frequency_snapshots)
    fsnap = structured_entries.frequency_snapshots(numID);
    SnapEntry.pos = fsnap.P2(fsnap.plane);
    [ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID, snap_plane, probe_ident, snap_time_number);
    [ esnap_filename, esnap_alphaID, esnap_pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, probe_ident, 1);
    %disp(['fsnap_filename = ', fsnap_filename]);
    %disp(['esnap_filename = ', esnap_filename]);
    SnapEntry.fileName = [folder, filesep, fsnap_filename];
    SnapEntry.epsFile = [folder, filesep, esnap_filename];
    Snaps{end+1} = SnapEntry;
  end
  
  %return

  %Snaps = {};
  %for m = 1:length(inpEntries)
    %data = inpEntries{m}.data;
    %if strcmp(lower(inpEntries{m}.type), 'frequency_snapshot')
      %% Findout which plane it is
      %snapNo = length(Snaps)+1;
      %%m
      %%data
      %disp(['snapDirInt = ',num2str(snapDirInt)])
      %% check if the direction of the snapshot corresponds to snap_plane
      %if data{7+snapDirInt} == data{10+snapDirInt}
        %% This way of getting the filename seems a bit dangerous... Does dir() return correctly ordered files?
        %% problem 1: this only works if the ID (flag.id) string is of length 1.
        %disp('==================================');
        %filename = FsnapFiles(snapNo).name; % get filename
        %fileNumStr = filename(2:end-7); % extract part between x/y/z and ID string, i.e. the alpha_ID
        %fileNumStr = fileNumStr - 96*ones(1,length(fileNumStr)); % convert alpha_ID of the form 'abc' to list of numbers of the form [1,2,3] (char(97)=a, double('a')=97)
        %% problem 2: This conversion only works if the alpha_ID is of length 1 or 2 (i.e. from 'a' to 'zz')
        %val = fileNumStr*fliplr([1:25:length(fileNumStr)*25])'; % convert list [1-26,1-26,1-26,...] into the corresponding numID
        %disp('==================================');

        %SnapEntry.fileName = [folder, filesep, filename];
        %SnapEntry.pos = data{7+snapDirInt};

        %% Note snap_time_number is usually =1 for epsilon snapshots (since no need for more and first is =1)
        %val
        %snap_plane
        %probe_ident
        %snap_time_number
        %[ epsfilename, alphaID, pair ] = numID_to_alphaID_TimeSnapshot(val, snap_plane, probe_ident, 1)

        %%[folder, filesep, snap_plane, num2str(val), 'a*.prn']
        %%epsFile = dir([folder, filesep, snap_plane, num2str(val), 'a*.prn']);
        %%epsFile(1)
        %SnapEntry.epsFile = [folder, filesep, epsfilename];
        %Snaps{snapNo} = SnapEntry;  
      %end
    %%elseif strcmp(lower(inpEntries{m}.type), 'xmesh')
      %%data
      %%m
      %%error('bleuargh')
      %%mesh{1} = data;
    %%elseif strcmp(lower(inpEntries{m}.type), 'ymesh')
      %%mesh{2} = data;
    %%elseif strcmp(lower(inpEntries{m}.type), 'zmesh')
      %%mesh{3} = data;
    %end
  %end

  mesh{1} = structured_entries.xmesh;
  mesh{2} = structured_entries.ymesh;
  mesh{3} = structured_entries.zmesh;

  % calculate the mode volume
  currMax = 0;
  Nom = 0;
  vv = [];

  for m = 1:length(Snaps)
    disp(['m =',num2str(m)]);
    
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
    % maxVal = max(nom(:));
    maxVal = max(sum(sum(nom)));
    vv = [vv,maxVal];

    if (maxVal>currMax)
      currMax = maxVal;
    end

    disp(['==> size(nom) = ',num2str(size(nom))]);
    disp(['==> size(areaM) = ',num2str(size(areaM))]);
    disp(['==> size(thickness) = ',num2str(size(thickness))]);

    Nom = Nom + sum(sum(nom.*areaM*thickness));
      
  % figure(1)
  % imagesc(ui(2:end),uj(2:end),nom);
  % figure(2)
  % imagesc(eps)
  end
      
  mode_volume_mum3 = Nom/currMax;

  if snap_plane == 'x'
    Lambda_mum = get_c0()/structured_entries.frequency_snapshots_X(1).frequency;
  elseif snap_plane == 'y'
    Lambda_mum = get_c0()/structured_entries.frequency_snapshots_Y(1).frequency;
  elseif snap_plane == 'z'
    Lambda_mum = get_c0()/structured_entries.frequency_snapshots_Z(1).frequency;
  else
    error(['Invalid snap_plane = ', num2str(snap_plane)])
  end    
  
  % n = refractive index of the defect;
  % Foptn = mode_volume_mum3/((Lambda_nm/1000.)/(2*n))^3
  % Foptn = mode_volume_mum3/(Lambda_mum/(2*n))^3;
  Foptn = mode_volume_mum3/((Lambda_mum/(2*refractive_index_defect))^3);

  disp(['mode_volume_mum3 = ',num2str(mode_volume_mum3)]);
  disp(['Lambda_mum = ',num2str(Lambda_mum)]);
  disp(['refractive_index_defect = ',num2str(refractive_index_defect)]);
  disp(['Foptn = ',num2str(Foptn)]);

end
