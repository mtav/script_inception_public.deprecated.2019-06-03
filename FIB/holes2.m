% upper case = pixels
% lower case = microns

function filename_cellarray = holes2(fileBaseName,mag,dwell,rep_vec,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,beamCurrent,separate_files)
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
    
    total_dwell_vector = [total_dwell_vector, dwell_vector];
    total_X = [total_X, X];
    total_Y = [total_Y, Y];
  end
    
  % writing
  mkdir(folder);
  if separate_files
    dwell=[];
    x=[];
    y=[];
    for idx=1:length(R)
      dwell = [dwell, repmat(dwell_vec{idx},1,rep_vec(idx))];
      x = [x, repmat(x_vec{idx},1,rep_vec(idx))];
      y = [y, repmat(y_vec{idx},1,rep_vec(idx))];
    end
    rep=1;
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
