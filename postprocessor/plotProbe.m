function [ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global ] = plotProbe(filename, probe_col, autosave, imageSaveName, hide_figures, plotNothing)
  % Usage:
  %[ wavelength_nm, Q_lorentz, Q_harminv_local, Q_harminv_global ] = plotProbe(filename, probe_col, autosave, imageSaveName, hide_figures)

  % defaults
  wavelength_nm = -1
  Q_lorentz = -1
  Q_harminv_local = -1
  Q_harminv_global = -1

  % default arguments
  if exist('autosave','var')==0; autosave = false; end;
  %if exist('imageSaveName','var')==0; imageSaveName = false; end;
  if exist('hide_figures','var')==0; hide_figures = false; end;
  if exist('plotNothing','var')==0; plotNothing = false; end;  

  %name|autosave|save|name|result
  %0   |0       |0   |0   |no save
  %0   |1       |1   |0   |save with default name
  %1   |0       |1   |1   |save with name
  %1   |1       |1   |1   |save with name

  %if ~imageSaveName

  %end

  DoAnalysis = true;
  plotLorentzFit = false;
  computeLorentz = true;
  computeHarminvLocal = true;
  computeHarminvGlobal = true;
  zoomFFT = true;
  Qtext = true;
  peakStars = true;

  [ folder, basename, ext ] = fileparts(filename);
  [ geoname_folder, geoname_basename ] = fileparts(folder);

  % read the PRN file
  [header, data] = readPrnFile(filename);
  time_mus = 1e-12*data(:,1);

  % check if a valid probe_col was given. Else show error and display list of valid values.
  if ( exist('probe_col','var')==0 ) || (probe_col<1) || (probe_col>length(header))
    warning('Please choose an integer value for probe_col from the following:')
    for idx=1:length(header)
     disp([num2str(idx),' : ',char(header(idx))]);
    end
    return;
  end
  data_name = header(probe_col);
  data_time_domain = data(:,probe_col);

  % calculate timestep
  % WARNING: The timestep is considered to be constant here!!!
  dt_mus = time_mus(2)-time_mus(1);  % data(*,1) being in 10^-18 s (because input frequency is in 10^6 Hz), dt is in 10^-18 s/1e-12 = 10^-6 s

  % cut beginning of time signal:
  tmin = 6e-8
  if tmin<time_mus(end)
    [time_mus,data_time_domain] = zoomPlot(time_mus,data_time_domain,tmin,time_mus(end));
  else
    warning( [ 'tmin = ', num2str(tmin),' >= time_mus(end) = ', num2str(time_mus(end)) ] );
  end

  % calculate the FFT
  % (with NFFT = double the number of points you want in the output = 2^19)
  % (probe_col = whatever column you want from the time probe file, i.e. Ex,Ey,etc)
  %[calcFFT_output_oldstyle, lambda_vec_mum_oldstyle, freq_vec_Mhz_oldstyle] = calcFFT(data_time_domain,dt_mus, 2^22);
  [calcFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus);

  % convert lambda to nm
  lambda_vec_nm = 1e3*lambda_vec_mum;
  %lambda_vec_nm_oldstyle = 1e3*lambda_vec_mum_oldstyle;

  if ~plotNothing
    % create new figure
    if hide_figures
      fig = figure('visible','off');
    else
      fig = figure('visible','on');
    end
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % plot in the time domain to see the ringdown
  if ~plotNothing
    subplot(1,2,1);
    plot(time_mus,data_time_domain);
  end
  
  if ~plotNothing
    % envelope fitting
    %[xzoom,yzoom] = zoomPlot(time_mus,data_time_domain,4e-8,time_mus(end));
    %[xzoom,yzoom] = zoomPlot(time_mus,data_time_domain,1e-6,time_mus(end));
    [xzoom,yzoom] = zoomPlot(time_mus,data_time_domain,tmin,time_mus(end));
    %res.trace1.x = time_mus
    %res.trace1.y = data_time_domain
    res.trace1.x = xzoom
    res.trace1.y = yzoom
    %ringdown(res,0.01)
  
    % go back to normal figure
    %figure(fig)
    
    xlabel('time (mus)');
    %ylabel(data_name);
    ylabel([char(data_name),' (arbitrary units)']);

    title( [ geoname_basename,' ', basename, ' ', char(data_name) ],'Interpreter','none');
    %title('Transversal field amplitude');
  end
  
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
  
  if ~plotNothing
    axis([xmin, xmax, 1.1*ymin, 1.1*ymax]);
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % plot the FFT to locate the resonance peak
  % define X and Y for the fitting (Y = power)
  X = lambda_vec_nm;
  %X_oldstyle = lambda_vec_nm_oldstyle;
  Y = calcFFT_output.* conj(calcFFT_output);
  %Y_oldstyle = calcFFT_output_oldstyle.* conj(calcFFT_output_oldstyle);
  
  % cut of anything to big
  [X,Y] = zoomPlot(X,Y,100,1500);

  if ~plotNothing
    subplot(1,2,2);
    %plot(X,Y,'bx');
    plot(X,Y);
    xlabel('lambda (nm)');
    ylabel(['FFT of ',char(data_name),' (arbitrary units)']);
    title( [ geoname_basename,' ', basename, ' ', char(data_name) ],'Interpreter','none');
    %title('FFT of the transversal field amplitude');
  end

  disp(['DATA INFO: min(Y) = ',num2str(min(Y))]);
  disp(['DATA INFO: max(Y) = ',num2str(max(Y))]);
  if min(Y)==0 & max(Y)==0
    disp('WARNING: empty data');
    return;
  end

  % zoom plot on interesting region
  idx_max = find(Y==max(Y));
  %idx_max_oldstyle = find(Y_oldstyle==max(Y_oldstyle));
  
  ViewingWindowSize = 200;
  %xmin_global = X_oldstyle(idx_max_oldstyle(1)) - ViewingWindowSize;
  %xmax_global = X_oldstyle(idx_max_oldstyle(length(idx_max))) + ViewingWindowSize;
  xmin_global = X(idx_max(1)) - ViewingWindowSize
  xmax_global = X(idx_max(length(idx_max))) + ViewingWindowSize

  % comment this line to get full FFT plot
  if zoomFFT
    if ~plotNothing
      axis([xmin_global, xmax_global, min(Y), 1.1*max(Y)]);
    end
  end

  disp(['DATA INFO: maximums at = ',num2str(X(idx_max))]);

  if DoAnalysis
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
    
    if ~plotNothing
      hold on;
    end

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    [ probefile_folder, probefile_basename, probefile_ext ] = fileparts(filename);
    [ probefile_folder_folder, probefile_folder_basename ] = fileparts(probefile_folder);

    harminv_dir = fullfile( probefile_folder, 'harminv' );
    if ~(exist(harminv_dir,'dir'))
      mkdir(harminv_dir); 
    end
    harminv_dir_local = fullfile( probefile_folder, 'harminv_local' );
    if ~(exist(harminv_dir_local,'dir'))
      mkdir(harminv_dir_local); 
    end
    
    harminv_basepath = [ harminv_dir, filesep, probefile_basename,'_',header{probe_col} ];
    harminv_basepath_local = [ harminv_dir_local, filesep, probefile_basename,'_',header{probe_col} ];
    
    outfileName = [ harminv_basepath, '_harminv.out.txt' ];
    harminvDataFile = [ harminv_basepath, '_harminv.in.txt' ];
    parametersFile = [ harminv_basepath, '_harminv.selection.txt' ];

    outfileName_local = [ harminv_basepath_local, '_harminv.out.txt' ];
    harminvDataFile_local = [ harminv_basepath_local, '_harminv.in.txt' ];
    parametersFile_local = [ harminv_basepath_local, '_harminv.selection.txt' ];

    if computeHarminvGlobal
      lambdaLow_mum = xmin_global*1e-3;
      lambdaHigh_mum = xmax_global*1e-3;

      fid = fopen(harminvDataFile,'w+');
      %fprintf(fid,'%2.8e\r\n',data(:,probe_col));
      fprintf(fid,'%2.8e\r\n',data_time_domain);
      fclose(fid);
      fid = fopen(harminvDataFile_local,'w+');
      %fprintf(fid,'%2.8e\r\n',data(:,probe_col));
      fprintf(fid,'%2.8e\r\n',data_time_domain);
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

    fid = fopen('~/tmpQ.txt', 'at');
    fprintf(fid, '%s\n', [pwd,' | ',filename] );
    fclose(fid);
    
    for n=1:size(peaks,1)
      if peakStars
        if ~plotNothing
          plot(peaks(n,1),peaks(n,2),'r*'); % plot little stars on detected peaks
          %plot(peaks(n,3),Y(closestInd(X,peaks(n,3))),'g*'); % plot little stars on detected peaks
          %plot(peaks(n,4),Y(closestInd(X,peaks(n,4))),'b*'); % plot little stars on detected peaks
        end
      end
      [indS,val] = closestInd(X,peaks(n,1));
      peakWaveLength = peaks(n,1);
      peakValue = peaks(n,2);
      
      %%%%%%%%%%%%
      % plot lorentz fit
      x = peaks(n,1);
      xmin = peaks(n,4);
      xmax = peaks(n,3);
      if computeLorentz
        [Q, vStart, vEnd] = getQfactor(X,Y,xmin,xmax);
        if plotLorentzFit
          if ~plotNothing
            plot(linspace(xmin,xmax,100),lorentz(vEnd,linspace(xmin,xmax,100)),'r-');
          end
        end
      else
        Q = -1;
      end      
      wavelength_nm(n) = peakWaveLength;
      Q_lorentz(n) = Q;
      %%%%%%%%%%%%
      
      if computeHarminvLocal
        Qfactor_harminv = getQfactor_harminv(x, harminvDataFile_local, dt_mus, xmin, xmax)
      else
        Qfactor_harminv = -1;
      end
        
      if size(Qfactor_harminv,1)>0
        Q_harminv_local(n) = Qfactor_harminv;
        
        Q1 = ['Q_L=',num2str(Q_lorentz(n))];
        Q2 = ['Q_{Hl}=',num2str(Q_harminv_local(n))];
        Q3 = ['Q = ',num2str(Q_harminv_global(n))];
        
        if Qtext
          if ~plotNothing
            %text(peakWaveLength, peakValue, {Q1;Q2;Q3}, 'FontSize', 8);
            text(peakWaveLength, peakValue, {Q3}, 'FontSize', 8);
          end
        end
        
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

    end % end of loop through peaks

  end % analysis end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %xmin = 770
  %xmax = 790

  %[Q, vStart, vEnd] = getQfactor(X,Y,xmin,xmax);
  %vEnd
  
  %wavelength_nm(n) = peakWaveLength;
  %Q_lorentz(n) = Q;
  
  %%figure
  %plot(linspace(xmin,xmax,100),lorentz(vStart,linspace(xmin,xmax,100)),'r-');
  %%figure
  %plot(linspace(xmin,xmax,100),lorentz(vEnd,linspace(xmin,xmax,100)),'g-');
  %axis([xmin, xmax, 0, 1.1*max(Y)]);

  %N=10000; xmin=778; xmax=784; Q=112970; y0=0; x0=780.8162; FWHM=x0/Q; A = 0.5*FWHM*(pi*(2.5*1e6-y0)); plot(linspace(xmin,xmax,N),lorentz([x0, y0, A, FWHM],linspace(xmin,xmax,N)),'r-');

  % autosaving
  if autosave == 1
    set(fig, 'Position', get(0,'Screensize')); % Maximize figure.
    figout = [dirname(filename), filesep, basename, '_', char(data_name), '.png'];
    disp(['Saving figure as ',figout]);
    print(fig,'-dpng','-r300',figout);
  end
  
  % normal saving
  if ( exist('imageSaveName','var')~=0 ) & (length(imageSaveName)>0)
    set(fig, 'Position', get(0,'Screensize')); % Maximize figure.
    disp(['Saving figure as ',imageSaveName]);
    print(fig,'-dpng','-r300',imageSaveName);
    %print(fig,'-depsc','-r1500',imageSaveName);
  end

  %name=>save with name
  %no name=>autosave=>save with default name
         %=>no autosave+>no save

  %saveas(gcf,[imageSaveName,'.png'],'png');
  %saveas(gcf,[imageSaveName,'.fig'],'fig');

end
