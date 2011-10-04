function PrnFileNameList = findPrnByName(inputFileList,name)
  PrnFileNameList = {};
  [entries,FDTDobj] = GEO_INP_reader(inputFileList);
  for numID = 1:length(FDTDobj.probe_list)
    if strcmp(name, FDTDobj.probe_list(numID).name)
      snap_plane = 'p';
      probe_ident = FDTDobj.flag.id;
      [ filename, alphaID, pair ] = numID_to_alphaID(numID, snap_plane, probe_ident);
      num = sprintf('%03d',numID);
      filename = strcat({snap_plane}, num, {probe_ident}, '.prn');
      filename = char(filename);
      PrnFileNameList{end+1} = filename;
    end
  end

end
