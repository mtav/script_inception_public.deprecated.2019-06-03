function plotProbe(filename, probe_col, autosave)

  [ folder, basename, ext ] = fileparts(filename);

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
  [cFFT_output, lambda_vec_mum, freq_vec_Mhz] = calcFFT(data_time_domain,dt_mus, 2^19);

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
  Y = cFFT_output.* conj(cFFT_output);

  subplot(1,2,2);
  plot(X,Y);
  xlabel('lambda (nm)');
  ylabel(['FFT of ',data_name,' (arbitrary units)']);

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
  % autosaving
  if autosave == 1
    figout = [folder, filesep, basename, '_', char(data_name), '.png'];
    disp(['Saving figure as ',figout]);
    print(gcf,'-dpng','-r300',figout);
  end
end
