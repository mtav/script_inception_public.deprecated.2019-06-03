% folder=uigetdir();
snapDirection='y';
Lamda=537.942766;
n=3.5;

snapDirInt=snapDirection-119;

%folder='J:\optics\Erman\Optimal vertical emission oPC cavities(optL3)\48nm_half\65400';
% folder='J:\optics\Erman\M1_13_11\M1_exe_inside\Ex_537.942766\y';
folder='J:\all\4Matthieu\latest\M1_13_11\M1_exe_inside\Ex_537.942766\y';
FsnapFiles=dir([folder,filesep,snapDirection,'*00.prn']);

% [InpFileName,InpPathName] = uigetfile('*.inp','Select INP file','J:\optics\Erman\Optimal vertical emission oPC cavities(optL3)\48nm_half\65400');
inpfile=dir([folder,'\*.inp']);
inpfile=[folder,filesep,inpfile(1).name];
inpEntries=GEO_INP_reader({inpfile});

Snaps={};
for m=1:length(inpEntries)
   data=inpEntries{m}.data;
   if strcmp(lower(inpEntries{m}.type),'frequency_snapshot')
       % Findout which plane it is
       snapNo=length(Snaps)+1;
       if data(7+snapDirInt)==data(10+snapDirInt)
           filename=FsnapFiles(snapNo).name;
           fileNumStr=filename(2:end-7);
           fileNumStr=fileNumStr-96*ones(1,length(fileNumStr));
           val=fileNumStr*fliplr([1:25:length(fileNumStr)*25])';
           
           SnapEntry.fileName=[folder,filesep,filename];
           SnapEntry.pos=data(7+snapDirInt);
           epsFile=dir([folder,filesep,snapDirection,num2str(val),'a*.prn']);
           SnapEntry.epsFile=[folder,filesep,epsFile(1).name];
           Snaps{snapNo}=SnapEntry;  
       end
   elseif strcmp(lower(inpEntries{m}.type),'xmesh')
       mesh{1}=data;
   elseif strcmp(lower(inpEntries{m}.type),'ymesh')
       mesh{2}=data;
   elseif strcmp(lower(inpEntries{m}.type),'zmesh')
       mesh{3}=data;
   end
end


Veff=0;
currMax=0;
Nom=0;
vv=[];

for m=1:length(Snaps)
    disp(m)
    [header,data,ui,uj]=readPrnFile(Snaps{m}.fileName);
    if m==length(Snaps)
        thickness=Snaps{m}.pos-Snaps{m-1}.pos;
    else
        thickness=Snaps{m+1}.pos-Snaps{m}.pos;
    end
    Exmod=data(:,:,1);
    Eymod=data(:,:,4);
    Ezmod=data(:,:,7);
    
    v=1:3;
    ind=find(v~=snapDirInt);

    vi=mesh{ind(1)};
    vj=mesh{ind(2)};
    
    areaM=vj*vi';
    
    [header,eps,ui,uj]=readPrnFile(Snaps{m}.epsFile);
    
    nom=(Exmod.^2+Eymod.^2+Ezmod.^2).*eps(:,:);
    
    % TODO: shouldn't this be:
    % maxVal=nom;
    maxVal=max(sum(sum(nom)));
    vv=[vv,maxVal];
    
    if (maxVal>currMax)
        currMax=maxVal;
    end
        
    Nom=Nom+sum(sum(nom.*areaM*thickness));
    
%     figure(1)
%     imagesc(ui(2:end),uj(2:end),nom);
%     figure(2)
%     imagesc(eps)
end
    
Veff=Nom/currMax 

% Which of those 2 is correct?
Foptn= Veff/(Lamda/(n))^3
% Foptn= Veff/((Lamda/1000)/(2*n))^3
