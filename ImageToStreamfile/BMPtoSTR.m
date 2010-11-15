function BMPtoSTR(dwell, rep, step, FILE)
    % function BMPtoSTR(dwell=10, rep=10, step=1, FILE)
    % converts a bitmap file to a streamfile by considering the red values of the image.
    % maximum red => dwell time = 0
    % minimum red (R=0) => dwell time = max dwell time
    
	if exist('dwell','var')==0
        dwell = 10;
	end
	if exist('rep','var')==0
        rep = 10;
	end
	if exist('step','var')==0
        step = 1;
	end
	if exist('FILE','var')==0
        [fileName,pathName] = uigetfile('*.bmp','Select input BMP-file',getuserdir());
    else
        [ pathName, fileName, ext ] = fileparts(FILE);
        fileName = [ fileName, ext ];
	end

    center=1;
    scanType='twoway';
    scanDir='h';

    fid0=fopen([pathName,filesep,fileName],'r');

    A=imread([pathName,filesep,fileName]);
    A=A(:,:,1);
    A=not(A);
    [x,y]=ScanIm(A,'twoway','h', 1);


    if center
        x=x+2048-round((min(x)+max(x))/2);
        y=y+1980-round((min(y)+max(y))/2);
    end

    fid=fopen([pathName,filesep,fileName,'_rep',num2str(rep),'_step',num2str(step),'_dw',num2str(dwell),'.str'],'w+');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    fprintf(fid,[num2str(dwell),' %i %i\r\n'],[x;y]);
    fclose(fid);
end
