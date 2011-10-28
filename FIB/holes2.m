% upper case = pixels
% lower case = microns

function filename_cellarray = holes(fileBaseName,mag,dwell,beamCurrent,AllInOne,rep_vec,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type)
  % rep Repetitions - try 1.
  % mag Magnification - set value from 20 to 200000.
  % holes_X : list of X positions of the holes (in mum)
  % holes_Y : list of Y positions of the holes (in mum)
  % holes_Radius : list of radii of the holes (in mum)
  % (x=0,y=0) = center of the screen
  % x = horizontal axis, from left to right
  % y = vertical axis, from bottom to top

  filename_cellarray = {};
  if exist('beamCurrent','var')==0;beamCurrent = 1;end;

  [res, HFW] = getResolution(mag);
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
      case 5
        [dwell_vector,X,Y] = triangleHoleUp(beamCurrent,res,dwell,holes_X(i),holes_Y(i),holes_Size_X(i),holes_Size_Y(i));
      case 6
        [dwell_vector,X,Y] = triangleHoleDown(beamCurrent,res,dwell,holes_X(i),holes_Y(i),holes_Size_X(i),holes_Size_Y(i));
      otherwise
        warning('Unexpected hole type. No hole created.');
    end
    
    total_dwell_vector = [total_dwell_vector, dwell_vector];
    total_X = [total_X, X];
    total_Y = [total_Y, Y];
  end
    
  % writing
  mkdir(folder);
  if AllInOne
    dwell=[];
    x=[];
    y=[];
    for idx=1:length(R)
      dwell = [dwell, repmat(dwell_vec{idx},1,rep_vec(idx))];
      x = [x, repmat(x_vec{idx},1,rep_vec(idx))];
      y = [y, repmat(y_vec{idx},1,rep_vec(idx))];
    end
    rep=1;
    % folder = uigetdir();
    filename = [folder,filesep,prefix,'.str'];
    %~ filename = [folder,filesep,prefix,'_holeCC_r',num2str(length(profile)),'px_',datestr(now,'yyyymmdd_HHMMSS'),'.str'];
    disp(['length(x) = ',num2str(length(x))]);
    disp(['Writing to ',filename]);
    fid = fopen(filename,'w');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    if ~direction
      fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
    else
      fprintf(fid,'%i %i %i\r\n',fliplr([dwell;x;y]));
    end
    fclose(fid);
    filename_cellarray{end+1} = filename;
  else
    for idx=1:length(R)
      dwell = dwell_vec{idx};
      x = x_vec{idx};
      y = y_vec{idx};
      % folder = uigetdir();
      filename = [folder,filesep,prefix,'.idx_',num2str(idx),'.rep_',num2str(rep_vec(idx)),'.str'];
      %~ filename = [folder,filesep,prefix,'_holeCC_r',num2str(length(profile)),'px_',datestr(now,'yyyymmdd_HHMMSS'),'.str'];
      disp(['length(x) = ',num2str(length(x))]);
      disp(['Writing to ',filename]);
      fid = fopen(filename,'w');
      fprintf(fid,'s\r\n%i\r\n%i\r\n',rep_vec(idx),length(x));
      if ~direction
        fprintf(fid,'%i %i %i\r\n',[dwell;x;y]);
      else
        fprintf(fid,'%i %i %i\r\n',fliplr([dwell;x;y]));
      end
      fclose(fid);
      filename_cellarray{end+1} = filename;
    end
  end
  
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
  shiftYfirst = 2060+Sy;

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
  % size of circles in nm as a function of the beamcurrent
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
  
  %projectName='trial9';
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
  %mag=200000;
  %dwell=20000;
  rep=1;
  beamCurrent=1; %Beam current.
  
  % vertical overlap of circles as a proportion of their diameter
  overlap=0.50;
  
  % horizontal distance between circles in nm
  %trenchWidth=150;  % nm
  %trenchWidth=0;  % nm
  
  % width and height of the whole structure in mum
  %W=1.25; %mum
  %H=0.5; %mum
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % size of a circle in mum
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  %spotSize = 0.500
    
  % vertical stepping distance
  BeamStep_Y = max(round((spotSize-spotSize*overlap)/res),1);
  %'BeamStep_Y'
  %round((spotSize-spotSize*overlap)/res)
  %1
  %BeamStep_Y
  
  % horizontal stepping distance
  %BeamStep_X = round((spotSize+trenchWidth*1e-3)/res);
  BeamStep_X = BeamStep_Y;
   
  W_pxl = round(x_size/res);
  H_pxl = round(y_size/res);
  
  %xp=[1,1+BeamStep_X,1+(1+2)*BeamStep_X,1+(1+2+3)*BeamStep_X]
  Xp = 1:BeamStep_X:W_pxl;
  Yp = 1:BeamStep_Y:H_pxl;
  
  %'lengths'
  %length(xp)
  %length(yp)
  %return
  
  YpFlip = fliplr(Yp);
  onesVec = ones(1,length(Yp));
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  N = length(Xp);
  for m=1:N
    %disp(['m = ',num2str(m/N)]);
    X = [X,Xp(m)*onesVec];
    if (mod(m,2)==0)
      Y = [Y,Yp];
    else
      Y = [Y,YpFlip];
    end
  end
  
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel
  
  X = round(X+Sx-W_pxl/2);
  Y = round(Y+Sy-H_pxl/2);
  dwell_vector = dwell*ones(1,length(X));
  
  %filename = ['snake_',projectName,'_',num2str(mag),'X_dwell',num2str(dwell),'_rep',num2str(rep),'.str'];
  %disp(['Writing to ',filename]);
  %fid=fopen(filename,'w+');
  %fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
  %fprintf(fid,[num2str(dwell),' %i %i\r\n'],[x;y]);
  %fclose(fid);
  
  % clf
  %disp('Plotting lines...');
  %figure;
  %subplot(2,1,1);
  %plot(x,y,'.');
  %subplot(2,1,2);
  %plot(res*x,res*y,'.');
  
  %hold on;
  
  %disp('Plotting circles...');
  %spotR=spotSize/res/2;
  %for m=1:length(x)
    %subplot(2,1,1)
    %rectangle('Position',[x(m)-spotR,y(m)-spotR,spotSize/res,spotSize/res],'Curvature',[1,1])
    %subplot(2,1,2)
    %rectangle('Position',res*[x(m)-spotR,y(m)-spotR,spotSize/res,spotSize/res],'Curvature',[1,1])
  %end
