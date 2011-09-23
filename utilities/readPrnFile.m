function [header,data,ux,uy]=readPrnFile(filename)
  % function [header,data,ux,uy]=readPrnFile(filename)
  % header = first line
  % data = rest of file
  % if ux and uy are asked for, it will create a 3D plot of col(3) vs ( col(1), col(2) )
  
  if (nargin==0)
    [FileName,PathName] = uigetfile({'*.prn *.dat'},'Select the prn-file',getenv('DATADIR'));
    filename=[PathName,filesep,FileName];
  end
  
  disp(['Opening: ',filename,' from ',pwd()]);
  %class filename
  %filename
  [fid, message] = fopen(filename,'r');
  if fid == -1
    error(message);
  end
  
  %try
    dummy = fgets(fid);
    words = regexp(dummy,'(?<word>\w+)\s*|\s*(?<word>\w+)','tokens');
    ncols = size(words,2);
    
    for m=1:ncols
      %char(words{m})
      header{m} = char(words{m});
    end
    
    M=fscanf(fid,'%e');
    fclose(fid);
    
    data=reshape(M,ncols,length(M)/ncols);
    data=data';
    
    ux=[];
    uy=[];
    if nargout>3 && not(strcmp(header{1},'Time'))
      x=data(:,1);
      y=data(:,2);
      ux=unique(x);
      nx=length(ux);
      ny=length(x)/nx;
      uy=y(1:ny);
      for m=3:size(data,2)
        Data(:,:,m-2)=reshape(data(:,m),ny,nx);
      end
      data=Data;
      imagesc(ux,uy,Data(:,:,1));
      xlabel(header(1));
      ylabel(header(2));
    end
  %catch
    %error('FATAL ERROR: Could not read .prn file correctly.');
    %header=[];
    %data=[];
  %end
  
  % figure
  % plot(data(:,1),data(:,2:end));
end
