function getResonanceFrequencies(probefile, colnumP, outputfile)
  % writes the resonance frequencies of probefile/column into outputfile + some plots into dirname(probefile)/harminv
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  computeHarminv = 0;

  clf;
  
  % read the data
  [header, data] = readPrnFile(probefile);

  % parts to build filenames
  [ probefile_folder, probefile_basename, probefile_ext ] = fileparts(probefile);
  [ probefile_folder_folder, probefile_folder_basename ] = fileparts(probefile_folder);
  [ outputfile_folder, outputfile_basename, outputfile_ext ] = fileparts(outputfile);
  harminv_dir = [ probefile_folder, filesep, 'harminv' ];
  harminv_basepath = [ harminv_dir, filesep, probefile_basename,'_',header{colnumP} ];
  harminv_basepath = [ harminv_dir, filesep, probefile_basename,'_',header{colnumP} ];
  title_base = fullfile(probefile_folder_basename, probefile_basename);
  
  if ~(exist(harminv_dir,'dir'))
    mkdir(harminv_dir); 
  end
  
  % plot output filenames
  filename_probe_time_png = [ harminv_basepath,'.png' ];
  filename_probe_time_fig = [ harminv_basepath,'.fig' ];
  filename_probe_freq_png = [ harminv_basepath,'_probeFFT.png' ];
  filename_probe_freq_fig = [ harminv_basepath,'_probeFFT.fig' ];
  filename_harminv_freq_png = [ harminv_basepath,'.png' ];
  filename_harminv_freq_fig = [ harminv_basepath,'.fig' ];
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  figure(1); clf;
  plot(data(:,1)*1e-9,data(:,colnumP));

  title_label = [ title_base, probefile_ext,'  ',header{colnumP} ];

  title(title_label,'Interpreter','none');
  xlabel('time (ns)');
  
  % save time domain plot from probe
  saveas(gcf,filename_probe_time_png,'png');disp(['Saved as ',filename_probe_time_png]);
  saveas(gcf,filename_probe_time_fig,'fig');disp(['Saved as ',filename_probe_time_fig]);
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  dt_mus = 1e-12*(data(2,1)-data(1,1));  % Normally the data in probe file is in values of 1e*18 seconds
  [Y,lambda_mum] = bFFT(data(:,colnumP),dt_mus);
  Mag=2*abs(Y);
  
  aver=sum(Mag)/length(Mag);
  delta=(max(Mag)-aver)/3;
 
  if (delta<0)
    return;
  end

  peaks=peakdet(Mag, delta/3,lambda_mum);
  wavelength_nm=1e3*lambda_mum;
  
  figure(2);hold off;
  plot(wavelength_nm, Mag);
  xlim(1e3*[0.8*min(peaks(:,1)),1.2*max(peaks(:,1))]);
  
  title([ title_base,' ',header{colnumP},'  Spectrum at Timestep:',num2str(length(data))],'Interpreter','none');
  xlabel('Wavelength (nm)');
  ylabel('Mag');

  if computeHarminv

    lambdaLow = 0.4; %0.62; %set min lamda  0.90
    lambdaHigh = 0.8; %set max lamda  0.98

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
    saveas(gcf,[outFile,'.png'],'png');disp(['Saved as ',[outFile,'.png']]);
    saveas(gcf,[outFile,'.fig'],'fig');disp(['Saved as ',[outFile,'.fig']]);
    
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
    
    % save frequency domain plot from probe
    saveas(gcf,filename_probe_freq_png,'png');disp(['Saved as ',filename_probe_freq_png]);
    saveas(gcf,filename_probe_freq_fig,'fig');disp(['Saved as ',filename_probe_freq_fig]);
    
  end
  disp('DONE')
end
