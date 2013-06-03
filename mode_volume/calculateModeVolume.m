function mode_volume_mum3 = calculateModeVolume(folder, inpfile_list, snap_plane, snap_time_number, refractive_index_defect)
  % function mode_volume_mum3 = calculateModeVolume(folder, inpfile_list, snap_plane, snap_time_number, refractive_index_defect)

  % folder : folder containing the .prn files
  % inpfile_list : of the form {'file1.inp','file2.inp',...}. Note : Full paths should be used!
  % snap_plane : direction of the snapshots ('x','y' or 'z')
  % snap_time_number : the number of the snapshot (i.e. 02 in zaaid02.prn for example)
  % refractive_index_defect : refractive index used to normalize the mode volume (usually refractive index of the defect/cavity)
      
  % convert snap_plane='x','y','z' to 1,2,3
  snapDirInt = (snap_plane - double('x')) + 1;

  % read the input files
  [inpEntries, structured_entries] = GEO_INP_reader(inpfile_list);
  probe_ident = structured_entries.flag.id;

  Snaps = {};
  %for numID = 1:length(structured_entries.frequency_snapshots)
    %fsnap = structured_entries.frequency_snapshots(numID);
  % temporary hack to select only Z snapshots, since that is what we currently use for mode volume calculations. TODO: replace by name-based filter
  for numID = 1:length(structured_entries.frequency_snapshots_Y)
    fsnap = structured_entries.frequency_snapshots_Y(numID);
    SnapEntry.pos = fsnap.P2(fsnap.plane);
    [ fsnap_filename, fsnap_alphaID, fsnap_pair ] = numID_to_alphaID_FrequencySnapshot(numID, snap_plane, probe_ident, snap_time_number);
    [ esnap_filename, esnap_alphaID, esnap_pair ] = numID_to_alphaID_TimeSnapshot(numID, snap_plane, probe_ident, 1);
    %disp(['fsnap_filename = ', fsnap_filename]);
    %disp(['esnap_filename = ', esnap_filename]);
    SnapEntry.fileName = [folder, filesep, fsnap_filename];
    SnapEntry.epsFile = [folder, filesep, esnap_filename];
    Snaps{end+1} = SnapEntry;
  end
  
  mesh{1} = structured_entries.xmesh;
  mesh{2} = structured_entries.ymesh;
  mesh{3} = structured_entries.zmesh;

  % calculate the mode volume
  currMax = 0;
  currMax_m = -1;
  
  Nom = 0;
  vv = [];

  for m = 1:length(Snaps)
    disp(['m =',num2str(m)]);
    
    [header_fsnap, data_fsnap, ui_fsnap, uj_fsnap] = readPrnFile(Snaps{m}.fileName);
    [header_esnap, data_esnap, ui_esnap, uj_esnap] = readPrnFile(Snaps{m}.epsFile);

    %disp(['==> size(data_fsnap) = ',num2str(size(data_fsnap))]);
    %disp(['==> size(ui_fsnap) = ',num2str(size(ui_fsnap))]);
    %disp(['==> size(uj_fsnap) = ',num2str(size(uj_fsnap))]);

    %disp(['==> size(data_esnap) = ',num2str(size(data_esnap))]);
    %disp(['==> size(ui_esnap) = ',num2str(size(ui_esnap))]);
    %disp(['==> size(uj_esnap) = ',num2str(size(uj_esnap))]);
    
    if length(Snaps) <= 1
      disp('WARNING: You are only using one snapshot!!! setting thickness = 1');
      thickness = 1;
    else
      % TODO: Fix this hack
      if m == length(Snaps)
        thickness = abs(Snaps{m}.pos-Snaps{m-1}.pos);
      else
        thickness = abs(Snaps{m+1}.pos-Snaps{m}.pos);
      end
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

    %disp(['==> size(vi) = ',num2str(size(vi))]);
    %disp(['==> size(vj) = ',num2str(size(vj))]);

    areaM = vj*vi';

    nom = data_esnap(:,:).*(Exmod.^2+Eymod.^2+Ezmod.^2);
    %size(nom)

    maxVal = max(nom(:));
    % maxVal = max(sum(sum(nom)));
    % maxVal = max(sum(sum(nom.*areaM*thickness)));
    
    vv = [vv,maxVal];

    if (maxVal>currMax)
      currMax = maxVal;
      currMax_m = m;
    end

    %disp(['==> size(nom) = ',num2str(size(nom))]);
    %disp(['==> size(areaM) = ',num2str(size(areaM))]);
    %disp(['==> size(thickness) = ',num2str(size(thickness))]);

    Nom = Nom + sum(sum(nom.*areaM*thickness));
  
  % figure(1)
  % imagesc(ui_esnap(2:end),uj_esnap(2:end),nom);
  % figure(2)
  % imagesc(eps)
  end
  
  mode_volume_mum3 = Nom/currMax;
  currMax
  currMax_m

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
