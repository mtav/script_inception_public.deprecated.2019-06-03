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
  
  %% Load geo file data
  Geoparms = geometryparms(handles);
  
  %% Load input file data
  Inpparms = inputparms(handles);
  
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
  if get(handles.checkbox_modulus,'Value') == 1
      data = abs(handles.fin1(:,column));
  else
      data = handles.fin1(:,column);
      if min(data) < 0
          modu = 0;
      end
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
  figure
  grey = 0;
  if (get(handles.radiobutton_colour,'Value') > get(handles.radiobutton_greyscale,'Value'))
      colormap(jet(256));
      grey = 0;
  else
      colormap(gray(256));
      grey = 1;
  end
  
  if handles.plane == 1
      if (get(handles.radiobutton_surface,'Value') > get(handles.radiobutton_contour,'Value')) 
          %pcolor(i,j,k)
          surf(i,j,k)
      else
          contour(i,j,k)
      end
  elseif handles.plane == 2
      if (get(handles.radiobutton_surface,'Value') > get(handles.radiobutton_contour,'Value')) 
          %pcolor(i,j,k)
          surf(i,j,k)
      else
          contour(i,j,k)
      end
  else
      if (get(handles.radiobutton_surface,'Value') > get(handles.radiobutton_contour,'Value')) 
          %pcolor(j,i,k)
          surf(j,i,k)
      else
          j
          i
          k
          contour(j,i,k)
      end
  end
  
  %colave = max(fin1(:,column));
  colfig = handles.colplot{column};
  if modu == 1 || get(handles.checkbox_modulus,'Value') == 1
      disp(['maxval=',num2str(maxval)]);
      caxis([0 maxval])
  else
      caxis([-maxval maxval])
  end
  colorbar
  AspectRatio = get(gca,'DataAspectRatio');
  AspectRatio(1) = AspectRatio(2);
  set(gca,'DataAspectRatio',AspectRatio);
  if get(handles.checkbox_interpolate,'Value') == 1
      shading interp
  else
      shading flat
  end
  switch handles.plane
      case 1
          xlabel('z')
          ylabel('y')
          axis([Geoparms.Box.Zl Geoparms.Box.Zu Geoparms.Box.Yl Geoparms.Box.Yu])
      case 2
          xlabel('z')
          ylabel('x')
          axis([Geoparms.Box.Zl Geoparms.Box.Zu Geoparms.Box.Xl Geoparms.Box.Xu])
      case 3
          xlabel('x')
          ylabel('y')
          axis([Geoparms.Box.Xl Geoparms.Box.Xu Geoparms.Box.Yl Geoparms.Box.Yu])
  end
  titlesnap = strread(handles.snapfile,'%s','delimiter','\\');
  title([char(titlesnap(length(titlesnap))) ': ' char(handles.colplot(column))],'FontWeight','bold');
  clear titlesnap
  hold on
  
  %% Plot Geometry Entities
  if get(handles.checkbox_geometry,'Value') == 1
      disp('DRAWING GEOMETRY')
      switch handles.plane
          case 1
              %Blocks
              if Geoparms.Blks > 0
                  for ii=1:1:length(Geoparms.Block)
                      plot([Geoparms.Block(1,ii).Zl Geoparms.Block(1,ii).Zl Geoparms.Block(1,ii).Zu Geoparms.Block(1,ii).Zu Geoparms.Block(1,ii).Zl],...
                      [Geoparms.Block(1,ii).Yl Geoparms.Block(1,ii).Yu Geoparms.Block(1,ii).Yu Geoparms.Block(1,ii).Yl Geoparms.Block(1,ii).Yl],'y','LineWidth',2);
                  end
              end
              if Geoparms.Cyls > 0
                  for ii=1:1:length(Geoparms.Cylinder)
                      I = [(Geoparms.Cylinder(1,ii).Z-Geoparms.Cylinder(1,ii).Rad1) ...
                          (Geoparms.Cylinder(1,ii).Z-Geoparms.Cylinder(1,ii).Rad2) ...
                          (Geoparms.Cylinder(1,ii).Z+Geoparms.Cylinder(1,ii).Rad2) ...
                          (Geoparms.Cylinder(1,ii).Z+Geoparms.Cylinder(1,ii).Rad1) ...
                          (Geoparms.Cylinder(1,ii).Z-Geoparms.Cylinder(1,ii).Rad1)];
                      J = [(Geoparms.Cylinder(1,ii).Y-(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y+(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y+(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y-(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y-(Geoparms.Cylinder(1,ii).H/2))];
                      plot(I,J,'y','LineWidth',2);
                      clear I J
                  end
              end
          case 2
              %Blocks
              if Geoparms.Blks > 0
                  for ii=1:1:length(Geoparms.Block)
                      plot([Geoparms.Block(1,ii).Zl Geoparms.Block(1,ii).Zl Geoparms.Block(1,ii).Zu Geoparms.Block(1,ii).Zu Geoparms.Block(1,ii).Zl],...
                     [Geoparms.Block(1,ii).Xl Geoparms.Block(1,ii).Xu Geoparms.Block(1,ii).Xu Geoparms.Block(1,ii).Xl Geoparms.Block(1,ii).Xl],'y','LineWidth',2);
                  end
              end
              if Geoparms.Cyls > 0
                  t = 0:0.1:((2*pi)+0.1);
                  circle_i = cos(t);
                  circle_j = sin(t);
                  for ii=1:1:length(Geoparms.Cylinder)
                      I = (Geoparms.Cylinder(1,ii).Rad1*circle_i)+Geoparms.Cylinder(1,ii).X;
                      J = (Geoparms.Cylinder(1,ii).Rad1*circle_j)+Geoparms.Cylinder(1,ii).Z;
                      plot(J,I,'y'); clear I J
                      I = (Geoparms.Cylinder(1,ii).Rad2*circle_i)+Geoparms.Cylinder(1,ii).X;
                      J = (Geoparms.Cylinder(1,ii).Rad2*circle_j)+Geoparms.Cylinder(1,ii).Z;
                      plot(J,I,'y','LineWidth',2); clear I J
                  end
              end
          case 3
              %Blocks
              if Geoparms.Blks > 0
                  for ii=1:1:length(Geoparms.Block)
                      plot([Geoparms.Block(1,ii).Xl Geoparms.Block(1,ii).Xl Geoparms.Block(1,ii).Xu Geoparms.Block(1,ii).Xu Geoparms.Block(1,ii).Zl],...
                     [Geoparms.Block(1,ii).Yl Geoparms.Block(1,ii).Yu Geoparms.Block(1,ii).Yu Geoparms.Block(1,ii).Yl Geoparms.Block(1,ii).Yl],'y','LineWidth',2);
                  end
              end
              if Geoparms.Cyls > 0
                  for ii=1:1:length(Geoparms.Cylinder)
                      I = [(Geoparms.Cylinder(1,ii).X-Geoparms.Cylinder(1,ii).Rad1) ...
                          (Geoparms.Cylinder(1,ii).X-Geoparms.Cylinder(1,ii).Rad2) ...
                          (Geoparms.Cylinder(1,ii).X+Geoparms.Cylinder(1,ii).Rad2) ...
                          (Geoparms.Cylinder(1,ii).X+Geoparms.Cylinder(1,ii).Rad1) ...
                          (Geoparms.Cylinder(1,ii).X-Geoparms.Cylinder(1,ii).Rad1)];
                      J = [(Geoparms.Cylinder(1,ii).Y-(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y+(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y+(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y-(Geoparms.Cylinder(1,ii).H/2)) ...
                          (Geoparms.Cylinder(1,ii).Y-(Geoparms.Cylinder(1,ii).H/2))];
                      plot(I,J,'y','LineWidth',2);
                      clear I J
                  end
              end
      end
  end
  
  if get(handles.checkbox_autosave,'Value') == 1
      dim = length(handles.snapfile);
      if grey == 1
          figout = [handles.snapfile(1:(dim-4)) '_' colfig '_' num2str(maxval) '_grey.png'];
      else
          figout = [handles.snapfile(1:(dim-4)) '_' colfig '_' num2str(maxval) '.png'];
      end
      print(gcf,'-dpng','-r300',figout)
  end
end
