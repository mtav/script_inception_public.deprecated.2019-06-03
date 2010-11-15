function BMPtoSTR()
    [fileName,pathName] = uigetfile('*.bmp','Select input BMP-file','H:\');

    % dwell=10;
    % rep=10;
    % step=1;

    dwell=11;
    rep=12;
    step=13;


    center=1;
    scanType='twoway';
    scanDir='h';

    fid0=fopen([pathName,'\',fileName],'r');


    A=imread([pathName,'\',fileName]);
    A=A(:,:,1);
    A=not(A);
    [x,y]=ScanIm(A,'twoway','h', 1);


    if center
        x=x+2048-round((min(x)+max(x))/2);
        y=y+1980-round((min(y)+max(y))/2);
    end

    fid=fopen([pathName,fileName,'_rep',num2str(rep),'_step',num2str(step),'_dw',num2str(dwell),'.str'],'w+');
    fprintf(fid,'s\r\n%i\r\n%i\r\n',rep,length(x));
    fprintf(fid,[num2str(dwell),' %i %i\r\n'],[x;y]);
    fclose(fid);
end
