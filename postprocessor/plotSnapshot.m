function plotSnapshot(snapshot_filename, column, maxval, handles, rotate90, hide_figures, imageSaveName)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % function plotSnapshot(snapshot_filename, column, maxval, handles, rotate90, hide_figures, imageSaveName)
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %Function to display results from frequency snapshots and poynting
  %vector calculations from University of Bristol FDTD software
  %
  %Written by Ian Buss 2006
  %
  %Must be used in conjunction with companion files: readtextfile.m,
  %hdrload.m
  %
  %Version 4.2
  %
  %For Poynting vector plots in the same format use snap_poy_int.m
  % TODO: Locate snap_poy_int.m
  % Arguments:
  % column = column ID, 1 being the first column of the snaphot .prn file, i.e. the xy/yz/zx columns are included
  %
  % required attributes of handles:
  % ===============================
  % handles.AllHeaders
  % handles.autosave
  % handles.colour
  % handles.data
  % handles.geofile
  % handles.geometry
  % handles.dataSize
  % handles.inpfile
  % handles.interpolate
  % handles.modulus
  % handles.plane
  % handles.surface
  % handles.Type
  % handles.drawColorBar
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  if exist('hide_figures','var')==0; hide_figures = false; end
  if exist('rotate90','var')==0; rotate90 = false; end
  
  if exist('handles','var')==0 || isfield(handles,'drawColorBar')==0; handles.drawColorBar = true; end
  if exist('handles','var')==0 || isfield(handles,'autosave')==0; handles.autosave = 0; end
  if exist('handles','var')==0 || isfield(handles,'colour')==0; handles.colour = 1; end
  if exist('handles','var')==0 || isfield(handles,'geometry')==0; handles.geometry = 0; end
  if exist('handles','var')==0 || isfield(handles,'interpolate')==0; handles.interpolate = 0; end
  if exist('handles','var')==0 || isfield(handles,'modulus')==0; handles.modulus = 0; end
  if exist('handles','var')==0 || isfield(handles,'surface')==0; handles.surface = 1; end

  if exist('handles','var')==0 || ...
     isfield(handles,'header')==0 || ...
     isfield(handles,'data')==0 || ...
     isfield(handles,'dataSize')==0 || ...
     isfield(handles,'plane')==0 || ...
     isfield(handles,'AllHeaders')==0
    
    [handles.header, handles.data] = hdrload(snapshot_filename);
    handles.dataSize = size(handles.data);
    columns = strread(handles.header,'%s');
    if strcmp(columns(1),'y') && strcmp(columns(2),'z')
      handles.plane = 1;
    elseif strcmp(columns(1),'x') && strcmp(columns(2),'z')
      handles.plane = 2;
    else
      handles.plane = 3;
    end
    handles.AllHeaders = columns; % all headers
    
  end

  if exist('column','var')==0
    disp('ERROR: no column specified. Please choose from the following:');
    for i=1:length(handles.AllHeaders)
      disp([num2str(i), ':' ,handles.AllHeaders{i}])
    end
    error('TODO: add column selector');
  end

  if exist('maxval','var')==0
    maxval = NaN;
  end
  
  % frequency snapshot specific
  [handles.Type, type_name] = getDataType(snapshot_filename);

  if handles.geometry==1
    if exist('handles','var') && isfield(handles,'geofile') && isfield(handles,'inpfile')
      % load geometry data
      [entries,FDTDobj] = GEO_INP_reader({handles.geofile,handles.inpfile});
    else
      error('ERROR: you need to specify geo and inp file in order to show the geometry.');
    end
  end
  
  %% Determine size of snapshot
  ii=1; ValPrev = handles.data(ii,1); grid_j = 1;
  while ii<handles.dataSize(1)
    if handles.data(ii,1) ~= ValPrev
      ValPrev = handles.data(ii,1);
      grid_j = grid_j+1;
    end
    ii=ii+1;
  end
  grid_i = handles.dataSize(1)/grid_j;
  
  %% Create meshgrids for snapshot
  for pp=1:grid_j
    for qq=1:grid_i
      i(pp,qq)=handles.data(qq,2);
    end
  end
  
  for pp=1:grid_j
    for qq=1:grid_i
      j(pp,qq)=handles.data((qq+((pp-1)*grid_i)),1);
    end
  end
  
  %% Load column of choice to data
  modu = 1;
  rawdata = handles.data(:,column);
  if handles.modulus == 1
    data = abs(rawdata);
  else
    data = rawdata;
    if min(data) < 0
      modu = 0;
    end
  end

  disp(['DATA INFO: min(rawdata) = ',num2str(min(rawdata))]);
  disp(['DATA INFO: max(rawdata) = ',num2str(max(rawdata))]);
  if min(rawdata)==0 & max(rawdata)==0
    disp('WARNING: empty data');
    return;
  end
  
  if isnan(maxval)
    %maxval = max(data);
    disp(['max(data) = ',num2str(max(data))])
    disp(['mean(data) = ',num2str(mean(data))])
    maxval = 8./9.*max(data)+1./9.*mean(data);
  end
  
  %% Create plot data meshgrid
  count=1;
  for ii=1:grid_j
    kk=grid_i*count;
    for jj=1:grid_i
      k(ii,jj)=data(jj+(kk-grid_i));
    end
    count=count+1;
  end
  
  %% Create figure and plot data
  if hide_figures
    fig = figure('visible','off');
  else
    fig = figure('visible','on');
  end
  grey = 0;
  if (handles.colour)
    colormap(jet(256));
    grey = 0;
  else
    colormap(gray(256));
    grey = 1;
  end
  
  if handles.plane == 1
    if (handles.surface)
      %pcolor(i,j,k)
      surf(i,j,k);
    else
      contour(i,j,k);
    end
  elseif handles.plane == 2
    if (handles.surface)
      %pcolor(i,j,k)
      surf(i,j,k);
    else
      contour(i,j,k);
    end
  else
    if (handles.surface)
      %pcolor(j,i,k)
      surf(j,i,k);
    else
      contour(j,i,k);
    end
  end
  
  %colave = max(fin1(:,column));
  colfig = handles.AllHeaders{column};
  disp(['maxval=',num2str(maxval)]);
  if (modu == 1) || (handles.modulus == 1)
    caxis([0 maxval]);
  else
    caxis([-maxval maxval]);
  end
  AspectRatio = get(gca,'DataAspectRatio');
  AspectRatio(1) = AspectRatio(2);
  set(gca,'DataAspectRatio',AspectRatio);
  if handles.interpolate == 1
    shading interp;
  else
    shading flat;
  end
  
   % to avoid white patches on the image
  if(not(inoctave))
    lighting phong;
  end
  
  %zmin = 0;
  %zmax = maxval;
  %cmin = 0;
  %cmax = maxval;
  
  % TODO: handle NaNs
  switch handles.plane
    case 1
      xlabel('z');
      ylabel('y');
      if handles.geometry
        foo = [FDTDobj.box.lower(3), FDTDobj.box.upper(3), FDTDobj.box.lower(2), FDTDobj.box.upper(2)];%, zmin,zmax,cmin,cmax];
      else
        foo = [ i(1,1),i(1,size(i,2)) , j(1,1),j(size(j,1),1)];%, zmin,zmax,cmin,cmax ];
      end
      axis(foo);
    case 2
      xlabel('z');
      ylabel('x');
      if handles.geometry
        foo = [FDTDobj.box.lower(3), FDTDobj.box.upper(3), FDTDobj.box.lower(1), FDTDobj.box.upper(1)];%, zmin,zmax,cmin,cmax];
      else
        foo = [ i(1,1),i(1,size(i,2)) , j(1,1),j(size(j,1),1)];%, zmin,zmax,cmin,cmax ];
      end
      axis(foo);
    case 3
      xlabel('x');
      ylabel('y');
      if handles.geometry
        foo = [FDTDobj.box.lower(1), FDTDobj.box.upper(1), FDTDobj.box.lower(2), FDTDobj.box.upper(2)];%, zmin,zmax,cmin,cmax];
      else
        foo = [ j(1,1),j(size(j,1),1), i(1,1),i(1,size(i,2))];%, zmin,zmax,cmin,cmax];
      end
      axis(foo);
  end

  % for octave, but might make things easier for matlab too
  view(0,90);
  %view(45,45);
  %axis equal;
  
  if rotate90
    view(90,90);
    if handles.drawColorBar
      colorbar('South');
    end
  else
    if handles.drawColorBar
      colorbar
    end
  end

  % old code from unknown origin and for unknow use  
  %snapshot_filename
  %titlesnap = strread(snapshot_filename,'%s','delimiter','\\');
  %snapfile_full = char(titlesnap(length(titlesnap)));
  
  % much easier and apparently working solution...
  snapfile_full = snapshot_filename

  [ snapfile_full_folder, snapfile_full_basename, snapfile_full_ext ] = fileparts(snapfile_full);
  [ snapfile_full_folder_folder, snapfile_full_folder_basename ] = fileparts(snapfile_full_folder);
  
  title_base = [ snapfile_full_folder_basename, filesep, snapfile_full_basename, snapfile_full_ext ]

  if handles.Type == 1 % probe
    error('ERROR: Trying to plot probe with snapshot plotter');
    return;
  elseif handles.Type == 2 % time snapshot
    % TODO: Add more info to title?
    title([title_base, ': ', char(handles.AllHeaders(column))],'FontWeight','bold','Interpreter','none');
  elseif handles.Type == 3 % frequency snapshot
    if exist('FDTDobj','var')==1
      Nsnap = alphaID_to_numID([snapfile_full_basename, snapfile_full_ext],FDTDobj.flag.id);
      Nsnap
      length(FDTDobj.frequency_snapshots)
      
      freq_snap_MHz = FDTDobj.frequency_snapshots(Nsnap).frequency;
      lambda_snap_mum = get_c0()/freq_snap_MHz;
      lambda_snap_nm = lambda_snap_mum*1e3;
      title([title_base, ': ', char(handles.AllHeaders(column)), ' at ',  num2str(lambda_snap_nm), ' nm, ', num2str(freq_snap_MHz),' MHz'],'FontWeight','bold','Interpreter','none');
    else
      title([title_base, ': ', char(handles.AllHeaders(column))],'FontWeight','bold','Interpreter','none');
    end
  elseif handles.Type == 4 % excitation template
    title([title_base, ': ', char(handles.AllHeaders(column))],'FontWeight','bold','Interpreter','none');  
  else
    warning(['Unknown data type: handles.Type = ',num2str(handles.Type)]);
    %return;
  end
  
  clear titlesnap;
  hold on;
  
  %% Plot Geometry Entities
  if handles.geometry == 1
    disp('DRAWING GEOMETRY')
    t = 0:0.1:((2*pi)+0.1);
    circle_i = cos(t);
    circle_j = sin(t);
    plotting_height_rectangle = max(data)*ones(1,5);
    plotting_height_circle = max(data)*ones(1,length(t));
    switch handles.plane
      case 1 % Z,Y
        for ii=1:length(FDTDobj.block_list)
          lower = FDTDobj.block_list(ii).lower;
          upper = FDTDobj.block_list(ii).upper;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(2) upper(2) upper(2) lower(2) lower(2)], plotting_height_rectangle,'y','LineWidth',1);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          if inner_radius == 0
            I = [(center(3)-outer_radius) ...
                (center(3)+outer_radius) ...
                (center(3)+outer_radius) ...
                (center(3)-outer_radius) ...
                (center(3)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle,'y','LineWidth',1);
          else
            I = [(center(3)-outer_radius) ...
                (center(3)-inner_radius) ...
                (center(3)-inner_radius) ...
                (center(3)-outer_radius) ...
                (center(3)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle,'y','LineWidth',1);
            I = [(center(3)+outer_radius) ...
                (center(3)+inner_radius) ...
                (center(3)+inner_radius) ...
                (center(3)+outer_radius) ...
                (center(3)+outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle,'y','LineWidth',1);
          end
          clear I J;
          clearvars I J;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
        end
        for ii=1:length(FDTDobj.excitations)
          lower = FDTDobj.excitations(ii).P1;
          upper = FDTDobj.excitations(ii).P2;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(2) upper(2) upper(2) lower(2) lower(2)], plotting_height_rectangle,'r','LineWidth',1);
        end
      case 2 % Z,X
        for ii=1:length(FDTDobj.block_list)
          lower = FDTDobj.block_list(ii).lower;
          upper = FDTDobj.block_list(ii).upper;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(1) upper(1) upper(1) lower(1) lower(1)], plotting_height_rectangle,'y','LineWidth',1);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
        end
        for ii=1:length(FDTDobj.excitations)
          lower = FDTDobj.excitations(ii).P1;
          upper = FDTDobj.excitations(ii).P2;
          plot3([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(1) upper(1) upper(1) lower(1) lower(1)], plotting_height_rectangle,'r','LineWidth',1);
        end
      case 3 % X,Y
        for ii=1:length(FDTDobj.block_list)
          lower = FDTDobj.block_list(ii).lower;
          upper = FDTDobj.block_list(ii).upper;
          plot3([lower(1), lower(1), upper(1), upper(1), lower(1)],...
            [lower(2), upper(2), upper(2), lower(2), lower(2)], plotting_height_rectangle,'y','LineWidth',1);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          if inner_radius == 0
            I = [(center(1)-outer_radius) ...
                (center(1)+outer_radius) ...
                (center(1)+outer_radius) ...
                (center(1)-outer_radius) ...
                (center(1)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle,'y','LineWidth',1);
          else
            I = [(center(1)-outer_radius) ...
                (center(1)-inner_radius) ...
                (center(1)-inner_radius) ...
                (center(1)-outer_radius) ...
                (center(1)-outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle,'y','LineWidth',1);
            I = [(center(1)+outer_radius) ...
                (center(1)+inner_radius) ...
                (center(1)+inner_radius) ...
                (center(1)+outer_radius) ...
                (center(1)+outer_radius)];
            J = [(center(2)-(height/2)) ...
                (center(2)-(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)+(height/2)) ...
                (center(2)-(height/2))];
            plot3(I,J,plotting_height_rectangle,'y','LineWidth',1);
          end
          clear I J;
          clearvars I J;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(1);
          J = (outer_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
          I = (inner_radius*circle_i)+center(1);
          J = (inner_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J; clearvars I J;
        end
        for ii=1:length(FDTDobj.excitations)
          lower = FDTDobj.excitations(ii).P1;
          upper = FDTDobj.excitations(ii).P2;
          plot3([lower(1), lower(1), upper(1), upper(1), lower(1)],...
            [lower(2), upper(2), upper(2), lower(2), lower(2)], plotting_height_rectangle,'r','LineWidth',1);
        end
    end
  end
  
  if handles.autosave == 1
    dim = length(snapshot_filename);
    if grey == 1
      figout = [snapshot_filename(1:(dim-4)) '_' colfig '_' num2str(maxval) '_grey.png'];
    else
      figout = [snapshot_filename(1:(dim-4)) '_' colfig '_' num2str(maxval) '.png'];
    end
    disp(['Saving figure as ',figout]);
    %print(fig,'-dpng','-r300',figout);
    print(fig,'-dpng',figout);
  end
  
  % normal saving ( with format string! :D )
  if exist('imageSaveName','var')~=0
    % substitution variable preparation
    [ folder, basename, ext ] = fileparts(snapshot_filename);
    % substitution
    imageSaveNameFinal = imageSaveName;
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%DATE', datestr(now,'yyyymmdd_HHMMSS'));
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%BASENAME', basename);
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%FIELD', num2str(colfig));
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%MAX', num2str(maxval));
    % additional stuff for frequency snapshots
    if handles.Type == 3 % frequency snapshot
      if exist('FDTDobj','var')==1
        Nsnap = alphaID_to_numID([snapfile_full_basename, snapfile_full_ext],FDTDobj.flag.id);
        freq_snap_MHz = FDTDobj.frequency_snapshots(Nsnap).frequency;
        pos_mum = FDTDobj.frequency_snapshots(Nsnap).P1(handles.plane);
        lambda_snap_mum = get_c0()/freq_snap_MHz;
        lambda_snap_nm = lambda_snap_mum*1e3;
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%NSNAP', num2str(Nsnap));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%FREQ_SNAP_MHZ', num2str(freq_snap_MHz));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%LAMBDA_SNAP_MUM', num2str(lambda_snap_mum));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%LAMBDA_SNAP_NM', num2str(lambda_snap_nm));
        imageSaveNameFinal = strrep(imageSaveNameFinal, '%POS_MUM', num2str(pos_mum));
      end
    end
    % saving
    disp(['Saving figure as ',imageSaveNameFinal]);
    print(fig,'-dpng','-r300',imageSaveNameFinal);
    %print(fig,'-depsc','-r1500',imageSaveNameFinal);
    
    % DO NOT CALL THIS IN INTERACTIVE MODE (otherwise the figure never shows up)
    delete(fig); %clear(fig);
  end

  clear i;
  clear j;
  clear k;
  clear FDTDobj;
  clearvars i j k FDTDobj;
  %clear;
  clear all;
  clearvars -global;

end
