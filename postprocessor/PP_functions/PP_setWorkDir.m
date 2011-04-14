function [handles, ok] = PP_setupLists(handles)
  disp('function [handles] = setWorkDir(handles, new_dir)')

  handles.data_files = {};
  handles.ProbeList = {};
  handles.TimeSnapshotList = {};
  handles.FrequencySnapshotList = {};
  handles.geolist = {};
  handles.inplist = {};

  data_files = [dir(fullfile(new_dir,'*.prn')); dir(fullfile(new_dir,'*.dat'))];
  handles.data_files = {data_files.name}; handles.data_files = handles.data_files';
  for idx=1:length(handles.data_files)
    unknown = 1;
    if ~isempty(regexp(handles.data_files{idx},'^p.*\.(prn|dat)$','ignorecase'))
      handles.ProbeList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if ~isempty(regexp(handles.data_files{idx},'^[xyz]\d+.*\d\d\.(prn|dat)$','ignorecase'))
      handles.TimeSnapshotList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if ~isempty(regexp(handles.data_files{idx},'^[xyz][a-z{|}~][a-z{]?.*\d\d\.(prn|dat)$','ignorecase'))
      handles.FrequencySnapshotList{end+1} = handles.data_files{idx};
      unknown = 0;
    end
    if unknown & isempty(regexp(handles.data_files{idx},'^ref\.(prn|dat)$','ignorecase'))
      error(['unknown data : ',handles.data_files{idx}])
      ok = 0;
      return
    end
  end
 
  disp([ 'length(handles.data_files)=', num2str(length(handles.data_files)) ])
  disp([ 'length(handles.ProbeList)=', num2str(length(handles.ProbeList)) ])
  disp([ 'length(handles.TimeSnapshotList)=', num2str(length(handles.TimeSnapshotList)) ])
  disp([ 'length(handles.FrequencySnapshotList)=', num2str(length(handles.FrequencySnapshotList)) ])
  total = length(handles.ProbeList) + length(handles.TimeSnapshotList) + length(handles.FrequencySnapshotList) + 1;
  disp(['total = ',num2str(total)])
 
  %prn_files = [dir(fullfile(new_dir,'*.prn')); dir(fullfile(new_dir,'*.dat'))];
  %handles.snaplist = {prn_files.name}; handles.snaplist = handles.snaplist';
  %prn_files = char(prn_files.name);
    
  geo_files = dir(fullfile(new_dir,'*.geo'));
  handles.geolist = {geo_files.name}; handles.geolist = handles.geolist';
  %geo_files = char(geo_files.name);
  
  inp_files = dir(fullfile(new_dir,'*.inp'));
  handles.inplist = {inp_files.name}; handles.inplist = handles.inplist';
  %inp_files = char(inp_files.name);

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
  ok = 1;
end
