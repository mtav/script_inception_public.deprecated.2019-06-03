% This function creates a stream file for a single ring hole
% folder : folder to save to
% rep : Repetitions (ex: 1,3,5 or 16)
% mag : Magnification (ex: 10000 or 20000)
% r_inner : inner radius in mum (ex: 0, 2, 2.8 or 4.2)
% r_outer : outer radius in mum (ex: 2, 2.8 or 4.2)

function holeSpiralErman_single_ring(folder,rep,mag,r_inner,r_outer)
  if exist('folder','var')==0
    folder = uigetdir(pwd(),'folder');
  end
  if ~(exist(folder,'dir'))
    error(['dir not found: ',folder]);
  end
  
  %%%%%%%%PARAMETERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
  dwell=800; % Dwell time (us).
  Step=1;  % The distance in pixels between each spiral ring.
  writeToFile=1;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  [res, HFW] = getResolution(mag);
  if (r_outer/1e3>HFW/2)
    error('Feature is too big for this magnification level..')
  end

  R_outer=r_outer/res/Step; % Radius in pixels.
  R_inner=r_inner/res/Step; % Radius in pixels.

  numPoints=2*pi*(R_outer^2-R_inner^2);

  t = [];

  t=linspace(2*R_inner*pi,2*R_outer*pi,numPoints);

  x = round(1/2/pi*t.*cos(t)*Step);
  y = round(1/2/pi*t.*sin(t)*Step);

  c=[x',y'];
  [mixed,k]=unique(c,'rows');
  kk=sort(k);
  coordinates=c(kk,:)';
  % lineLength(coordinates)
  x=coordinates(1,:);
  y=coordinates(2,:);

  x=x+2048-round((min(x)+max(x))/2);
  y=y+2048-round((min(y)+max(y))/2);

  % figure;
  % plot(x,y)
  % title([num2str(length(x)),' Points']);
  % axis tight;
  % axis equal;
  figure;
  surfMask(x,y,dwell,1)

  if writeToFile
    % Write to file.
    % folder=uigetdir();
    mkdir(folder);
    filename = [folder,filesep,'holeSp_mag',num2str(mag),'_r',num2str(r_outer),'_r',num2str(r_inner),'um.str'];
    disp(['Writing to ',filename]);
    fid=fopen(filename,'w');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    fprintf(fid,[num2str(dwell),' %i %i\r\n'],[x;y]);
    fclose(fid);
  end
end
