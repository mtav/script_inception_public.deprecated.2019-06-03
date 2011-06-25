function filename_cellarray = holes_test()

  holeType = 2;
  left = 1;
  center = 0;
  right = 1;
  fileBaseName = 'tmp.str';
  
  mag = 30000;
  dwell = 2400; %unit: 0.1us
  rep = 1;
  Ntop = 20;
  Nbottom = 40;
  size_x_mum = 0.066;
  size_y_mum = 0.200;
  delta_x_mum = size_x_mum + 0.078;
  cavity_x_mum = 0.145;
  radius_mum = 0.500;
  height_mum = Nbottom*delta_x_mum + cavity_x_mum + Ntop*delta_x_mum;
  
  [res, HFW] = getResolution(mag);
  if height_mum>HFW
    height_mum
    HFW
    error('pillar too big for this magnification');
  end
  
  x_current = -0.5*height_mum;
  holes_X = [];
  holes_Y = [];
  
  for i = 1:Nbottom
    if left
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0.5*radius_mum];
    end
    if center
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0];
    end
    if right
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, -0.5*radius_mum];
    end
    x_current = x_current + delta_x_mum;
  end
  
  x_current = x_current + cavity_x_mum + size_x_mum;

  for i = 1:Ntop
    if left
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0.5*radius_mum];
    end
    if center
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0];
    end
    if right
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, -0.5*radius_mum];
    end
    x_current = x_current + delta_x_mum;
  end
  
  holes_Size_X = size_x_mum*ones(1,length(holes_X));
  holes_Size_Y = size_y_mum*ones(1,length(holes_X));
  
  holes_Type = holeType*ones(1,length(holes_X));
  separate_files = 0;
  filename_cellarray = holes(fileBaseName,mag,dwell,rep,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,separate_files);
end
