function plotgen(maxval, column, handles, imageSaveName, hide_figures, invert_axes)
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
  % handles.snapfile
  % handles.surface
  % handles.Type
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  if exist('hide_figures','var')==0
    hide_figures = false;
  end

  if exist('invert_axes','var')==0
    invert_axes = false;
  end

  % load geometry data
  [entries,FDTDobj]=GEO_INP_reader({handles.geofile,handles.inpfile});
  
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
    maxval = max(data);
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
  colorbar
  AspectRatio = get(gca,'DataAspectRatio');
  AspectRatio(1) = AspectRatio(2);
  set(gca,'DataAspectRatio',AspectRatio);
  if handles.interpolate == 1
    shading interp;
  else
    shading flat;
  end
  % TODO: handle NaNs
  switch handles.plane
    case 1
      xlabel('z')
      ylabel('y')
      foo = [FDTDobj.box.lower(3) FDTDobj.box.upper(3) FDTDobj.box.lower(2) FDTDobj.box.upper(2)];
      axis(foo)
    case 2
      xlabel('z')
      ylabel('x')
      foo = [FDTDobj.box.lower(3) FDTDobj.box.upper(3) FDTDobj.box.lower(1) FDTDobj.box.upper(1)];
      axis(foo)
    case 3
      xlabel('x')
      ylabel('y')
      foo = [FDTDobj.box.lower(1) FDTDobj.box.upper(1) FDTDobj.box.lower(2) FDTDobj.box.upper(2)];
      axis(foo)
  end
  titlesnap = strread(handles.snapfile,'%s','delimiter','\\');
  snapfile_full = char(titlesnap(length(titlesnap)));

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
    Nsnap = alphaID_to_numID([snapfile_full_basename, snapfile_full_ext],FDTDobj.flag.id);
    freq_snap_MHz = FDTDobj.frequency_snapshots(Nsnap).frequency;
    lambda_snap_mum = get_c0()/freq_snap_MHz;
    lambda_snap_nm = lambda_snap_mum*1e3;
    title([title_base, ': ', char(handles.AllHeaders(column)), ' at ',  num2str(lambda_snap_nm), ' nm, ', num2str(freq_snap_MHz),' MHz'],'FontWeight','bold','Interpreter','none');
  else
    error('ERROR: Unknown data type');
    return;
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
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
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
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(3);
          J = (outer_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
          I = (inner_radius*circle_i)+center(3);
          J = (inner_radius*circle_j)+center(1);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
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
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center;
          outer_radius = FDTDobj.sphere_list(ii).outer_radius;
          inner_radius = FDTDobj.sphere_list(ii).inner_radius;
          I = (outer_radius*circle_i)+center(1);
          J = (outer_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
          I = (inner_radius*circle_i)+center(1);
          J = (inner_radius*circle_j)+center(2);
          plot3(I, J, plotting_height_circle, 'y','LineWidth',1); clear I J;
        end
    end
  end
  
  if handles.autosave == 1
    dim = length(handles.snapfile);
    if grey == 1
      figout = [handles.snapfile(1:(dim-4)) '_' colfig '_' num2str(maxval) '_grey.png'];
    else
      figout = [handles.snapfile(1:(dim-4)) '_' colfig '_' num2str(maxval) '.png'];
    end
    disp(['Saving figure as ',figout]);
    %print(fig,'-dpng','-r300',figout);
    print(fig,'-dpng',figout);
  end
  
  % normal saving ( with format string! :D )
  if exist('imageSaveName','var')~=0
    % substitution variable preparation
    [ folder, basename, ext ] = fileparts(handles.snapfile);
    % substitution
    imageSaveNameFinal = imageSaveName;
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%DATE', datestr(now,'yyyymmdd_HHMMSS'));
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%BASENAME', basename);
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%FIELD', num2str(colfig));
    imageSaveNameFinal = strrep(imageSaveNameFinal, '%MAX', num2str(maxval));
    % additional stuff for frequency snapshots
    if handles.Type == 3 % frequency snapshot
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
    % saving
    disp(['Saving figure as ',imageSaveNameFinal]);
    %print(fig,'-dpng','-r300',imageSaveNameFinal);
    print(fig,'-depsc','-r1500',imageSaveNameFinal);
  end

end
