% upper case = pixels
% lower case = microns

function filename_cellarray = holes(fileBaseName,mag,dwell,rep,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,separate_files)
  %rep Repetitions - try 1.
  %mag Magnification - set value from 20 to 200000.
  % holes_X : list of X positions of the holes (in mum)
  % holes_Y : list of Y positions of the holes (in mum)
  % holes_Radius : list of radii of the holes (in mum)
  % (x=0,y=0) = center of the screen
  % x = horizontal axis, from left to right
  % y = vertical axis, from bottom to top

  filename_cellarray = {};
  beamCurrent = 1;

  HFW = 304000/mag; %; % Width of the horizontal scan (mum).
  res = HFW/4096; % size of each pixel (mum).
  disp(['Resolution = (304000/4096)/mag = ',num2str(res),' mum/pxl']);

  total_dwell_vector = [];
  total_X = [];
  total_Y = [];
  for i=1:length(holes_X)
    dwell_vector = []; X = []; Y = [];
    switch holes_Type(i)
      case 0
        [dwell_vector,X,Y] = spiralHoleCircular(beamCurrent,res,dwell,holes_X(i),holes_Y(i),holes_Size_X(i),holes_Size_Y(i));
      case 1
        [dwell_vector,X,Y] = spiralHoleRectangular(beamCurrent,res,dwell,holes_X(i),holes_Y(i),holes_Size_X(i),holes_Size_Y(i));
      case 2
        [dwell_vector,X,Y] = ZigZagHoleRectangular(beamCurrent,res,dwell,holes_X(i),holes_Y(i),holes_Size_X(i),holes_Size_Y(i));
      case 3
        [dwell_vector,X,Y] = triangleHoleLeft(beamCurrent,res,dwell,holes_X(i),holes_Y(i),holes_Size_X(i),holes_Size_Y(i));
      case 4
        [dwell_vector,X,Y] = triangleHoleRight(beamCurrent,res,dwell,holes_X(i),holes_Y(i),holes_Size_X(i),holes_Size_Y(i));
      otherwise
        warning('Unexpected hole type. No hole created.');
    end
    
    if separate_files == true
      % Write to file.
      [ folder, basename, ext ] = fileparts(fileBaseName);
      if strcmp(ext,'.str')
        sub_filename = fullfile(folder, [ basename, '.', num2str(i), '.str']);
      else
        sub_filename = [fileBaseName, '.', num2str(i), '.str'];
      end

      disp(['Creating ',sub_filename]);
      fid = fopen(sub_filename,'w+');
      fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(X));
      fprintf(fid,'%i %i %i\r\n',[dwell_vector;X;Y]);
      % fprintf('s\r\n%i\r\n%i\r\n',rep,length(total_X));
      % fprintf('%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
      fclose(fid);
      filename_cellarray{end+1}=sub_filename;
      % surfMask(total_X,total_Y,total_dwell_vector);
      %~ readStrFile(fileBaseName);
    end
    total_dwell_vector = [total_dwell_vector, dwell_vector];
    total_X = [total_X, X];
    total_Y = [total_Y, Y];
  end
  
  if separate_files == false
    % Write to file.
    disp(['Creating ',fileBaseName]);
    fid = fopen(fileBaseName,'w+');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(total_X));
    fprintf(fid,'%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
    % fprintf('s\r\n%i\r\n%i\r\n',rep,length(total_X));
    % fprintf('%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
    fclose(fid);
    filename_cellarray{end+1}=fileBaseName;
    
    % surfMask(total_X,total_Y,total_dwell_vector);
    
    %readStrFile({fileBaseName});
  end
  
  figure;
  plot(res*total_X(1:1:end),res*total_Y(1:1:end),'r');
  xlabel('microns');
  ylabel('microns');
  axis(res*[0 4096 0 4096]);
  
end

function [dwell_vector,X,Y] = spiralHoleCircular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  %%%%%%%%Input-PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %dwell_vector time (us) - try 800.
  %radius Width of the square (um).
  %s shift first hole centre to centre cavity = cavity length(um).

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  radius = 0.5*x_size;
  
  if (radius>4096*res/2)
     error('Feature is too big for this magnification level..');
  end

  R=radius/res; % Radius in pixels.
  % R=radius;

  Sx = round(x_center/res); % shift centre in pixel
  Sy = round(y_center/res); % shift centre in pixel
  
  numPoints = 2*pi*R^2;

  % numPoints
  t = linspace(0,2*pi*R,numPoints);

  X = round(1/(2*pi)*t.*cos(t));
  Y = round(1/(2*pi)*t.*sin(t));

  X = X-min(X)+2048-round(R);
  Y = Y-min(Y)+1980-round(R);

  c = [X',Y'];
  [mixed,k] = unique(c,'rows');
  kk = sort(k);
  coordinates = c(kk,:)';
  % lineLength(coordinates)
  X = coordinates(1,:);
  Y = coordinates(2,:);

  shiftXfirst = 2048+Sx;
  shiftYfirst = 1980+Sy;

  X = shiftXfirst+X-round((min(X)+max(X))/2);
  Y = shiftYfirst+Y-round((min(Y)+max(Y))/2);
  dwell_vector = dwell*ones(1,length(X));
end

function [dwell_vector,X,Y] = spiralHoleRectangular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  spotSizes=[1 8;
  4 12;
  11 15;
  70 25;
  150 35;
  350 55;
  1000 80;
  2700 120;
  6600 270;
  11500 500;
  ];
  
  %%%%%%%%PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  overlap = 0.25;
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  lineSep = spotSize*(2-overlap)/2;  % Seperation of consecutive spiral circles (um).
  innerToOuter = 0; % Direction of etch.
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%55
  W = round(x_size/res);  % Width in pixels.
  H = round(y_size/res);  % Heigth in pixels.
  L = round(lineSep/res);  % Line seperation in pixels.
  
  if ( L == 0 )
    L = 1;
    display('Separation too small using highest resolution')
  end
  
  xl = W + L;
  yl = H + L;
  
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel

  offsetX = Sx-round(W/2);
  offsetY = Sy-round(H/2); %TODO: Use functions/global vars to get constants like 1908 and 2048

  X = offsetX*ones(1,H);
  Y = offsetY+(H-1:-1:0);
  
  while(xl>L && yl>L)  
    %Go to right xl
    xl = xl-L;
    X = [X,(X(end)+1:X(end)+xl-1)];
    Y = [Y,Y(end)*ones(1,xl-1)];
    %Go down yl
    yl = yl-L;
    X = [X,X(end)*ones(1,yl-1)];
    Y = [Y,(Y(end)+1:Y(end)+yl-1)];
    %Go left xl - L
    xl = xl-L;
    X = [X,(X(end)-1:-1:X(end)-xl+1)];
    Y = [Y,Y(end)*ones(1,xl-1)];
    %Go up yl-L
    yl = yl-L;
    X = [X,X(end)*ones(1,yl-1)];
    Y = [Y,(Y(end)-1:-1:Y(end)-yl+1)];
    %Set xl=xl-2L yl=yl-2L
  end
  
  if (innerToOuter)
    X = fliplr(X);
    Y = fliplr(Y);
  end
  dwell_vector = repmat(dwell,size(X,1),size(X,2));
end

function [dwell_vector,X,Y] = ZigZagHoleRectangular(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  %%%%%%%%Input-PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %dwell_vector time (us) - try 800.
  %radius Width of the square (um).
  %s shift first hole centre to centre cavity = cavity length(um).

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  radius = 0.5*x_size;
  
  if (radius>4096*res/2)
     error('Feature is too big for this magnification level..');
  end

  R=radius/res; % Radius in pixels.
  % R=radius;

  Sx=round(x_center/res); % shift centre in pixel
  Sy=round(y_center/res); % shift centre in pixel

  % Sx=x_center;
  % Sy=y_center;
  
  numPoints=2*pi*R^2;
  % numPoints=100;

  % t = [];

  % numPoints
  t=linspace(0,2*pi*R,numPoints);

  X = round(1/(2*pi)*t.*cos(t));
  Y = round(1/(2*pi)*t.*sin(t));

  X=X-min(X)+2048-round(R);
  Y=Y-min(Y)+1980-round(R);

  c=[X',Y'];
  [mixed,k]=unique(c,'rows');
  kk=sort(k);
  coordinates=c(kk,:)';
  % lineLength(coordinates)
  X=coordinates(1,:);
  Y=coordinates(2,:);

  shiftXfirst=2048+Sx;
  shiftYfirst=1980+Sy;

  X = shiftXfirst+X-round((min(X)+max(X))/2);
  Y = shiftYfirst+Y-round((min(Y)+max(Y))/2);
  % length(X)
  % X

  dwell_vector = dwell*ones(1,length(X));
end

function [dwell_vector,X,Y] = triangleHoleLeft(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  %%%%%%%%Input-PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %dwell_vector time (us) - try 800.
  %radius Width of the square (um).
  %s shift first hole centre to centre cavity = cavity length(um).

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  radius = 0.5*x_size;
  if (radius>4096*res/2)
     error('Feature is too big for this magnification level..');
  end

  R=radius/res; % Radius in pixels.
  % R=radius;

  Sx=round(x_center/res); % shift centre in pixel
  Sy=round(y_center/res); % shift centre in pixel

  % Sx=x_center;
  % Sy=y_center;
  
  numPoints=2*pi*R^2;
  % numPoints=100;

  % t = [];

  % numPoints
  t=linspace(0,2*pi*R,numPoints);

  X = round(1/(2*pi)*t.*cos(t));
  Y = round(1/(2*pi)*t.*sin(t));

  X=X-min(X)+2048-round(R);
  Y=Y-min(Y)+1980-round(R);

  c=[X',Y'];
  [mixed,k]=unique(c,'rows');
  kk=sort(k);
  coordinates=c(kk,:)';
  % lineLength(coordinates)
  X=coordinates(1,:);
  Y=coordinates(2,:);

  shiftXfirst=2048+Sx;
  shiftYfirst=1980+Sy;

  X = shiftXfirst+X-round((min(X)+max(X))/2);
  Y = shiftYfirst+Y-round((min(Y)+max(Y))/2);
  % length(X)
  % X

  dwell_vector = dwell*ones(1,length(X));
end

function [dwell_vector,X,Y] = triangleHoleRight(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  %%%%%%%%Input-PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %dwell_vector time (us) - try 800.
  %radius Width of the square (um).
  %s shift first hole centre to centre cavity = cavity length(um).

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  radius = 0.5*x_size;
  if (radius>4096*res/2)
     error('Feature is too big for this magnification level..');
  end

  R=radius/res; % Radius in pixels.
  % R=radius;

  Sx=round(x_center/res); % shift centre in pixel
  Sy=round(y_center/res); % shift centre in pixel

  % Sx=x_center;
  % Sy=y_center;
  
  numPoints=2*pi*R^2;
  % numPoints=100;

  % t = [];

  % numPoints
  t=linspace(0,2*pi*R,numPoints);

  X = round(1/(2*pi)*t.*cos(t));
  Y = round(1/(2*pi)*t.*sin(t));

  X=X-min(X)+2048-round(R);
  Y=Y-min(Y)+1980-round(R);

  c=[X',Y'];
  [mixed,k]=unique(c,'rows');
  kk=sort(k);
  coordinates=c(kk,:)';
  % lineLength(coordinates)
  X=coordinates(1,:);
  Y=coordinates(2,:);

  shiftXfirst=2048+Sx;
  shiftYfirst=1980+Sy;

  X = shiftXfirst+X-round((min(X)+max(X))/2);
  Y = shiftYfirst+Y-round((min(Y)+max(Y))/2);
  % length(X)
  % X

  dwell_vector = dwell*ones(1,length(X));
end
