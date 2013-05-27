function createEnergySnapshot(esnap, fsnap, outfile)
  % function createEnergySnapshot(esnap, fsnap, outfile)
  
  % read in data
  [header_esnap, data_esnap, ui_esnap, uj_esnap] = readPrnFile(esnap);
  [header_fsnap, data_fsnap, ui_fsnap, uj_fsnap] = readPrnFile(fsnap);
  
  % calculate epsilon*(|Ex|^2+|Ey|^2+|Ez|^2)
  Exmod = data_fsnap(:,:,1);
  Eymod = data_fsnap(:,:,4);
  Ezmod = data_fsnap(:,:,7);
  nom = (Exmod.^2+Eymod.^2+Ezmod.^2).*data_esnap(:,:);
  
  % prepare arguments for hdrsave
  % TODO: Put this into hdrsave or whatever else is the new kid on the block
  new_header = [header_esnap{1},' ',header_esnap{2},' ','epsilon*(Ex^2+Ey^2+Ez^2)'];
  new_data = [ kron(ui_esnap,ones(length(uj_esnap),1)), repmat(uj_esnap,length(ui_esnap),1), reshape(nom,[],1) ];
  
  % save into new file
  hdrsave(outfile, new_header, new_data);
end
