function [ handles, ok ] = PP_generate_plot(handles)
  disp('function pushbutton_generate_plot_Callback(hObject, eventdata, handles)')
  % hObject    handle to pushbutton_generate_plot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)

  if ~handles.isLoaded
    disp('WARNING: Please load a file first');
    return;
  end
  
  col = handles.col;
  handles.dataname = handles.colplot(col);
  max = handles.maxplotvalue;
  
  if handles.Type == 1
    disp('WARNING: No plot generator available yet for probes.')
    ok = 0;
    return;
  elseif handles.Type == 2
    handles.snapfile = handles.TimeSnapshotFile;
    plotgen(max,col,handles);
  elseif handles.Type == 3
    handles.snapfile = handles.FrequencySnapshotFile;
    plotgen(max,col,handles);
  else
    error('Unknown data type');
    ok = 0;
    return;
  end
  ok = 1;
end
