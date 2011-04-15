function getResonanceFrequencies(probefile, colnumP, outputfile)
  % writes the resonance frequencies of probefile/column into outputfile
  
  computeHarminv = 1;
  lambdaLow = 0.4 %0.62; %set min lamda  0.90
  lambdaHigh = 0.8; %set max lamda  0.98

  clf;
  
  [header, data] = readPrnFile(probefile);
  figure(1); clf;
  plot(data(:,1)*1e-9,data(:,colnumP))
  
  [ probefile_folder, probefile_basename, probefile_ext ] = fileparts(probefile);
  [ probefile_folder_folder, probefile_folder_basename ] = fileparts(probefile_folder);
  [ outputfile_folder, outputfile_basename, outputfile_ext ] = fileparts(outputfile);
  filename_time_png = [filename,'_',header{colnumP}];
  filename_time_fig = [filename,'_',header{colnumP}];
  title_label = [probefile_folder_basename,filesep,probefile_basename, probefile_ext,'  ',header{colnumP}];

  title(title_label);
  xlabel('time (ns)');
  
  % save time domain plot from probe
  saveas(gcf,filename_time_png,'png');
  saveas(gcf,filename_time_fig,'fig');

  dt=1e-12*(data(2,1)-data(1,1));  % Normally the data in probe file is in values of 1e*18 seconds
  [Y,lambda]=bFFT(data(:,colnumP),dt);
  Mag=2*abs(Y);
  
  aver=sum(Mag)/length(Mag);
  delta=(max(Mag)-aver)/3;
 
  if (delta<0)
    return;
  end

  peaks=peakdet(Mag, delta/3,lambda);
  
  %     indMax=min(find(lambda==min(peaks(:,1)))+250,length(lambda));
  %     indMin=max(find(lambda==max(peaks(:,1)))-250,1);

  wavelength=1e3*lambda;
  %     wavelength=1e3*lambda(indMin:indMax); %Unit of wavelength is nm.
  %     Mag=Mag(indMin:indMax);
  figure(2);hold off;
  plot(wavelength,Mag);
  xlim(1e3*[0.8*min(peaks(:,1)),1.2*max(peaks(:,1))])
  
  title([filesP(m).name,' ',header{colnumP},'  Spectrum at Timestep:',num2str(length(data))])
  xlabel('Wavelength (nm)')
  ylabel('Mag')

  if computeHarminv
    harminvFolder
    harminvDataFile=[strrep([harminvFolder,filesep,filesP(m).name],'.prn','_harminv'),'_',header{colnumP},'.txt'];
    fid=fopen(harminvDataFile,'w+');
    fprintf(fid,'%2.8e\r\n',data(:,colnumP));
    fclose(fid);
    
    harminvDataFile
    dt
    lambdaLow
    lambdaHigh
    [lambdaH,Q,outFile,err,minErrInd] = doHarminv(harminvDataFile,dt,lambdaLow,lambdaHigh);
    
    figure(4); clf
    plot(lambdaH,Q,'r','LineWidth',2);
    hold on
    rel=1./err; rel=rel/max(rel)*max(Q);
    plot(lambdaH,rel,':')
    hold off
    xlim([lambdaLow lambdaHigh])
    
    if length(Q)
      ylim(sort([0 1.1*max(Q)]))
    end
  
    title([filename,'_',header{colnumP}],'interpreter','none')
    xlabel('wavelength(um)')
    ylabel('Q Factor')
    
    % save frequency domain plot from harminv
    saveas(gcf,[outFile,'.png'],'png');
    saveas(gcf,[outFile,'.fig'],'fig');
    
    parametersFile=[filename,'_',header{colnumP},'_parameters.txt'];
    fid=fopen(parametersFile,'w+');
    fprintf(fid,'PeakNo\tFrequency(Hz)\tWavelength(nm)\tQFactor\t\r\n');

    frequency_list_file = [filename,'_',header{colnumP},'_parameters.txt'];
    fdsfds
    for n=1:size(peaks,1)
      figure(2); hold on;
      plot(1e3*peaks(n,1),peaks(n,2),'r*')
      [indS,val]=closestInd(lambdaH,peaks(n,1));
      peakWaveLength=1e3*peaks(n,1);
      peakValue=peaks(n,2);
      text(peakWaveLength,peakValue,['Q=',num2str(Q(indS))],'FontSize',16);
      %% Write peaks to a text file.
      fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\r\n',n,get_c0()/peakWaveLength*1e9,peakWaveLength,Q(indS));
      
      fclose(fid);     
    end
    
    figure(2)
    imageName=[filename,'_probeFFT_',header{colnumP},'.png'];
    
    % save frequency domain plot from probe
    saveas(gcf,imageName,'png');
    saveas(gcf,[imageName,'.fig'],'fig');
    
  end
  disp('DONE')
end
