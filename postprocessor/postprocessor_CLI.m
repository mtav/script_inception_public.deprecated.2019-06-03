function postprocessor_CLI()
  disp('function postprocessor_CLI()')
  handles = struct;
  handles.workdir = getuserdir();
  browse(handles);
  %if isempty(WORKDIR)
    %return;
  %end
end

function WORKDIR = browse(handles)
  disp('function pushbutton_browse_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in pushbutton_browse.
  % hObject    handle to pushbutton_browse (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  new_dir = uigetdir(handles.workdir);
  if new_dir == 0
      return;
  end
  setWorkDir(handles,new_dir);
end

function setWorkDir(handles, new_dir)
  disp('function [handles] = setWorkDir(handles, new_dir)')
  %handles.workdir = new_dir;

  %set(handles.label_working_directory,'String',new_dir);

  %handles.snaplist = {};
  %handles.geolist = {};
  %handles.inplist = {};

  %prn_files = [dir(fullfile(new_dir,'*.prn')); dir(fullfile(new_dir,'*.dat'))];
  
  %handles.snaplist = {prn_files.name}';
  %prn_files = char(prn_files.name);
  %geo_files = dir(fullfile(new_dir,'*.geo'));
  %handles.geolist = {geo_files.name}';
  %geo_files = char(geo_files.name);
  %inp_files = dir(fullfile(new_dir,'*.inp'));
  %handles.inplist = {inp_files.name}';
  %inp_files = char(inp_files.name);

  %% disp(['prn_files=',prn_files]);
  %% if(prn_files=='')
  %%     disp('no .prn files found');
  %% end

  %if length(prn_files)>0
    %set(handles.popupmenu_inputsnapshot,'String',prn_files);
  %end
  %if length(geo_files)>0
    %set(handles.popupmenu_geometryfile,'String',geo_files);
  %end
  %if length(inp_files)>0
    %set(handles.popupmenu_inputfile,'String',inp_files);
  %end

  %clear prn_files geo_files inp_files
end
