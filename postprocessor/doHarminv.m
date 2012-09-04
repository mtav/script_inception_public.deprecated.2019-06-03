% TODO: Document and use a sane order. This should be a simple wrapper for harminv, with same input/output order, nothing more. (will require changes to all occurences of doHarminv elsewhere)
function [ status, lambda, Q, outFile, err, minErrInd, frequency, decay_constant, amplitude, phase ] = doHarminv(dataFile,dt,lambdaLow,lambdaHigh)

  if ( exist('dataFile','var')==0 ) | ( exist(dataFile, 'file')==0 )
    warning('No file specified or found.');
    [fileBasenameWithExtension,path] = uigetfile();
    dataFile = [path,fileBasenameWithExtension];
  else
    [path,fileBasenameWithoutExtension,ext] = fileparts(dataFile);
    fileBasenameWithExtension = [fileBasenameWithoutExtension,ext];
  end

  if exist('dt','var')==0; dt=0.01; end
  if exist('lambdaLow','var')==0; lambdaLow=0.75*get_c0(); end
  if exist('lambdaHigh','var')==0; lambdaHigh=1.2*get_c0(); end
    
  %hostname='bluecrystalp2.bris.ac.uk';
  %username='yh1714';
  %ftp1=getAvailableSSH(hostname,1,'sftp',username);
  %remoteFolder='/gpfs/cluster/cerc/yh1714/Simulations/Meep/harminvTemp/';
  %mkdir(ftp1,remoteFolder);
  
  %cd(ftp1,remoteFolder);
  %mput(ftp1,dataFile,fileBasenameWithExtension);
  
  %remoteFile=[remoteFolder,fileBasenameWithExtension];
  %outfileName = [fileBasenameWithExtension(1:max(strfind(fileBasenameWithExtension,'.'))-1),'_harminv.out'];
  outfileName = [fileBasenameWithoutExtension,'.out'];
  %remoteOutFile=[remoteFolder,outfileName];
  
  outFile = [path,filesep,outfileName];

  hcommand = ['harminv -t ',num2str(dt,'%2.8e'),' ',num2str(get_c0()/lambdaHigh,'%2.8e'),'-',num2str(get_c0()/lambdaLow,'%2.8e'),' < ',dataFile,' > ',outFile];

  fid = fopen([path,filesep,fileBasenameWithoutExtension,'.command'],'w');
  fprintf(fid,[hcommand,'\r\n']);
  fclose(fid);
 
  [status,result] = system(hcommand);
  if (status == 0)
    %rund(ftp1,hcommand)
    %rund(hcommand)
    
    %mget(ftp1,remoteOutFile,path);
    %rm(ftp1, fileBasenameWithExtension)
    %rm(ftp1, remoteOutFile)
      
    if ~(exist(outFile,'file'))
      error(['ERROR: File ', outFile, ' does not exist.'])
    end
  
    % read contents of file into "C"
    fid = fopen(outFile,'r');
    tline = fgetl(fid);
    numCol = length(strfind(tline,','));
    str = repmat('%f, ',1,numCol);
    str = [str,'%f'];
    C = textscan(fid, str);
    fclose(fid);

    % fill output variables    
    frequency = C{1};
    decay_constant = C{2};
    Q = C{3};
    amplitude = C{4};
    phase = C{5};
    err = C{6};
    lambda = get_c0()./C{1};
    
    % sort everything by lambda
    [lambda,k] = sort(lambda);

    frequency = frequency(k);
    decay_constant = decay_constant(k);
    Q = Q(k);
    amplitude = amplitude(k);
    phase = phase(k);
    err = err(k);

    
    minErrInd = find(err==min(err));
  else
    lambda = -1;
    Q = -1;
    outFile = -1;
    err = -1;
    minErrInd = -1;
    warning('Failed to execute command:');
    hcommand
    disp(result);
  end
end
