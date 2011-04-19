function plotProbe(filename, probe_col, autosave)

  [ folder, basename, ext ] = fileparts(filename);
  [ geoname_folder, geoname_basename ] = fileparts(folder);

  % read the PRN file
  [header, data] = readPrnFile(filename);
  data_name = header(probe_col);

  time_mus = 1e-12*data(:,1);
  data_time_domain = data(:,probe_col);

  % calculate timestep
  % WARNING: The timestep is considered to be constant here!!!
  dt_mus = time_mus(2)-time_mus(1);  % data(*,1) being in 10^-18 s (because input frequency is in 10^6 Hz), dt is in 10^-18 s/1e-12 = 10^-6 s

  % calculate the FFT
  % (with NFFT = double the number of points you want in the output = 2^19)
  % (probe_col = whatever column you want from the time probe file, i.e. Ex,Ey,etc)
  [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus, 2^19);

  % convert lambda to nm
  lambda_vec_nm = 1e3*lambda_vec_mum;

  % create new figure
  figure;

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % plot in the time domain to see the ringdown
  subplot(1,2,1);
  plot(time_mus,data_time_domain);
  xlabel('time (mus)');
  ylabel(data_name);
  title( [ geoname_basename,' ', basename, ' ', char(data_name) ],'Interpreter','none');
  
  disp(['DATA INFO: min(data_time_domain) = ',num2str(min(data_time_domain))]);
  disp(['DATA INFO: max(data_time_domain) = ',num2str(max(data_time_domain))]);
  if min(data_time_domain)==0 & max(data_time_domain)==0
    disp('WARNING: empty data');
    return;
  end

  % zoom plot on interesting region
  ViewingWindowThreshold = 1e-3; % stop plotting when the remaining values are under this ViewingWindowThreshold*max(Y)
  ymin = min(data_time_domain);
  ymax = max(data_time_domain);
  for idx_max=length(data_time_domain):-1:1;
    if data_time_domain(idx_max)>ViewingWindowThreshold*ymax;
      break;
    end;
  end;
  xmin = time_mus(1);
  xmax = time_mus(idx_max);
  axis([xmin, xmax, 1.1*ymin, 1.1*ymax]);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % plot the FFT to locate the resonance peak
  % define X and Y for the fitting (Y = power)
  X = lambda_vec_nm;
  Y = calcFFT_output.* conj(calcFFT_output);

  subplot(1,2,2);
  plot(X,Y);
  xlabel('lambda (nm)');
  ylabel(['FFT of ',data_name,' (arbitrary units)']);
  title( [ geoname_basename,' ', basename, ' ', char(data_name) ],'Interpreter','none');

  disp(['DATA INFO: min(Y) = ',num2str(min(Y))]);
  disp(['DATA INFO: max(Y) = ',num2str(max(Y))]);
  if min(Y)==0 & max(Y)==0
    disp('WARNING: empty data');
    return;
  end

  % zoom plot on interesting region
  idx_max = find(Y==max(Y));
  ViewingWindowSize = 200;
  xmin = X(idx_max(1)) - ViewingWindowSize;
  xmax = X(idx_max(length(idx_max))) + ViewingWindowSize;

  axis([xmin, xmax, min(Y), 1.1*max(Y)]);

  disp(['DATA INFO: maximums at = ',num2str(X(idx_max))]);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % peak detection
  aver = sum(Y)/length(Y);
  delta = (max(Y)-aver)/9;
 
  if (delta<0)
    disp(['ERROR delta<0 : ',delta])
    return;
  end

  peaks = peakdet(Y, delta, X);
  peaks
  
  hold on;

  Q_lorentz = [1,2,3,4];  
  Q_harminv_local = [11,22,33,44];  
  Q_harminv_global = [111,222,333,444];  
  for n=1:size(peaks,1)
    plot(peaks(n,1),peaks(n,2),'r*'); % plot little stars on detected peaks
    [indS,val] = closestInd(X,peaks(n,1))
    peakWaveLength = peaks(n,1);
    peakValue = peaks(n,2);
    
    Q1 = ['Q=',num2str(Q_lorentz(n))];
    Q2 = ['Q=',num2str(Q_harminv_local(n))];
    Q3 = ['Q=',num2str(Q_harminv_global(n))];
    text(peakWaveLength, peakValue, {Q1;Q2;Q3}, 'FontSize', 16);

    %text(peakWaveLength, peakValue + 0*font_size, );
    %text(peakWaveLength, peakValue + 1*font_size, ,'FontSize',font_size;
    %text(peakWaveLength, peakValue + 2*font_size, ,'FontSize',font_size);
    
    %% Write peaks to a text file.
    %Frequency_Hz = get_c0()/peakWaveLength*1e9;
    %fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\r\n',n,Frequency_Hz,peakWaveLength,Q(indS));
    %disp(Frequency_Hz*10^-6)
    %frequency_struct.PeakNo{end+1} = 
    %frequency_struct.Frequency_Hz{end+1} = 
    %frequency_struct.Wavelength_nm{end+1} = 
    %frequency_struct.QFactor = 
    %frequency_struct_array = 

  end
  
  computeHarminv = 0
  if computeHarminv

    lambdaLow = xmin; %0.62; %set min lamda  0.90
    lambdaHigh = xmax; %set max lamda  0.98

    fid = fopen(harminvDataFile,'w+');
    fprintf(fid,'%2.8e\r\n',data(:,colnumP));
    fclose(fid);
    
    [lambdaH,Q,outFile,err,minErrInd] = doHarminv(harminvDataFile,dt_mus,lambdaLow,lambdaHigh);
    
    figure(3); clf
    plot(lambdaH,Q,'r','LineWidth',2);
    hold on
    rel=1./err; rel=rel/max(rel)*max(Q);
    plot(lambdaH,rel,':')
    hold off
    xlim([lambdaLow lambdaHigh])
    
    if length(Q)
      ylim(sort([0 1.1*max(Q)]))
    end
  
    title(title_base,'interpreter','none')
    xlabel('wavelength(um)')
    ylabel('Q Factor')
    
    % save frequency domain plot from harminv
    saveas(gcf,[outFile,'.png'],'png');disp(['Saved as ',[outFile,'.png']]);
    saveas(gcf,[outFile,'.fig'],'fig');disp(['Saved as ',[outFile,'.fig']]);
    
    fid = fopen(parametersFile,'w+');
    fprintf(fid,'PeakNo\tFrequency(Hz)\tWavelength(nm)\tQFactor\t\r\n');

    for n=1:size(peaks,1)
      figure(2); hold on;
      plot(1e3*peaks(n,1),peaks(n,2),'r*')
      [indS,val]=closestInd(lambdaH,peaks(n,1));
      peakWaveLength=1e3*peaks(n,1);
      peakValue=peaks(n,2);
      text(peakWaveLength,peakValue,['Q=',num2str(Q(indS))],'FontSize',16);
      %% Write peaks to a text file.
      Frequency_Hz = get_c0()/peakWaveLength*1e9;
      fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\r\n',n,Frequency_Hz,peakWaveLength,Q(indS));
      disp(Frequency_Hz*10^-6)
      %frequency_struct.PeakNo{end+1} = 
      %frequency_struct.Frequency_Hz{end+1} = 
      %frequency_struct.Wavelength_nm{end+1} = 
      %frequency_struct.QFactor = 
      %frequency_struct_array = 

    end
      
    fclose(fid);     
  end % end of if computeHarminv

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % autosaving
  if autosave == 1
    figout = [folder, filesep, basename, '_', char(data_name), '.png'];
    disp(['Saving figure as ',figout]);
    print(gcf,'-dpng','-r300',figout);
  end
end
