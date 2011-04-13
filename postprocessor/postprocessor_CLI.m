function postprocessor_CLI()
  disp('function postprocessor_CLI()')
  handles = struct;
  handles.workdir = pwd();
  handles.snaplist = {};
  handles.geolist = {};
  handles.inplist = {};
  [handles, dirChosen] = browse(handles);
  if dirChosen;
    handles.inputsnapshot = 1;
    handles.geometryfile = 1;
    handles.inputfile = 1;
    handles = load_data(handles);
  end
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

  handles.snaplist = {};
  handles.geolist = {};
  handles.inplist = {};

  prn_files = [dir(fullfile(new_dir,'*.prn')); dir(fullfile(new_dir,'*.dat'))];
  handles.snaplist = {prn_files.name}; handles.snaplist = handles.snaplist';
  prn_files = char(prn_files.name);
    
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

  clear prn_files geo_files inp_files;
  
  %handles.snaplist
end

function handles = load_data(handles)
  disp('function pushbutton_load_data_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in pushbutton_load_data.
  % hObject    handle to pushbutton_load_data (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  val = handles.inputsnapshot;
  if (val<1) | (length(handles.snaplist)<val)
    return
  end
  snapfile = handles.snaplist{val};
  handles.snapfile = [handles.workdir, filesep, snapfile];
  
  val = handles.geometryfile;
  if (val<1) | (length(handles.geolist)<val)
    return
  end
  geofile = handles.geolist{val};
  handles.geofile = [handles.workdir, filesep, geofile];
  
  val = handles.inputfile;
  if (val<1) | (length(handles.inplist)<val)
    return
  end
  inpfile = handles.inplist{val};
  handles.inpfile = [handles.workdir, filesep, inpfile];
  
  %load snapshot data
  [header, handles.fin1] = hdrload(handles.snapfile);
  
  %determine orientation of snapshot
  handles.gr = size(handles.fin1);
  columns = strread(header,'%s');
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
  
  handles.colplot = columns;
  columns = columns(3:length(columns));
  columns = char(columns);
  handles.plotcolumn = columns;
end
