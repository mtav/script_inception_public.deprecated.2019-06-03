function [lambda,Q,outFile,err,minErrInd]=doHarminv(dataFile,dt,lambdaLow,lambdaHigh)
  if ~exist('dataFile')
    [file,path] = uigetfile();
    dataFile = [path,file];
    
    dt=0.01;
    lambdaLow=0.75*get_c0();
    lambdaHigh=1.2*get_c0();
    
  else
    [path,file,ext] = fileparts(dataFile);
    file = [file,ext];
  end
  %hostname='bluecrystalp2.bris.ac.uk';
  %username='yh1714';
  %ftp1=getAvailableSSH(hostname,1,'sftp',username);
  %remoteFolder='/gpfs/cluster/cerc/yh1714/Simulations/Meep/harminvTemp/';
  %mkdir(ftp1,remoteFolder);
  
  %cd(ftp1,remoteFolder);
  %mput(ftp1,dataFile,file);
  
  %remoteFile=[remoteFolder,file];
  outfileName=[file(1:max(strfind(file,'.'))-1),'_harminv.out'];
  %remoteOutFile=[remoteFolder,outfileName];
  
  outFile=[path,filesep,outfileName];

  hcommand=['harminv -t ',num2str(dt,'%2.8e'),' ',num2str(get_c0()/lambdaHigh,'%2.8e'),'-',num2str(get_c0()/lambdaLow,'%2.8e'),' < ',dataFile,' > ',outFile]
  
  [status,result] = system(hcommand);
  %rund(ftp1,hcommand)
  %rund(hcommand)
  
  %mget(ftp1,remoteOutFile,path);
  %rm(ftp1, file)
  %rm(ftp1, remoteOutFile)
    
  if ~(exist(outFile,'file'))
    error(['ERROR: File ', outFile, ' does not exist.'])
  end

  fid = fopen(outFile,'r');
  tline = fgetl(fid);
  numCol=length(strfind(tline,','));
  str=repmat('%f, ',1,numCol);
  str=[str,'%f'];
  C = textscan(fid, str);
  fclose(fid);
  
  lambda=get_c0()./C{1};
  [lambda,k]=sort(lambda);
  Q=C{3};
  Q=Q(k);
  err=C{end};
  err=err(k);
  
  minErrInd=find(err==min(err));
end