end

function [dwell_vector,X,Y] = triangleHoleLeft(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  % size of circles in nm as a function of the beamcurrent
  spotSizes = [1 8;
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
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  rep=1;
  beamCurrent=1; %Beam current.
  % vertical overlap of circles as a proportion of their diameter
  overlap=0.50;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % size of a circle in mum
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  
  % vertical stepping distance
  BeamStep_Y = max(round((spotSize-spotSize*overlap)/res),1);
  % horizontal stepping distance
  BeamStep_X = BeamStep_Y;
  
  W_pxl = round(x_size/res);
  H_pxl = round(y_size/res);
  
  Yp = 1:BeamStep_Y:H_pxl;
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  for m = 1:length(Yp);
    L_pxl = W_pxl - abs(Yp(m)-0.5*H_pxl)*(2*W_pxl/H_pxl);
    Xp = -L_pxl:BeamStep_X:-1;
    if (mod(m,2)==0)
      X = [X, Xp];
    else
      X = [X, fliplr(Xp)];
    end
    Y = [Y, Yp(m)*ones(1,length(Xp))];
  end
  
  % place at desired position
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel
  
  X = round(X+Sx);
  Y = round(Y+Sy-H_pxl/2);
  dwell_vector = dwell*ones(1,length(X));
end

function [dwell_vector,X,Y] = triangleHoleRight(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  % size of circles in nm as a function of the beamcurrent
  spotSizes = [1 8;
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
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  rep=1;
  beamCurrent=1; %Beam current.
  % vertical overlap of circles as a proportion of their diameter
  overlap=0.50;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % size of a circle in mum
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  
  % vertical stepping distance
  BeamStep_Y = max(round((spotSize-spotSize*overlap)/res),1);
  % horizontal stepping distance
  BeamStep_X = BeamStep_Y;
  
  W_pxl = round(x_size/res);
  H_pxl = round(y_size/res);
  
  Yp = 1:BeamStep_Y:H_pxl;
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  for m = 1:length(Yp);
    L_pxl = W_pxl - abs(Yp(m)-0.5*H_pxl)*(2*W_pxl/H_pxl);
    Xp = 1:BeamStep_X:L_pxl;
    if (mod(m,2)==0)
      X = [X, Xp];
    else
      X = [X, fliplr(Xp)];
    end
    Y = [Y, Yp(m)*ones(1,length(Xp))];
  end
  
  % place at desired position
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel
  
  X = round(X+Sx);
  Y = round(Y+Sy-H_pxl/2);
  dwell_vector = dwell*ones(1,length(X));
end

function [dwell_vector,X,Y] = triangleHoleUp(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  % size of circles in nm as a function of the beamcurrent
  spotSizes = [1 8;
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
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  rep=1;
  beamCurrent=1; %Beam current.
  % vertical overlap of circles as a proportion of their diameter
  overlap=0.50;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % size of a circle in mum
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  
  % vertical stepping distance
  BeamStep_Y = max(round((spotSize-spotSize*overlap)/res),1);
  % horizontal stepping distance
  BeamStep_X = BeamStep_Y;
  
  W_pxl = round(x_size/res);
  H_pxl = round(y_size/res);
  
  Xp = 1:BeamStep_X:W_pxl;
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  for m = 1:length(Xp);
    L_pxl = H_pxl - abs(Xp(m)-0.5*W_pxl)*(2*H_pxl/W_pxl);
    Yp = 1:BeamStep_Y:L_pxl;
    if (mod(m,2)==0)
      Y = [Y, Yp];
    else
      Y = [Y, fliplr(Yp)];
    end
    X = [X, Xp(m)*ones(1,length(Yp))];
  end
  
  % place at desired position
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel
  
  X = round(X+Sx-W_pxl/2);
  Y = round(Y+Sy);
  dwell_vector = dwell*ones(1,length(X));
end

function [dwell_vector,X,Y] = triangleHoleDown(beamCurrent,res,dwell,x_center,y_center,x_size,y_size)
  % size of circles in nm as a function of the beamcurrent
  spotSizes = [1 8;
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
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  rep=1;
  beamCurrent=1; %Beam current.
  % vertical overlap of circles as a proportion of their diameter
  overlap=0.50;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % size of a circle in mum
  spotSize = spotSizes(find(spotSizes==beamCurrent),2)*1e-3;
  
  % vertical stepping distance
  BeamStep_Y = max(round((spotSize-spotSize*overlap)/res),1);
  % horizontal stepping distance
  BeamStep_X = BeamStep_Y;
  
  W_pxl = round(x_size/res);
  H_pxl = round(y_size/res);
  
  Xp = 1:BeamStep_X:W_pxl;
  
  dwell_vector = [];
  X = [];
  Y = [];
  
  for m = 1:length(Xp);
    L_pxl = H_pxl - abs(Xp(m)-0.5*W_pxl)*(2*H_pxl/W_pxl);
    Yp = -L_pxl:BeamStep_Y:-1;
    if (mod(m,2)==0)
      Y = [Y, Yp];
    else
      Y = [Y, fliplr(Yp)];
    end
    X = [X, Xp(m)*ones(1,length(Yp))];
  end
  
  % place at desired position
  Sx = 2048+round(x_center/res); % shift centre in pixel
  Sy = 1980+round(y_center/res); % shift centre in pixel
  
  X = round(X+Sx-W_pxl/2);
  Y = round(Y+Sy);
  dwell_vector = dwell*ones(1,length(X));
end
