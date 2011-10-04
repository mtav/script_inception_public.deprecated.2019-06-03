function efficiency = calculateEfficiency(inputFileList)
  efficiency = 0;
  
  PrnFileNameList_xp = findPrnByName(inputFileList,'Box frequency snapshot X+');
  PrnFileNameList_yp = findPrnByName(inputFileList,'Box frequency snapshot Y+');
  PrnFileNameList_zp = findPrnByName(inputFileList,'Box frequency snapshot Z+');
  PrnFileNameList_xm = findPrnByName(inputFileList,'Box frequency snapshot X-');
  PrnFileNameList_ym = findPrnByName(inputFileList,'Box frequency snapshot Y-');
  PrnFileNameList_zm = findPrnByName(inputFileList,'Box frequency snapshot Z-');


end
