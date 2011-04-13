function postprocessor_CLI()
  disp('function postprocessor_CLI()')
  handles = struct;
  handles.workdir = pwd();
  handles.snaplist = {};
  handles.geolist = {};
  handles.inplist = {};
  [handles, dirChosen] = browse(handles);
  if ~dirChosen
    return
  end
  handles.Type = 1;
  handles.ProbeID = 1;
  handles.TimeSnapshotID = 1;
  handles.FrequencySnapshotID = 1;
  handles.geometryfile = 1;
  handles.inputfile = 1;
  [ handles, isLoaded ] = load_data(handles);
  if ~isLoaded
    return
  end
  handles.col = 1;
  handles.maxplotvalue = 1;
  handles = generate_plot(handles);
end

function [handles, dirChosen] = browse(handles)
  disp('function pushbutton_browse_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in pushbutton_browse.
  % hObject    handle to pushbutton_browse (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  new_dir = uigetdir(handles.workdir);
  if new_dir == 0
    dirChosen = 0;
    return;
  end
  handles = setWorkDir(handles,new_dir);
  dirChosen = 1;
  return;
end

function handles = setWorkDir(handles, new_dir)
  disp('function [handles] = setWorkDir(handles, new_dir)')
  handles.workdir = new_dir;

  handles.data_files = {};
  handles.ProbeList = {};
  handles.TimeSnapshotList = {};
  handles.FrequencySnapshotList = {};
  handles.geolist = {};
  handles.inplist = {};

  data_files = [dir(fullfile(new_dir,'*.prn')); dir(fullfile(new_dir,'*.dat'))];
  handles.data_files = {data_files.name}; handles.data_files = handles.data_files';
  for idx=1:length(handles.data_files)
    if ~isempty(regexp(handles.data_files{idx},'^p.*id\.(prn|dat)$','ignorecase'))
      handles.ProbeList{end+1} = handles.data_files{idx};
    end
    if ~isempty(regexp(handles.data_files{idx},'^[xyz]\d+id\d\d\.(prn|dat)$','ignorecase'))
      handles.TimeSnapshotList{end+1} = handles.data_files{idx};
    end
    if ~isempty(regexp(handles.data_files{idx},'^[xyz]ABid\d\d\.(prn|dat)$','ignorecase'))
      handles.FrequencySnapshotList{end+1} = handles.data_files{idx};
    end
  end
 
  %prn_files = [dir(fullfile(new_dir,'*.prn')); dir(fullfile(new_dir,'*.dat'))];
  %handles.snaplist = {prn_files.name}; handles.snaplist = handles.snaplist';
  %prn_files = char(prn_files.name);
    
  geo_files = dir(fullfile(new_dir,'*.geo'));
  handles.geolist = {geo_files.name}; handles.geolist = handles.geolist';
  geo_files = char(geo_files.name);
  
  inp_files = dir(fullfile(new_dir,'*.inp'));
  handles.inplist = {inp_files.name}; handles.inplist = handles.inplist';
  inp_files = char(inp_files.name);

  %prn_files
  %disp(['prn_files=',prn_files(:)']);
  % if(prn_files=='')
  %     disp('no .prn files found');
  % end

  %if length(prn_files)>0
    %set(handles.popupmenu_inputsnapshot,'String',prn_files);
  %end
  %if length(geo_files)>0
    %set(handles.popupmenu_geometryfile,'String',geo_files);
  %end
  %if length(inp_files)>0
    %set(handles.popupmenu_inputfile,'String',inp_files);
  %end

  clear data_files geo_files inp_files;
  
  %handles.snaplist
end

function [ handles, isLoaded ] = load_data(handles)
  disp('function pushbutton_load_data_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in pushbutton_load_data.
  % hObject    handle to pushbutton_load_data (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  val = handles.geometryfile;
  if (val<1) | (length(handles.geolist)<val)
    isLoaded = 0;
    return
  end
  geofile = handles.geolist{val};
  handles.geofile = [handles.workdir, filesep, geofile];
  
  val = handles.inputfile;
  if (val<1) | (length(handles.inplist)<val)
    isLoaded = 0;
    return
  end
  inpfile = handles.inplist{val};
  handles.inpfile = [handles.workdir, filesep, inpfile];

  if handles.Type == 1
    val = handles.ProbeID;
    if (val<1) | (length(handles.ProbeList)<val)
      isLoaded = 0;
      return
    end
    name = handles.ProbeList{val};
    handles.ProbeFile = [handles.workdir, filesep, name];
    %load snapshot data
    [handles.header, handles.fin1] = hdrload(handles.ProbeFile);
  elseif handles.Type == 2
    val = handles.TimeSnapshotID;
    if (val<1) | (length(handles.TimeSnapshotList)<val)
      isLoaded = 0;
      return
    end
    name = handles.TimeSnapshotList{val};
    handles.TimeSnapshotFile = [handles.workdir, filesep, name];
    [handles.header, handles.fin1] = hdrload(handles.TimeSnapshotFile);
  elseif handles.Type == 3
    val = handles.FrequencySnapshotID;
    if (val<1) | (length(handles.FrequencySnapshotList)<val)
      isLoaded = 0;
      return
    end
    name = handles.FrequencySnapshotList{val};
    handles.FrequencySnapshotFile = [handles.workdir, filesep, name];
    [handles.header, handles.fin1] = hdrload(handles.FrequencySnapshotFile);
  else
    error('Unknown data type')
    return
  end
  
  %determine orientation of snapshot
  handles.gr = size(handles.fin1);
  columns = strread(handles.header,'%s');
  if strcmp(columns(1),'y') && strcmp(columns(2),'z')
      handles.plane = 1;
      handles.maxy = handles.fin1(handles.gr(1),1);
      handles.maxz = handles.fin1(handles.gr(1),2);
  elseif strcmp(columns(1),'x') && strcmp(columns(2),'z')
      handles.plane = 2;
      handles.maxx = handles.fin1(handles.gr(1),1);
      handles.maxz = handles.fin1(handles.gr(1),2);
  else
      handles.plane = 3;
      handles.maxx = handles.fin1(handles.gr(1),1);
      handles.maxy = handles.fin1(handles.gr(1),2);
  end
  
  handles.colplot = columns; % all headers
  columns = columns(3:length(columns));
  columns = char(columns);
  handles.plotcolumn = columns; % all headers except the two first ones
  
  isLoaded = 1;
end

function handles = generate_plot(handles)
  disp('function pushbutton_generate_plot_Callback(hObject, eventdata, handles)')
  % hObject    handle to pushbutton_generate_plot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  %handles.colplot
  
  %handles.plotcolumn
  
  col = handles.col;
  %col = col+2;
  handles.dataname = handles.colplot(col);
  max = handles.maxplotvalue;
  
  plotgen(max,col,handles);
end
