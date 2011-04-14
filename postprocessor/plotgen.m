function plotgen(maxval,column,handles)
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
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  % load geometry data
  [entries,FDTDobj]=GEO_INP_reader({handles.geofile,handles.inpfile});
  
  %% Determine size of snapshot
  ii=1; ValPrev = handles.fin1(ii,1); grid_j = 1;
  while ii<handles.gr(1)
      if handles.fin1(ii,1) ~= ValPrev
          ValPrev = handles.fin1(ii,1);
          grid_j = grid_j+1;
      end
      ii=ii+1;
  end
  grid_i = handles.gr(1)/grid_j;
  
  %% Create meshgrids for snapshot
  for pp=1:grid_j
      for qq=1:grid_i
          i(pp,qq)=handles.fin1(qq,2);
      end
  end
  
  for pp=1:grid_j
      for qq=1:grid_i
          j(pp,qq)=handles.fin1((qq+((pp-1)*grid_i)),1);
      end
  end
  
  %% Load column of choice to data
  modu = 1;
  rawdata = handles.fin1(:,column);
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
  figure;
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
  title([char(titlesnap(length(titlesnap))) ': ' char(handles.AllHeaders(column))],'FontWeight','bold');
  clear titlesnap;
  hold on;
  
  %% Plot Geometry Entities
  if handles.geometry == 1
    disp('DRAWING GEOMETRY')
    t = 0:0.1:((2*pi)+0.1);
    circle_i = cos(t);
    circle_j = sin(t);
    switch handles.plane
      case 1
        for ii=1:length(FDTDobj.block_list)
          lower = FDTDobj.block_list(ii).lower;
          upper = FDTDobj.block_list(ii).upper;
          plot([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(2) upper(2) upper(2) lower(2) lower(2)],'y','LineWidth',2);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          I = [(Z-Rad1) ...
              (Z-Rad2) ...
              (Z+Rad2) ...
              (Z+Rad1) ...
              (Z-Rad1)];
          J = [(Y-(H/2)) ...
              (Y+(H/2)) ...
              (Y+(H/2)) ...
              (Y-(H/2)) ...
              (Y-(H/2))];
          plot(I,J,'y','LineWidth',2);
          clear I J;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center
          outer_radius = FDTDobj.sphere_list(ii).outer_radius
          inner_radius = FDTDobj.sphere_list(ii).inner_radius
        end
      case 2
        for ii=1:length(FDTDobj.block_list)
          L = FDTDobj.block_list(ii).lower;
          U = FDTDobj.block_list(ii).upper;
          plot([lower(3) lower(3) upper(3) upper(3) lower(3)],...
            [lower(1) upper(1) upper(1) lower(1) lower(1)],'y','LineWidth',2);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          I = (Rad1*circle_i)+X;
          J = (Rad1*circle_j)+Z;
          plot(J,I,'y'); clear I J
          I = (Rad2*circle_i)+X;
          J = (Rad2*circle_j)+Z;
          plot(J,I,'y','LineWidth',2); clear I J;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center
          outer_radius = FDTDobj.sphere_list(ii).outer_radius
          inner_radius = FDTDobj.sphere_list(ii).inner_radius
        end
      case 3
        for ii=1:length(FDTDobj.block_list)
          L = FDTDobj.block_list(ii).lower;
          U = FDTDobj.block_list(ii).upper;
          plot([lower(1) lower(1) upper(1) upper(1) lower(3)],...
            [lower(2) upper(2) upper(2) lower(2) lower(2)],'y','LineWidth',2);
        end
        for ii=1:length(FDTDobj.cylinder_list)
          center = FDTDobj.cylinder_list(ii).center;
          inner_radius = FDTDobj.cylinder_list(ii).inner_radius;
          outer_radius = FDTDobj.cylinder_list(ii).outer_radius;
          height = FDTDobj.cylinder_list(ii).height;
          I = [(X-Rad1) ...
              (X-Rad2) ...
              (X+Rad2) ...
              (X+Rad1) ...
              (X-Rad1)];
          J = [(Y-(H/2)) ...
              (Y+(H/2)) ...
              (Y+(H/2)) ...
              (Y-(H/2)) ...
              (Y-(H/2))];
          plot(I,J,'y','LineWidth',2);
          clear I J;
        end
        for ii=1:length(FDTDobj.sphere_list)
          center = FDTDobj.sphere_list(ii).center
          outer_radius = FDTDobj.sphere_list(ii).outer_radius
          inner_radius = FDTDobj.sphere_list(ii).inner_radius
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
      print(gcf,'-dpng','-r300',figout);
  end
end
