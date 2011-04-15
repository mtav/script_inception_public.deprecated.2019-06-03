function varargout = postprocessor(varargin)
  disp('function varargout = postprocessor(varargin)')
  %
  % usage examples:
  % postprocessor
  % postprocessor({'H:\DATA\IN\loncar_test_4'})
  %
  % postprocessor v4, written by Ian Buss 2007
  %
  % POSTPROCESSOR M-file for postprocessor.fig
  %      POSTPROCESSOR, by itself, creates a new POSTPROCESSOR or raises the existing
  %      singleton*.
  %
  %      H = POSTPROCESSOR returns the handle to a new POSTPROCESSOR or the handle to
  %      the existing singleton*.
  %
  %      POSTPROCESSOR('CALLBACK',hObject,eventData,handles,...) calls the local
  %      function named CALLBACK in POSTPROCESSOR.M with the given input arguments.
  %
  %      POSTPROCESSOR('Property','Value',...) creates a new POSTPROCESSOR or raises the
  %      existing singleton*.  Starting from the left, property value pairs are
  %      applied to the GUI before postprocessor_OpeningFunction gets called.  An
  %      unrecognized property name or invalid value makes property application
  %      stop.  All inputs are passed to postprocessor_OpeningFcn via varargin.
  %
  %      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
  %      instance to run (singleton)".
  %
  % See also: GUIDE, GUIDATA, GUIHANDLES
  
  % Copyright 2002-2003 The MathWorks, Inc.
  
  % Edit the above text to modify the response to help postprocessor
  
  % Last Modified by GUIDE v2.5 14-Apr-2011 14:53:22
  
  % Begin initialization code - DO NOT EDIT
  gui_Singleton = 1;
  gui_State = struct('gui_Name',       mfilename, ...
                     'gui_Singleton',  gui_Singleton, ...
                     'gui_OpeningFcn', @postprocessor_OpeningFcn, ...
                     'gui_OutputFcn',  @postprocessor_OutputFcn, ...
                     'gui_LayoutFcn',  [] , ...
                     'gui_Callback',   []);
  if nargin && ischar(varargin{1})
      gui_State.gui_Callback = str2func(varargin{1});
  end
  
  if nargout
      [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
  else
      gui_mainfcn(gui_State, varargin{:});
  end
  % End initialization code - DO NOT EDIT
end

function postprocessor_OpeningFcn(hObject, eventdata, handles, varargin)
  disp('function postprocessor_OpeningFcn(hObject, eventdata, handles, varargin)')
  % --- Executes just before postprocessor is made visible.
  % This function has no output args, see OutputFcn.
  % hObject    handle to figure
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  % varargin   command line arguments to postprocessor (see VARARGIN)

  % Choose default command line output for postprocessor
  handles.output = hObject;

  % to prevent errors on attempts to plot before loading
  handles.isLoaded = 0;

  disp('=== ARGUMENT INFO ===')
  disp(['nargin = ',num2str(nargin)]);
  disp(['nargout = ',num2str(nargout)]);
  for k = 1:length(varargin)
    disp(varargin{k});
  end
  disp('=====================')

  if nargin>4
    disp('We have input');
  end

  % set default value
  handles.workdir = pwd();
  
  % set GUI default values
  set(handles.radiobutton_TimeSnapshot,'Value',1);
  set(handles.checkbox_geometry,'Value',1);
  set(handles.radiobutton_surface,'Value',1);

  % CLI input arg handling
  if nargin > 3
    if exist(varargin{1}{1},'dir')
      handles.workdir = varargin{1}{1};
    else
      %errordlg({'Input argument must be a valid folder'},'Input Argument Error!');
      disp('WARNING: Input Argument Error!: Input argument must be a valid folder');
      guidata(hObject, handles);
    end
  end

  [handles] = setupListsGUI(handles);

  % Update handles structure
  guidata(hObject, handles);

  % UIWAIT makes postprocessor wait for user response (see UIRESUME)
  % uiwait(handles.figure1);
end

function varargout = postprocessor_OutputFcn(hObject, eventdata, handles)
  disp('function varargout = postprocessor_OutputFcn(hObject, eventdata, handles)')
  % --- Outputs from this function are returned to the command line.
  % varargout  cell array for returning output args (see VARARGOUT);
  % hObject    handle to figure
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Get default command line output from handles structure
  varargout{1} = handles.output;
end

function popupmenu_Probe_Callback(hObject, eventdata, handles)
  disp('function popupmenu_inputsnapshot_Callback(hObject, eventdata, handles)')
  % --- Executes on selection change in popupmenu_Probe.
  % hObject    handle to popupmenu_Probe (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_Probe contents as cell array
  %        contents{get(hObject,'Value')} returns selected item from popupmenu_Probe
end

function popupmenu_Probe_CreateFcn(hObject, eventdata, handles)
  disp('function popupmenu_inputsnapshot_CreateFcn(hObject, eventdata, handles)')
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_Probe (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function popupmenu_inputfile_Callback(hObject, eventdata, handles)
  disp('function popupmenu_inputfile_Callback(hObject, eventdata, handles)')
  % --- Executes on selection change in popupmenu_inputfile.
  % hObject    handle to popupmenu_inputfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_inputfile contents as cell array
  %        contents{get(hObject,'Value')} returns selected item from popupmenu_inputfile
end

function popupmenu_inputfile_CreateFcn(hObject, eventdata, handles)
  disp('function popupmenu_inputfile_CreateFcn(hObject, eventdata, handles)')
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_inputfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function pushbutton_load_data_Callback(hObject, eventdata, handles)
  disp('function pushbutton_load_data_Callback(hObject, eventdata, handles)')
  
  % get from GUI
  if get(handles.radiobutton_Probe,'Value')
    handles.Type = 1;
  end
  if get(handles.radiobutton_TimeSnapshot,'Value');
    handles.Type = 2;
  end
  if get(handles.radiobutton_FrequencySnapshot,'Value');
    handles.Type = 3;
  end
  
  handles.ProbeID = get(handles.popupmenu_Probe,'Value');
  handles.TimeSnapshotID = get(handles.popupmenu_TimeSnapshot,'Value');
  handles.FrequencySnapshotID = get(handles.popupmenu_FrequencySnapshot,'Value');
  handles.geometryfile = get(handles.popupmenu_geometryfile,'Value');
  handles.inputfile = get(handles.popupmenu_inputfile,'Value');
  
  % load data
  [ handles ] = PP_load_data(handles);
  
  % set to GUI
  if handles.isLoaded
    set(handles.popupmenu_plotcolumn,'String',handles.HeadersForPopupList);
    set(handles.text11,'String',['Loaded data: ',handles.snapfile]);
  else
    set(handles.popupmenu_plotcolumn,'String',{''});
    set(handles.text11,'String',['Loaded data: ',{''}]);
  end

  guidata(hObject,handles);
end

function popupmenu_geometryfile_Callback(hObject, eventdata, handles)
  disp('function popupmenu_geometryfile_Callback(hObject, eventdata, handles)')
  % --- Executes on selection change in popupmenu_geometryfile.
  % hObject    handle to popupmenu_geometryfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_geometryfile contents as cell array
  %        contents{get(hObject,'Value')} returns selected item from popupmenu_geometryfile
end

function popupmenu_geometryfile_CreateFcn(hObject, eventdata, handles)
  disp('function popupmenu_geometryfile_CreateFcn(hObject, eventdata, handles)')
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_geometryfile (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function popupmenu_plotcolumn_Callback(hObject, eventdata, handles)
  disp('function popupmenu_plotcolumn_Callback(hObject, eventdata, handles)')
  % --- Executes on selection change in popupmenu_plotcolumn.
  % hObject    handle to popupmenu_plotcolumn (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_plotcolumn contents as cell array
  %        contents{get(hObject,'Value')} returns selected item from popupmenu_plotcolumn
  
  
  % --- Executes during object creation, after setting all properties.
end

function popupmenu_plotcolumn_CreateFcn(hObject, eventdata, handles)
  disp('function popupmenu_plotcolumn_CreateFcn(hObject, eventdata, handles)')
  % hObject    handle to popupmenu_plotcolumn (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function edit_maxplotvalue_Callback(hObject, eventdata, handles)
  disp('function edit_maxplotvalue_Callback(hObject, eventdata, handles)')
  % hObject    handle to edit_maxplotvalue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: get(hObject,'String') returns contents of edit_maxplotvalue as text
  %        str2double(get(hObject,'String')) returns contents of edit_maxplotvalue as a double
end

function edit_maxplotvalue_CreateFcn(hObject, eventdata, handles)
  disp('function edit_maxplotvalue_CreateFcn(hObject, eventdata, handles)')
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit_maxplotvalue (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function radiobutton7_Callback(hObject, eventdata, handles)
  disp('function radiobutton7_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in radiobutton7.
  % hObject    handle to radiobutton7 (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of radiobutton7
  
  
  % --- Executes on button press in radiobutton8.
end

function radiobutton8_Callback(hObject, eventdata, handles)
  disp('function radiobutton8_Callback(hObject, eventdata, handles)')
  % hObject    handle to radiobutton8 (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of radiobutton8
  
  
  % --- Executes on button press in pushbutton_generate_plot.
end

function pushbutton_generate_plot_Callback(hObject, eventdata, handles)
  disp('function pushbutton_generate_plot_Callback(hObject, eventdata, handles)')
  % hObject    handle to pushbutton_generate_plot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % get from GUI
  if get(handles.radiobutton_Probe,'Value')
    handles.col = get(handles.popupmenu_plotcolumn,'Value')+1;
  end
  if get(handles.radiobutton_TimeSnapshot,'Value');
    handles.col = get(handles.popupmenu_plotcolumn,'Value')+2;
  end
  if get(handles.radiobutton_FrequencySnapshot,'Value');
    handles.col = get(handles.popupmenu_plotcolumn,'Value')+2;
  end
  handles.maxplotvalue = str2double(get(handles.edit_maxplotvalue,'String'));
  
  handles.interpolate = get(handles.checkbox_interpolate,'Value');
  handles.autosave= get(handles.checkbox_autosave,'Value');
  handles.geometry= get(handles.checkbox_geometry,'Value');
  handles.modulus = get(handles.checkbox_modulus,'Value');

  handles.colour = get(handles.radiobutton_colour,'Value');
  handles.surface = get(handles.radiobutton_surface,'Value');

  % generate plot
  [ handles, ok ] = PP_generate_plot(handles);

  guidata(hObject,handles);
end

function edit3_Callback(hObject, eventdata, handles)
  disp('function edit3_Callback(hObject, eventdata, handles)')
  % hObject    handle to edit3 (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: get(hObject,'String') returns contents of edit3 as text
  %        str2double(get(hObject,'String')) returns contents of edit3 as a double
end

function [handles] = setupListsGUI(handles)
  [handles, ok] = PP_setupLists(handles);
  if ok
    set(handles.label_working_directory,'String',handles.workdir);
  
    if length(handles.ProbeList)>0
      set(handles.popupmenu_Probe,'String',handles.ProbeList);
    else
      set(handles.popupmenu_Probe,'String',{''});
    end
  
    if length(handles.TimeSnapshotList)>0
      set(handles.popupmenu_TimeSnapshot,'String',handles.TimeSnapshotList);
    else
      set(handles.popupmenu_TimeSnapshot,'String',{''});
    end
  
    if length(handles.FrequencySnapshotList)>0
      set(handles.popupmenu_FrequencySnapshot,'String',handles.FrequencySnapshotList);
    else
      set(handles.popupmenu_FrequencySnapshot,'String',{''});
    end
    
    if length(handles.geolist)>0
      set(handles.popupmenu_geometryfile,'String',handles.geolist);
    else
      set(handles.popupmenu_geometryfile,'String',{''});
    end
    
    if length(handles.inplist)>0
      set(handles.popupmenu_inputfile,'String',handles.inplist);
    else
      set(handles.popupmenu_inputfile,'String',{''});  
    end
  end
end

function edit3_CreateFcn(hObject, eventdata, handles)
  disp('function edit3_CreateFcn(hObject, eventdata, handles)')
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to edit3 (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function pushbutton_browse_Callback(hObject, eventdata, handles)
  disp('function pushbutton_browse_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in pushbutton_browse.
  % hObject    handle to pushbutton_browse (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % get from GUI
  handles.workdir = get(handles.label_working_directory,'String');
  
  % browse
  [handles, dirChosen] = PP_browse(handles);
  
  % set to GUI
  [handles] = setupListsGUI(handles);

  guidata(hObject,handles);
end

function edit4_Callback(hObject, eventdata, handles)
  disp('function edit4_Callback(hObject, eventdata, handles)')
  % hObject    handle to edit4 (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: get(hObject,'String') returns contents of edit4 as text
  %        str2double(get(hObject,'String')) returns contents of edit4 as a double
  
  
  % --- Executes during object creation, after setting all properties.
end

function edit4_CreateFcn(hObject, eventdata, handles)
  disp('function edit4_CreateFcn(hObject, eventdata, handles)')
  % hObject    handle to edit4 (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called

  % Hint: edit controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function checkbox_interpolate_Callback(hObject, eventdata, handles)
  disp('function checkbox_interpolate_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in checkbox_interpolate.
  % hObject    handle to checkbox_interpolate (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of checkbox_interpolate
end

function checkbox_autosave_Callback(hObject, eventdata, handles)
  disp('function checkbox_autosave_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in checkbox_autosave.
  % hObject    handle to checkbox_autosave (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of checkbox_autosave
end

function checkbox_geometry_Callback(hObject, eventdata, handles)
  disp('function checkbox_geometry_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in checkbox_geometry.
  % hObject    handle to checkbox_geometry (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of checkbox_geometry
end

function checkbox_modulus_Callback(hObject, eventdata, handles)
  disp('function checkbox_modulus_Callback(hObject, eventdata, handles)')
  % --- Executes on button press in checkbox_modulus.
  % hObject    handle to checkbox_modulus (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of checkbox_modulus
end

function popupmenu_FrequencySnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_FrequencySnapshot.
  % hObject    handle to popupmenu_FrequencySnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_FrequencySnapshot contents as cell array
  %        contents{get(hObject,'Value')} returns selected item from popupmenu_FrequencySnapshot
end

function popupmenu_FrequencySnapshot_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_FrequencySnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function popupmenu_TimeSnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on selection change in popupmenu_TimeSnapshot.
  % hObject    handle to popupmenu_TimeSnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hints: contents = get(hObject,'String') returns popupmenu_TimeSnapshot contents as cell array
  %        contents{get(hObject,'Value')} returns selected item from popupmenu_TimeSnapshot
end

function popupmenu_TimeSnapshot_CreateFcn(hObject, eventdata, handles)
  % --- Executes during object creation, after setting all properties.
  % hObject    handle to popupmenu_TimeSnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    empty - handles not created until after all CreateFcns called
  
  % Hint: popupmenu controls usually have a white background on Windows.
  %       See ISPC and COMPUTER.
  if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
      set(hObject,'BackgroundColor','white');
  end
end

function radiobutton_Probe_Callback(hObject, eventdata, handles)
  % --- Executes on button press in radiobutton_Probe.
  % hObject    handle to radiobutton_Probe (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of radiobutton_Probe
end

function radiobutton_TimeSnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on button press in radiobutton_TimeSnapshot.
  % hObject    handle to radiobutton_TimeSnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  
  % Hint: get(hObject,'Value') returns toggle state of radiobutton_TimeSnapshot
end

function radiobutton_FrequencySnapshot_Callback(hObject, eventdata, handles)
  % --- Executes on button press in radiobutton_FrequencySnapshot.
  % hObject    handle to radiobutton_FrequencySnapshot (see GCBO)
  % eventdata  reserved - to be defined in a future version of MATLAB
  % handles    structure with handles and user data (see GUIDATA)
  % Hint: get(hObject,'Value') returns toggle state of radiobutton_FrequencySnapshot
end
