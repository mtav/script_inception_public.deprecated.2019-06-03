function hdrsave(filename,header,data)
  % function hdrsave(filename,header,data)

  % write header
  file = fopen(filename,'w');
  % fprintf(file,'%s\r\n',header);
  fprintf(file,[header,'\r\n']);
  fclose(file);

  % write data
  save(filename, 'data', '-ascii', '-double', '-tabs', '-append')

  % TODO: Maybe improve this function so it can take header and data in the various other formats. (or settle on one best one)
  % Left in for reference:

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %% read in data
  %[header_esnap,data_esnap] = readPrnFile(esnap);
  %[header_fsnap,data_fsnap] = readPrnFile(fsnap);

  %% prepare arguments for hdrsave
  %new_header = [header_esnap{1},' ',header_esnap{2},' ','epsilon*(Ex^2+Ey^2+Ez^2)'];
  %new_data = [data_esnap(:,1),data_esnap(:,2),data_esnap(:,3).*(data_fsnap(:,3).^2+data_fsnap(:,6).^2+data_fsnap(:,9).^2)];
  
  %% write energy snapshot to outfile
  %hdrsave(outfile, new_header, new_data);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %% read in data
  %[header_esnap, data_esnap, ui_esnap, uj_esnap] = readPrnFile(esnap);
  %[header_fsnap, data_fsnap, ui_fsnap, uj_fsnap] = readPrnFile(fsnap);
  
  %% calculate epsilon*(|Ex|^2+|Ey|^2+|Ez|^2)
  %Exmod = data_fsnap(:,:,1);
  %Eymod = data_fsnap(:,:,4);
  %Ezmod = data_fsnap(:,:,7);
  %nom = data_esnap(:,:).*(Exmod.^2+Eymod.^2+Ezmod.^2);
  
  %% prepare arguments for hdrsave
  %% TODO: Put this into hdrsave or whatever else is the new kid on the block
  %new_header = [header_esnap{1},' ',header_esnap{2},' ','epsilon*(Ex^2+Ey^2+Ez^2)'];
  %new_data = [ kron(ui_esnap,ones(length(uj_esnap),1)), repmat(uj_esnap,length(ui_esnap),1), reshape(nom,[],1) ];

  %% write energy snapshot to outfile
  %hdrsave(outfile, new_header, new_data);

end
