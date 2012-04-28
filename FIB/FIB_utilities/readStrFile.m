%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
%       ERMAN ENGIN
%       UNIVERSSITY OF BRISTOL
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This function reads and plots a mask file (.str)
% Usage:
% function [x,y,dwell,rep,numPoints] = readStrFile(filename_cellarray, magnitude)
% magnitude is optional. If given a second plot in mum will be created.

function [x,y,dwell,rep,numPoints] = readStrFile(filename_cellarray, magnitude)
  
  if (nargin==0)
    [FileName,PathName,FilterIndex] = uigetfile('*.str','',pwd());
    filename=[PathName,filesep,FileName];
    filename_cellarray = {filename};
  end

  if exist('magnitude','var')==1
    [res, HFW] = getResolution(magnitude);
  end

  figure;
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


    if exist('magnitude','var')==1
      subplot(1,2,1);
      plot(x(1:1:end),y(1:1:end),'r-'); hold on;
      plot(x(1:1:end),y(1:1:end),'b.');
      subplot(1,2,2);
      plot(res*x(1:1:end),res*y(1:1:end),'r-'); hold on;
      plot(res*x(1:1:end),res*y(1:1:end),'b.');
    else
      plot(x(1:1:end),y(1:1:end),'r-'); hold on;
      plot(x(1:1:end),y(1:1:end),'b.');
    end

    % calculate approximate mask duration
    sec = rep*(sum(dwell)*1e-7+0.008163229517396*numPoints);
    hour   = fix(sec/3600);      % get number of hours
    sec    = sec - 3600*hour;    % remove the hours
    minute = fix(sec/60);        % get number of minutes
    sec    = sec - 60*minute;    % remove the minutes
    second = sec;
    disp(sprintf('Approximate Mask Duration is %2.5f hours %2.5f minutes %2.5f seconds',hour,minute,second));

    %if (nargin==0)
    %%     scatter(x,y)
    %% plot(x,y)
        %set(gca,'YDir','reverse');
        %title([num2str(length(x)),' Points']);
    %%     
    %%     spotR=1;
    %%     for m=1:min(55500,length(x))
    %%     % for m=1:length(x)
    %%     rectangle('Position',[x(m)-spotR,y(m)-spotR,2*spotR,2*spotR],'Curvature',[1,1])
    %%     end
    %%     axis equal
    %end

    % A=zeros(4094,4096);

    % for m=1:length(x)
    %   A(x(m),y(m))=dwell(m);
    % end
    % B=autoCrop(A);
    % surf(B);
    % imagesc(A)
    % imagesc(B)

  end

  % pbaspect temporarily disabled for quick octave (3.2.4) compatibility
  % (although the function seems to be available on later octave versions)
  if exist('magnitude','var')==1
    subplot(1,2,1);
    xlabel('pixels');
    ylabel('pixels');
    axis([0 4096 0 4096]);
    % pbaspect([1,1,1]);
    subplot(1,2,2);
    xlabel('mum');
    ylabel('mum');
    axis([0 res*4096 0 res*4096]);
    % pbaspect([1,1,1]);
  else
    xlabel('pixels');
    ylabel('pixels');
    axis([0 4096 0 4096]);
    % pbaspect([1,1,1]);
  end

end
