function createEnergySnapshot(esnap, fsnap, outfile)
  % function createEnergySnapshot(esnap, fsnap, outfile)
  
  % read in data
  [header_esnap,data_esnap] = readPrnFile(esnap);
  [header_fsnap,data_fsnap] = readPrnFile(fsnap);

  % prepare arguments for hdrsave
  new_header = [header_esnap{1},' ',header_esnap{2},' ','epsilon*(Ex^2+Ey^2+Ez^2)'];
  new_data = [data_esnap(:,1),data_esnap(:,2),data_esnap(:,3).*(data_fsnap(:,3).^2+data_fsnap(:,6).^2+data_fsnap(:,9).^2)];
  
  % write energy snapshot to outfile
  hdrsave(outfile, new_header, new_data);
end
