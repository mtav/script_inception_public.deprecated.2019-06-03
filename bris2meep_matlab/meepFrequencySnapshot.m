% Format example:
%(set! snapshots
  %(list
    %(make snapshot	
      %(name "snapshot-1")
      %(center 0 0 0)
      %(size (- sx (* 2 dpml)) (- sy (* 2 dpml)) 0)
      %(wavelength 0.600)
      %(components Ex Ey Ez Hx Hy Hz)
      %(res resolution)
    %)
    %(make snapshot	
      %(name "snapshot-1")
      %(center 0 0 0)
      %(size (- sx (* 2 dpml)) (- sy (* 2 dpml)) 0)
      %(wavelength 0.600)
      %(components Ex Ey Ez Hx Hy Hz)
      %(res resolution)
    %)
  %)
%)
function ret = meepFrequencySnapshot(name,center_vec3,size_vec3,wavelength_mum,components_vec9,resolution)
  ret = ['    (make snapshot\n'];
  ret = [ret, '      (name "',name,'")\n'];
  ret = [ret, '      (center ',num2str(center_vec3,'%4.9g '),')\n'];
  ret = [ret, '      (size ',num2str(size_vec3,'%4.9g '),')\n'];
  ret = [ret, '      (wavelength ',num2str(wavelength_mum),')\n'];
  
  components_cell_array = {};
  if (components_vec9(1) == 1); components_cell_array{end+1} = 'Ex';end;
  if (components_vec9(2) == 1); components_cell_array{end+1} = 'Ey';end;
  if (components_vec9(3) == 1); components_cell_array{end+1} = 'Ez';end;
  if (components_vec9(4) == 1); components_cell_array{end+1} = 'Hx';end;
  if (components_vec9(5) == 1); components_cell_array{end+1} = 'Hy';end;
  if (components_vec9(6) == 1); components_cell_array{end+1} = 'Hz';end;
  if (components_vec9(7) == 1); components_cell_array{end+1} = 'Jx';end;
  if (components_vec9(8) == 1); components_cell_array{end+1} = 'Jy';end;
  if (components_vec9(9) == 1); components_cell_array{end+1} = 'Jz';end;
  
  %components_string = '';
  %if (components_vec9(1) == 1); components_string = [components_string, 'Ex'];end;
  %if (components_vec9(2) == 1); components_string = [components_string, 'Ey'];end;
  %if (components_vec9(3) == 1); components_string = [components_string, 'Ez'];end;
  %if (components_vec9(4) == 1); components_string = [components_string, 'Hx'];end;
  %if (components_vec9(5) == 1); components_string = [components_string, 'Hy'];end;
  %if (components_vec9(6) == 1); components_string = [components_string, 'Hz'];end;
  
  components_string = '';
  for i=1:length(components_cell_array)
    if (i==1)
      components_string = components_cell_array{i};
    else
      components_string = [components_string,' ',components_cell_array{i}];
    end
  end
  
  %caAddRemDirs{end+1} = strStartDir;

  ret = [ret, '      (components ',components_string,')\n'];
  ret = [ret, '      (res ',num2str(resolution),')\n'];
  ret = [ret, '    )\n'];
end
