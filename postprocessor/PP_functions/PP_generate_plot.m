function [ handles, ok ] = PP_generate_plot(handles)
  disp('function pushbutton_generate_plot_Callback(hObject, eventdata, handles)')
  % hObject    handle to pushbutton_generate_plot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  if ~handles.isLoaded
    disp('WARNING: Please load a file first');
    ok = 0;
    return;
  end
  
  col = handles.col;
  handles.dataname = handles.AllHeaders(col);  
  zlimits = [ handles.minplotvalue, handles.maxplotvalue ];
  
  if handles.Type == 1
    plotProbe(handles.ProbeFile, handles.col, handles.autosave);
  elseif handles.Type == 2
    handles.snapfile = handles.TimeSnapshotFile;
    plotSnapshot(handles.snapfile, col, zlimits, handles);
  elseif handles.Type == 3
    handles.snapfile = handles.FrequencySnapshotFile;
    plotSnapshot(handles.snapfile, col, zlimits, handles);
  elseif handles.Type == 4
    handles.snapfile = handles.ExcitationTemplateFile;
    plotSnapshot(handles.snapfile, col, zlimits, handles);
  elseif handles.Type == 5
    handles.snapfile = handles.SnapshotFile;
    plotSnapshot(handles.snapfile, col, zlimits, handles);
  else
    error('Unknown data type');
    ok = 0;
    return;
  end
  ok = 1;
end
