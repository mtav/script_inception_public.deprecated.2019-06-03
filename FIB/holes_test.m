function filename_cellarray = holes_test(fileBaseName,type,mag,dwell,beamCurrent)
% filename_cellarray = holes_test(fileBaseName,type)
% type = loncar,DFBrectSpiral,DFBrectRaster,DFBtriangle
% ex:
% a=holes_test('loncar.str','loncar');readStrFile(a);
% a=holes_test('DFBrectSpiral.str','DFBrectSpiral');readStrFile(a);
% a=holes_test('DFBrectRaster.str','DFBrectRaster');readStrFile(a);
% a=holes_test('DFBtriangle.str','DFBtriangle');readStrFile(a);
% a=holes_test('../../../loncar','loncar',30000,3*2400,11);readStrFile(a);
% a=holes_test('../../../DFBrectSpiral','DFBrectSpiral',30000,3*2400,11);readStrFile(a);
% a=holes_test('../../../DFBrectRaster','DFBrectRaster',30000,3*2400,11);readStrFile(a);
% a=holes_test('../../../DFBtriangle','DFBtriangle',30000,3*2400,11);readStrFile(a);

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
  
  if exist('mag','var')==0;mag = 34000;end;
  if exist('dwell','var')==0;dwell = 3*2400;end; %unit: 0.1us
  rep = 2;
  Ntop = 10;%8;
  Nbottom = 20;%18;%40;
  size_x_mum = 2*0.066;
  size_y_mum = 0.200;
  delta_x_mum = size_x_mum + 2*0.078;
  cavity_x_mum = 2*0.145;
  radius_mum = 1;%0.500;%0.450+0.065;
  
  height_mum = 9
  Nsug = (height_mum - cavity_x_mum )/delta_x_mum
  Ntopsug = 1/3*(height_mum - cavity_x_mum )/delta_x_mum
  Nbottomsug = 2/3*(height_mum - cavity_x_mum )/delta_x_mum
  
  height_mum = Nbottom*delta_x_mum + cavity_x_mum + Ntop*delta_x_mum;
  
  [res, HFW] = getResolution(mag);
  disp(['height_mum = ',num2str(height_mum)]);
  disp(['HFW = ',num2str(HFW)]);
  
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

  % TODO: Finally create a function for this kind of stuff
  [ folder, basename, ext ] = fileparts(fileBaseName);
  if strcmp(ext,'.str')
        fileBaseName2 = fullfile(folder, basename);
  else
        fileBaseName2 = fileBaseName;
  end
  fileBaseName3 = [fileBaseName2,'.mag_',num2str(mag),'.dwell_',num2str(dwell),'.beamCurrent_',num2str(beamCurrent),'.radius_',num2str(radius_mum),'.Nbottom_',num2str(Nbottom),'.Ntop_',num2str(Ntop),'.rep_',num2str(rep)];
  filename_cellarray = holes(fileBaseName3,mag,dwell,rep,holes_X,holes_Y,holes_Size_X,holes_Size_Y,holes_Type,separate_files);
end
