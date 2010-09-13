%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Written by Erman Engin, University of Bristol
% 
% NOTES:
% The code might give errors if INP file has other sources than a Gaussian pulse
% Only one field in the excitation component defined in INP should be one.
% That is either Ex or Ey ... Hx...etc;  Otherwise the first nonzero
% component will be translated to ctl.

% PML Layer translation should be implemented using the data in
% inpEntries.boundaries

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[GeoFileName,GeoPathName] = uigetfile('*.geo','Select GEO file','D:\Simulations\BFDTD\');
geofile=[GeoPathName,GeoFileName];

[InpFileName,InpPathName] = uigetfile('*.inp','Select INP file',GeoPathName);
inpfile=[InpPathName,InpFileName];

[geoEntries]=GEO_INP_reader(geofile);
[jj2,inpEntries]=GEO_INP_reader(inpfile);

projectPath=[GeoPathName,'\ctlConversion\'];
mkdir(projectPath)
filename=[projectPath,GeoFileName,'.ctl'];
fid = fopen(filename, 'w+');


%% GEO FILE%
for m=1:length(geoEntries)
    if strcmp(lower(geoEntries{m}.type),'box')
        data=geoEntries{m}.data;
        xl=data(1);
        yl=data(2);
        zl=data(3);
        xu=data(4);
        yu=data(5);
        zu=data(6);
    end
end

simSize=[xu-xl yu-yl zu-zl];
geoCenter=simSize'/2;

xmesh=inpEntries.xmesh; if ~length(xmesh); xmesh=-1; end
ymesh=inpEntries.ymesh; if ~length(ymesh); ymesh=-1; end
zmesh=inpEntries.zmesh; if ~length(zmesh); zmesh=-1; end

dxyz=min([min(xmesh),min(ymesh),min(zmesh)]);
resolution=1/dxyz;

numSteps=inpEntries.flag.numSteps;
fprintf(fid,'(set-param! resolution %2.6f )\r\n',resolution);
fprintf(fid,['(set! geometry-lattice (make lattice (size ',num2str(simSize,'%2.5f '),')))\r\n\r\n;geometry specification\r\n(set! geometry\r\n(list\r\n']);
fprintf(fid,'\r\n');

for m=1:length(geoEntries)
   type=geoEntries{m}.type;
   data=geoEntries{m}.data;
   
   switch lower(type)
   case 'block'
       data(1:6)=data(1:6)-[geoCenter;geoCenter];
       xl=data(1); yl=data(2);zl=data(3);xu=data(4);yu=data(5);zu=data(6);eps=data(7);
       w=data(4)-data(1);h=data(5)-data(2);d=data(6)-data(3);
       
       text=meepBlock([xl+w/2,yl+h/2,zl+d/2],[w,h,d],eps);
       fprintf(fid,text);
   case 'cylinder'
       data(1:3)=data(1:3)-geoCenter;
       xc=data(1);yc=data(2);zc=data(3);ri=data(4);ro=data(5);h=data(6);eps=data(7);
       
       text=meepCylinder([xc,yc,zc],ro,h,[0 1 0],eps);
       fprintf(fid,text);
   case 'sphere'
       data(1:3)=data(1:3)-geoCenter;
       xc=data(1);yc=data(2);zc=data(3);ri=data(4);ro=data(5);h=data(6);eps=data(7);
       
       text=meepSphere([xc,yc,zc],ri,eps);
       fprintf(fid,text);
   end   
end

%% INP FILE

% Excitations
fields={'Ex','Ey','Ez','Hx','Hy','Hz'};
for m=1:length(inpEntries.excitations)
    entry=inpEntries.excitations(m);
    excFrequency=entry.frequency/get_c0();
    excComponent=fields{find([entry.E,entry.H]==1)};
    excSize=abs(entry.P1-entry.P2);
    excCenter=(entry.P1+entry.P2)/2-geoCenter';
    excWidth=entry.time_constant*get_c0();
    fprintf(fid,[';;excitations specification\r\n(set! sources\r\n(list\r\n(make source\r\n(src (make gaussian-src (frequency ',num2str(excFrequency,'%2.7f'),') (width ',num2str(excWidth,'%2.7f'),')\r\n))\r\n(component ',excComponent,')\r\n(center ',num2str(excCenter,'%2.5f '),')\r\n(size ',num2str(excSize,'%2.5f '),'))\r\n)\r\n)\r\n']);

end

% PML Layers
pmlThickness=0.3;
fprintf(fid,';boundaries specification\r\n(set! pml-layers\r\n(list\r\n');

fprintf(fid,['(make pml (direction X) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
fprintf(fid,['(make pml (direction Y) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
fprintf(fid,['(make pml (direction Z) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
fprintf(fid,['(make pml (direction X) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
fprintf(fid,['(make pml (direction Y) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
fprintf(fid,['(make pml (direction Z) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
fprintf(fid,'))\r\n');

% Run Command
fprintf(fid,'(init-fields)\r\n');
runUntil=2*dxyz*numSteps;
fprintf(fid,['(run-until ',num2str(runUntil),'\r\n']);
fprintf(fid,'(at-beginning output-epsilon)\r\n');
for m=1:length(inpEntries.all_snapshots)
    entry=inpEntries.all_snapshots(m);
    sliceCenter=(entry.P1+entry.P2)/2-geoCenter';
    sliceSize=abs(entry.P1-entry.P2);
    atEverySlice=2*dxyz*entry.repetition;
    fprintf(fid,sprintf('(to-appended "Slice%i"\r\n(at-every %2.4g\r\n(in-volume (volume (center %f %f %f) (size %f %f %f))\r\noutput-efield-x)))\r\n',m,atEverySlice,sliceCenter,sliceSize));
    fprintf(fid,'\r\n');
end
fprintf(fid,')\r\n');


fclose(fid);
