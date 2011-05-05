function plotAll(directory, specific_probe_cell)

  % ex: specific_probe_cell = {'pxx.prn','ptyruytue.prn',etc}
  
  if exist('directory','var')==0
    directory = pwd();
  end

  % loop through .sh files  
  [Files,Bytes,Names] = dirr(directory,'\.sh\>','name');
  for script_idx = 1:length(Names)
    script_filename = char(Names(script_idx));
    [ script_folder, script_basename, script_ext ] = fileparts(script_filename);
    handles.geofile = [ script_folder, filesep, script_basename, '.geo' ];
    handles.inpfile = [ script_folder, filesep, script_basename, '.inp' ];
    
    disp(['Processing ', script_folder]);
    [entries,FDTDobj]=GEO_INP_reader({handles.geofile,handles.inpfile});
    excitation = FDTDobj.excitations(1).E;

    if excitation == [1,0,0]
      probe_col = 2
    elseif excitation == [0,1,0]
      probe_col = 3
    elseif excitation == [0,0,1]
      probe_col = 4
    else
      error('Unknown excitation');
    end

    % store workdir
    workdir = pwd();

    % loop through .prn files
    cd(script_folder);
    prnFiles = dir('*.prn');
    for prn_idx = 1:length(prnFiles)
      prn_filename = prnFiles(prn_idx).name;
      [ prn_filename_folder, prn_filename_basename, prn_filename_ext ] = fileparts(prn_filename);
      disp(['Processing ', prn_filename]);
      [type_ID, type_name] = getDataType(prn_filename);
      if strcmp(type_name, 'Probe')
        if ( exist('specific_probe_cell','var')==0 ) | ( exist('specific_probe_cell','var')==1 & max(strcmp([prn_filename_basename, prn_filename_ext],specific_probe_cell)) )
          disp('plotting Probe');
          plotProbe(prn_filename, probe_col, false, [ prn_filename_folder, prn_filename_basename, '.png' ],true);
        end
      elseif strcmp(type_name, 'TimeSnapshot')
        disp('plotting TimeSnapshot');
      elseif strcmp(type_name, 'FrequencySnapshot')
        disp('plotting FrequencySnapshot');
      elseif strcmp(type_name, 'Reference')
        disp('skipping Reference');
      else
        warning('Unknown data type');
      end
    end

    % restore workdir
    cd(workdir);
    
  end
  return;

plotProbe(filename, probe_col, autosave, imageSaveName)
plotgen(maxval,column,handles)

  handles = struct;
  handles.isLoaded = 0;
  handles.workdir = pwd();
  handles.snaplist = {};
  handles.geolist = {};
  handles.inplist = {};

  % browse
  [handles, dirChosen] = PP_browse(handles);
  if ~dirChosen
    return
  end

  handles.Type = 2;
  handles.ProbeID = 1;
  handles.TimeSnapshotID = 1;
  handles.FrequencySnapshotID = 1;
  handles.geometryfile = 1;
  handles.inputfile = 1;
  
  % load data
  [ handles ] = PP_load_data(handles);
  if ~handles.isLoaded
    return
  end
  
  handles.col = 3;
  handles.maxplotvalue = NaN;

  handles.interpolate = 0;
  handles.autosave= 0;
  handles.geometry= 1;
  handles.modulus = 0;

  handles.colour = 1;
  handles.surface = 1;

  % generate plot
  [ handles, ok ] = PP_generate_plot(handles);
end
