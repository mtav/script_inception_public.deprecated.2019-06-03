function DProcess(folder)
  % folder=uigetdir();
  %folder='J:\optics\Erman\Optimal vertical emission oPC cavities(optL3)\48nm_half\65400';
  %folder='J:\optics\Erman\qedc3_3_0525b_6_30_1';
  XFsnapFiles=dir([folder,'\x*01.prn']);
  YFsnapFiles=dir([folder,'\y*01.prn']);
  ZFsnapFiles=dir([folder,'\z*01.prn']);
  
  % [InpFileName,InpPathName] = uigetfile('*.inp','Select INP file','J:\optics\Erman\Optimal vertical emission oPC cavities(optL3)\48nm_half\65400');
  inpfile=dir([folder,filesep,'*.inp']);
  inpfile
  inpfile=[folder,filesep,inpfile(1).name];
  inpEntries=GEO_INP_reader({inpfile});
  
  XSnaps={};YSnaps={};ZSnaps={};
  for m=1:length(inpEntries)
    if strcmp(lower(inpEntries{m}.type),'frequency_snapshot')
      % Findout which plane it is
      data=inpEntries{m}.data;
      if cell2mat(data(8))==cell2mat(data(11))
        snapNo=length(XSnaps)+1;
        XSnapEntry.fileName=XFsnapFiles(snapNo).name;
        XSnapEntry.pos=data(8);
        XSnaps{snapNo}=XSnapEntry;  
      elseif cell2mat(data(9))==cell2mat(data(12))
        snapNo=length(YSnaps)+1;
        YSnapEntry.fileName=YFsnapFiles(snapNo).name;
        YSnapEntry.pos=data(9);
        YSnaps{snapNo}=YSnapEntry;
      elseif cell2mat(data(10))==cell2mat(data(13))
        snapNo=length(ZSnaps)+1;
        ZSnapEntry.fileName=ZFsnapFiles(snapNo).name;
        ZSnapEntry.pos=data(10);
        ZSnaps{snapNo}=ZSnapEntry;
      end
    end
  end
  
  xLimits=[];  % The limits of the surronding box.
  yLimits=[];
  zLimits=[];
  
  [prnFileNames,prnPathName] = uigetfile('*.prn','Select 6 PRN files',folder,'MultiSelect','on');
  prnFileNames=sort(prnFileNames);
  
  for n=1:5
    prnFileName=prnFileNames{n};
    plane=prnFileName(1)-119;
  
    if plane==1
      for m=1:length(XSnaps)
        if strcmp(prnFileName,XSnaps{m}.fileName)
          break;
        end 
      end
      xLimits(length(xLimits)+1)=XSnaps{m}.pos;
    elseif plane==2
      for m=1:length(YSnaps)
        if strcmp(prnFileName,YSnaps{m}.fileName)
          break;
        end 
      end
      yLimits(length(yLimits)+1)=YSnaps{m}.pos;
    elseif plane==3
      for m=1:length(ZSnaps)
        if strcmp(prnFileName,ZSnaps{m}.fileName)
          break;
        end 
      end
      zLimits(length(zLimits)+1)=ZSnaps{m}.pos;
    end
  end
  
  xLimits=[xLimits,1e20];
  xLimits=sort(xLimits);
  [yLimits,k]=sort(yLimits);
  zLimits=sort(zLimits);
  
  Res=[];
  for m=1:5
    [jj,f]=fileparts(prnFileNames{m});
    plane=f(1)-119;
    [header,data,ui,uj]=readPrnFile([prnPathName,prnFileNames{m}]);
    figure(1)
    imagesc(ui,uj,data(:,:,1)')
    if plane==1
      minui=min(find(ui>yLimits(1)));
      maxui=max(find(ui<=yLimits(2)));
      
      minuj=min(find(uj>zLimits(1)));
      maxuj=max(find(uj<=zLimits(2)));
      
      colNames={'Eyre','Eyim','Hzre','Hzim','Ezre','Ezim','Hyre','Hyim'};
    elseif plane==2
      minui=min(find(ui>xLimits(1)));
      maxui=max(find(ui<=xLimits(2)));
      
      minuj=min(find(uj>zLimits(1)));
      maxuj=max(find(uj<=zLimits(2))); 
      
      colNames={'Exre','Exim','Hzre','Hzim','Ezre','Ezim','Hxre','Hxim'};
    elseif plane==3
      minui=min(find(ui>xLimits(1)));
      maxui=max(find(ui<=xLimits(2)));
      
      minuj=min(find(uj>yLimits(1)));
      maxuj=max(find(uj<=yLimits(2)));
      colNames={'Exre','Exim','Hyre','Hyim','Eyre','Eyim','Hxre','Hxim'};
    end
      
    data=data(minuj:maxuj,minui:maxui,:);
    figure(2)
    imagesc(data(:,:,1)')
    
    colIndices=zeros(1,length(colNames));
  
    Fields=zeros([size(data,1),size(data,2),length(colNames)]);
  
    for n=1:length(colNames)
      for o=1:length(header)
        if strcmp(header{o},colNames{n})
          Fields(:,:,n)=data(:,:,o-2);
        end
      end
    end
  
    i=sqrt(-1);
  
    PFD=0.5*real((Fields(:,:,1)+i*Fields(:,:,2)).*conj(Fields(:,:,3)+i*Fields(:,:,4))-(Fields(:,:,5)+i*Fields(:,:,6)).*conj(Fields(:,:,7)+i*Fields(:,:,8)));
    figure(3)
    imagesc(PFD')
    uiL=ui(minui-1:maxui);
    ujL=uj(minuj-1:maxuj);
    
    AreaM=repmat(diff(ujL),1,length(uiL)-1).*repmat(diff(uiL)',length(ujL)-1,1);
    imagesc(AreaM')
    
    Res(m)=sum(sum(PFD.*AreaM));
    figure(4)
    imagesc((PFD.*AreaM)')
  end
  
  Res(3)/sum(Res)
end
