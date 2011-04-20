function saveProbeImage(DIR)
  DIR
  cd(DIR);
  close all;
  [ folder, basename, ext ] = fileparts(DIR);
  plotProbe('p005id.prn',3,0,['~/Labortablo/Qplot/',basename, ext,'.png']);
end

