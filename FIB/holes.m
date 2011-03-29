% upper case = pixels
% lower case = microns

function res = holes(filename,mag,dwell,rep,holes_X,holes_Y,holes_Radius,separate_files)
    %rep Repetitions - try 1.
    %mag Magnification - set value from 20 to 200000.
    % holes_X : list of X positions of the holes (in mum)
    % holes_Y : list of Y positions of the holes (in mum)
    % holes_Radius : list of radii of the holes (in mum)
    % (x=0,y=0) = center of the screen
    % x = horizontal axis, from left to right
    % y = vertical axis, from bottom to top

    HFW=304000/mag; %; % Width of the horizontal scan (mum).
    res=HFW/4096; % size of each pixel (mum).
    % res=1;

    total_dwell_vector = [];
    total_X = [];
    total_Y = [];
    for i=1:length(holes_X)
        [dwell_vector,X,Y] = spiralHole(filename,res,dwell,holes_X(i),holes_Y(i),holes_Radius(i));
        if separate_files == true
          % Write to file.
          [ folder, basename, ext ] = fileparts(filename);
          if strcmp(ext,'.str')
            sub_filename = fullfile(folder, [ basename, '.', num2str(i), '.str']);
          else
            sub_filename = [filename, '.', num2str(i), '.str'];
          end

          disp(['Creating ',sub_filename]);
          fid = fopen(sub_filename,'w+');
          fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(X));
          fprintf(fid,'%i %i %i\r\n',[dwell_vector;X;Y]);
          % fprintf('s\r\n%i\r\n%i\r\n',rep,length(total_X));
          % fprintf('%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
          fclose(fid);
          
          % surfMask(total_X,total_Y,total_dwell_vector);
          %~ readStrFile(filename);
        end
        total_dwell_vector = [total_dwell_vector, dwell_vector];
        total_X = [total_X, X];
        total_Y = [total_Y, Y];
    end
    
    if separate_files == false
      % Write to file.
      disp(['Creating ',filename]);
      fid = fopen(filename,'w+');
      fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(total_X));
      fprintf(fid,'%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
      % fprintf('s\r\n%i\r\n%i\r\n',rep,length(total_X));
      % fprintf('%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
      fclose(fid);
      
      % surfMask(total_X,total_Y,total_dwell_vector);
      readStrFile(filename);
    end
    
    figure;
    plot(res*total_X(1:1:end),res*total_Y(1:1:end),'r')
    xlabel('microns');
    ylabel('microns');
    axis(res*[0 4096 0 4096]);
    
end

function [dwell_vector,X,Y] = spiralHole(filename,res,dwell,x_center,y_center,radius)
    %%%%%%%%Input-PARAMTERS%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %dwell_vector time (us) - try 800.
    %radius Width of the square (um).
    %s shift first hole centre to centre cavity = cavity length(um).

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
