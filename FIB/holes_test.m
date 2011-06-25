function filename_cellarray = holes_test(fileBaseName,type)
% filename_cellarray = holes_test(fileBaseName,type)
% type = loncar,DFBrectSpiral,DFBrectRaster,DFBtriangle

  switch type
    case 'loncar'
      % loncar
      holeType_left = 0;
      holeType_center = 0;
      holeType_right = 0;
      left = 0;
      center = 1;
      right = 0;
    case 'DFBrectSpiral'
      % DFB rect spiral
      holeType_left = 1;
      holeType_center = 0;
      holeType_right = 1;
      left = 1;
      center = 0;
      right = 1;
    case 'DFBrectRaster'
      % DFB rect raster
      holeType_left = 2;
      holeType_center = 0;
      holeType_right = 2;
      left = 1;
      center = 0;
      right = 1;
    case 'DFBtriangle'
      % DFB triangles
      holeType_left = 6;
      holeType_center = 0;
      holeType_right = 5;
      left = 1;
      center = 0;
      right = 1;
    otherwise
      error('Unexpected type. No streamfile created.');
  end
  
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
  holes_Type = [];
  
  for i = 1:Nbottom
    if left
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0.5*radius_mum];
      holes_Type = [ holes_Type, holeType_left ];
    end
    if center
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0];
      holes_Type = [ holes_Type, holeType_center ];
    end
    if right
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, -0.5*radius_mum];
      holes_Type = [ holes_Type, holeType_right ];
    end
    x_current = x_current + delta_x_mum;
  end
  
  x_current = x_current + cavity_x_mum + size_x_mum;

  for i = 1:Ntop
    if left
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0.5*radius_mum];
      holes_Type = [ holes_Type, holeType_left ];
    end
    if center
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, 0];
      holes_Type = [ holes_Type, holeType_center ];
    end
    if right
      holes_X = [ holes_X, x_current];
      holes_Y = [ holes_Y, -0.5*radius_mum];
      holes_Type = [ holes_Type, holeType_right ];
    end
    x_current = x_current + delta_x_mum;
  end
  
  holes_Size_X = size_x_mum*ones(1,length(holes_X));
  holes_Size_Y = size_y_mum*ones(1,length(holes_X));
  
  separate_files = 0;
  filename_cellarray = holes(fileBaseName,mag,dwell,rep,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,separate_files);
end
