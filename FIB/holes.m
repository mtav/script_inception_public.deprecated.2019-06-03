% upper case = pixels
% lower case = microns

function filename_cellarray = holes(fileBaseName,mag,dwell,rep,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,separate_files,beamCurrent)
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
  disp(['Resolution = ',num2str(res),' mum/pxl']);

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
    [ folder, basename, ext ] = fileparts(fileBaseName);
    if strcmp(ext,'.str')
        filename = fullfile(folder, [ basename, '.str']);
    else
        filename = [fileBaseName, '.str'];
    end
    disp(['Creating ',filename]);
    fid = fopen(filename,'w+');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(total_X));
    fprintf(fid,'%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
    % fprintf('s\r\n%i\r\n%i\r\n',rep,length(total_X));
    % fprintf('%i %i %i\r\n',[total_dwell_vector;total_X;total_Y]);
    fclose(fid);
    filename_cellarray{end+1}=filename;
    
    % surfMask(total_X,total_Y,total_dwell_vector);
    
    %readStrFile({fileBaseName});
  end
  
  %figure;
  %plot(res*total_X(1:1:end),res*total_Y(1:1:end),'r');
  %xlabel('microns');
  %ylabel('microns');
  %axis(res*[0 4096 0 4096]);
  
end
