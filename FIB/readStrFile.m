% This function reads and plots a mask file (.str)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
%       ERMAN ENGIN
%       UNIVERSSITY OF BRISTOL
% 
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [x,y,dwell,rep,numPoints]=readStrFile(filename_cellarray)
  
  if (nargin==0)
    [FileName,PathName,FilterIndex] = uigetfile('*.str','',pwd());
    filename=[PathName,filesep,FileName];
    filename_cellarray = {filename};
  end

  figure;
  hold on;
  for idx=1:length(filename_cellarray)
    % default values
    x=[];y=[];dwell=[];rep=0;numPoints=0;
    
    filename = char(filename_cellarray(idx));
    disp(['processing : ',filename]);

    try
      fid=fopen(filename);
      dummy=fgets(fid);
      rep=str2num(fgets(fid));
      numPoints=str2num(fgets(fid));
      M=fscanf(fid,'%f %f %f',[3 inf]);
      fclose(fid);
    catch
      disp(['Error opening file ', filename]);
      fclose(fid);
    end

    if size(M,1)<3
      disp('WARNING: Empty streamfile');
    else
      dwell=M(1,:);
      x=M(2,:);
      y=M(3,:);
    end
    plot(x(1:1:end),y(1:1:end),'r-');
    plot(x(1:1:end),y(1:1:end),'b.');

    sec = rep*(sum(dwell)*1e-7+0.008163229517396*numPoints);
    hour   = fix(sec/3600);      % get number of hours
    sec    = sec - 3600*hour;    % remove the hours
    minute = fix(sec/60);        % get number of minutes
    sec    = sec - 60*minute;    % remove the minutes
    second = sec;
    disp(sprintf('Approximate Mask Duration is %2.5f hours %2.5f minutes %2.5f seconds',hour,minute,second));

    if (nargin==0)
    %     scatter(x,y)
    % plot(x,y)
        set(gca,'YDir','reverse');
        title([num2str(length(x)),' Points']);
    %     
    %     spotR=1;
    %     for m=1:min(55500,length(x))
    %     % for m=1:length(x)
    %     rectangle('Position',[x(m)-spotR,y(m)-spotR,2*spotR,2*spotR],'Curvature',[1,1])
    %     end
    %     axis equal
    end

    % A=zeros(4094,4096);

    % for m=1:length(x)
    %   A(x(m),y(m))=dwell(m);
    % end
    % B=autoCrop(A);
    % surf(B);
    % imagesc(A)
    % imagesc(B)

  end

  xlabel('pixels');
  ylabel('pixels');
  axis([0 4096 0 4096]);
  pbaspect([1,1,1]);

end
