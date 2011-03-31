% This function reads and plots a mask file (.str)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
%       ERMAN ENGIN
%       UNIVERSSITY OF BRISTOL
% 
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [x,y,dwell,rep,numPoints]=readStrFile(filename)

    if (nargin==0)
        [FileName,PathName,FilterIndex] = uigetfile('*.str','',pwd());
        filename=[PathName,filesep,FileName];
    end

    try
        fid=fopen(filename);
        dummy=fgets(fid);
        rep=str2num(fgets(fid));
        numPoints=str2num(fgets(fid));

        M=fscanf(fid,'%f %f %f',[3 inf]);
        fclose(fid);
    catch
        ['Error in oppening file', filename]
        fclose(fid);
    end

    dwell=M(1,:);
    x=M(2,:);
    y=M(3,:);
    plot(x(1:1:end),y(1:1:end),'r')
    xlabel('pixels');
    ylabel('pixels');
    axis([0 4096 0 4096]);

    disp(sprintf('Approximate Mask Duration is %2.5f seconds',sum(dwell)*1e-5+0.008163229517396*numPoints));
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

    A=zeros(4094,4096);

    % for m=1:length(x)
    %   A(x(m),y(m))=dwell(m);
    % end
    % B=autoCrop(A);
    % surf(B);
    % imagesc(A)
    % imagesc(B)
end
