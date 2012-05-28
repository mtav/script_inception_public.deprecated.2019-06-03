function [ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global ] = plotProbe(filename, probe_col, autosave, imageSaveName, hide_figures)

  computeHarminvLocal = false
  computeHarminvGlobal = true;

  if exist('hide_figures','var')==0
    hide_figures = false;
  end

  [ folder, basename, ext ] = fileparts(filename);
  [ geoname_folder, geoname_basename ] = fileparts(folder);

  % read the PRN file
  filename
  [header, data] = readPrnFile(filename);
  header
  probe_col
  data_name = header(probe_col);

  time_mus = 1e-12*data(:,1);
  data_time_domain = data(:,probe_col);

  % calculate timestep
  % WARNING: The timestep is considered to be constant here!!!
  dt_mus = time_mus(2)-time_mus(1);  % data(*,1) being in 10^-18 s (because input frequency is in 10^6 Hz), dt is in 10^-18 s/1e-12 = 10^-6 s

  % calculate the FFT
  % (with NFFT = double the number of points you want in the output = 2^19)
  % (probe_col = whatever column you want from the time probe file, i.e. Ex,Ey,etc)
  %[calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus, 2^19);
  [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus, 2^22);

  % convert lambda to nm
  lambda_vec_nm = 1e3*lambda_vec_mum;

  % create new figure
  if hide_figures
    fig = figure('visible','off');
  else
    fig = figure('visible','on');
  end

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % plot in the time domain to see the ringdown
  subplot(1,2,1);
  plot(time_mus,data_time_domain);
  
  % envelope fitting
  %[xzoom,yzoom]=zoomPlot(time_mus,data_time_domain,4e-8,time_mus(end));
  [xzoom,yzoom]=zoomPlot(time_mus,data_time_domain,1e-6,time_mus(end));
  %res.trace1.x = time_mus
  %res.trace1.y = data_time_domain
  res.trace1.x = xzoom
  res.trace1.y = yzoom
  %ringdown(res,0.01)
  
  % go back to normal figure
  %figure(fig)
  
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
  %xmax = time_mus(idx_max);
  xmax = time_mus(length(data_time_domain));
  
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
  xmin_global = X(idx_max(1)) - ViewingWindowSize;
  xmax_global = X(idx_max(length(idx_max))) + ViewingWindowSize;

  % comment this line to get full FFT plot
  axis([xmin_global, xmax_global, min(Y), 1.1*max(Y)]);

  disp(['DATA INFO: maximums at = ',num2str(X(idx_max))]);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % peak detection
  aver = sum(Y)/length(Y);
  delta = (max(Y)-aver)/9;
 
  if (delta<0)
    disp(['ERROR delta<0 : ',num2str(delta)])
    return;
  end

  peaks = peakdet(Y, delta, X);
  peaks
  
  wavelength_nm = zeros(1,size(peaks,1));
  Q_lorentz = zeros(1,size(peaks,1));
  Q_harminv_local = zeros(1,size(peaks,1));
  Q_harminv_global = zeros(1,size(peaks,1));

  %closestInd(Y,peaks(1,3))
  %closestInd(Y,peaks(2,3))
  %closestInd(Y,peaks(3,3))
  %closestInd(Y,peaks(4,3))
  
  hold on;

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  [ probefile_folder, probefile_basename, probefile_ext ] = fileparts(filename);
  [ probefile_folder_folder, probefile_folder_basename ] = fileparts(probefile_folder);
  harminv_dir = fullfile( probefile_folder, 'harminv' );
  
  if ~(exist(harminv_dir,'dir'))
    harminv_dir
    mkdir(harminv_dir); 
  end
  
  harminv_basepath = [ harminv_dir, filesep, probefile_basename,'_',header{probe_col} ];
  outfileName =               [ harminv_basepath, '_harminv.out' ];
  harminvDataFile =           [ harminv_basepath, '_harminv.in' ];
  parametersFile =            [ harminv_basepath, '_harminv.selection' ];

  if computeHarminvGlobal
    lambdaLow_mum = xmin_global*1e-3;
    lambdaHigh_mum = xmax_global*1e-3;

    harminvDataFile
    fid = fopen(harminvDataFile,'w+');
    fprintf(fid,'%2.8e\r\n',data(:,probe_col));
    fclose(fid);
    
    disp('===> Computing global harminv:');
    [ status, lambdaH_mum, Q, outFile, err, minErrInd, frequency, decay_constant, amplitude, phase ] = doHarminv(harminvDataFile,dt_mus,lambdaLow_mum,lambdaHigh_mum);
        
    if ( status == 0 )
      if ( length(Q) ~= 0 )
      
        % calculate time-domain fit based on harminv output
        harminv_time = zeros(size(time_mus));
        %harminv_fig = figure(); hold on;
        for i=1:length(frequency)
          disp([num2str(frequency(i)),', ', num2str(decay_constant(i)),', ', num2str(Q(i)),', ', num2str(amplitude(i)),', ', num2str(phase(i)),', ', num2str(err(i))]);
          %harminv_time = harminv_time + amplitude(i)*sin(2*pi*frequency(i)*time_mus+phase(i)).*exp(-decay_constant(i)*time_mus);
          harminv_time = harminv_time + amplitude(i)*cos(-2*pi*frequency(i).*time_mus+phase(i)).*exp(decay_constant(i).*time_mus);
          %plot(time_mus, amplitude(i)*exp(-decay_constant(i).*time_mus));
        end
        %plot(time_mus,harminv_time);
        
        % go back to the regular programming
        %figure(fig);
        
        lambdaH_nm = lambdaH_mum*1e3;
        
        rel=1./err; rel=rel/max(rel)*max(Q);
        
        fid = fopen(parametersFile,'w+');
        fprintf(fid,'PeakNo\tFrequency(Hz)\tWavelength(nm)\tQFactor\t\r\n');
        for n=1:size(peaks,1)
          [indS,val]=closestInd(lambdaH_nm,peaks(n,1));
          %Q
          %length(Q)
          Q_harminv_global(n) = Q(indS);
          peakWaveLength_nm = peaks(n,1);
          Frequency_Hz = get_c0()/peakWaveLength_nm*1e9;
          fprintf(fid,'%i\t%2.8g\t%2.11g\t%2.8g\r\n',n,Frequency_Hz,peakWaveLength_nm,Q(indS));
        end
        fclose(fid);
      else
        warning('harminv was unable to find peaks in the specified frequency range.');
      end
    else
      warning('harminv command failed.');
    end
  end % end of if computeHarminvGlobal
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  disp('===> Looping through peaks:');
  peaks
  size(peaks,1)

  fid = fopen('~/tmpQ.txt', 'at');
  fprintf(fid, '%s\n', [pwd,' | ',filename] );
  fclose(fid);
  
  for n=1:size(peaks,1)
    plot(peaks(n,1),peaks(n,2),'r*'); % plot little stars on detected peaks
    plot(peaks(n,3),Y(closestInd(X,peaks(n,3))),'g*'); % plot little stars on detected peaks
    plot(peaks(n,4),Y(closestInd(X,peaks(n,4))),'b*'); % plot little stars on detected peaks
    [indS,val] = closestInd(X,peaks(n,1));
    peakWaveLength = peaks(n,1);
    peakValue = peaks(n,2);
    
    x = peaks(n,1);
    xmin = peaks(n,4);
    xmax = peaks(n,3);
    [Q, vStart, vEnd] = getQfactor(X,Y,xmin,xmax);
    
    wavelength_nm(n) = peakWaveLength;
    Q_lorentz(n) = Q;
    plot(linspace(xmin,xmax,100),lorentz(vEnd,linspace(xmin,xmax,100)),'r.');

    if computeHarminvLocal
      disp('=================')
      disp('Qfactor_harminv = getQfactor_harminv(x, harminvDataFile, dt_mus, xmin, xmax)')
      x
      harminvDataFile
      dt_mus
      xmin
      xmax
      disp('=================')
      Qfactor_harminv = getQfactor_harminv(x, harminvDataFile, dt_mus, xmin, xmax)
    else
      Qfactor_harminv = -1
    end
    
    if size(Qfactor_harminv,1)>0
      Q_harminv_local(n) = Qfactor_harminv;
      
      Q1 = ['Q_L=',num2str(Q_lorentz(n))];
      Q2 = ['Q_{Hl}=',num2str(Q_harminv_local(n))];
      Q3 = ['Q_{Hg}=',num2str(Q_harminv_global(n))];
      text(peakWaveLength, peakValue, {Q1;Q2;Q3}, 'FontSize', 8);
      
      fid = fopen('~/tmpQ.txt', 'at');
      fprintf(fid, '%10.0f\t%10.0f\n', peakWaveLength, Q_lorentz(n));
      fclose(fid);

      %text(peakWaveLength, peakValue, {Q1}, 'FontSize', 8);
    end

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
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  set(fig, 'Position', get(0,'Screensize')); % Maximize figure.

  % autosaving
  if autosave == 1
    figout = [dirname(filename), filesep, basename, '_', char(data_name), '.png'];
    disp(['Saving figure as ',figout]);
    print(fig,'-dpng','-r300',figout);
  end
  
  % normal saving
  if ( exist('imageSaveName','var')~=0 ) & (length(imageSaveName)>0)
    disp(['Saving figure as ',imageSaveName]);
    print(fig,'-dpng','-r300',imageSaveName);
    %print(fig,'-depsc','-r1500',imageSaveName);
  end

end
