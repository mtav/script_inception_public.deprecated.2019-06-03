function harminv_fit()
  
  %f0 = [30,50,100,1000]
  %Q0 = [20,40,30,2e6]
  %A0 = [10,20,30,40]

  %f0 = [100]
  %Q0 = [5e2]
  %A0 = [40]

  f0 = [30,50,200,1000]
  Q0 = [20,40,30,5e3]
  A0 = [100,20,30,4000]

  dt = 1/(300*max(f0));
  tmin = 0;
  tmax = Q0(1)*1/(min(f0));
  
  disp('=== Creating sample function ===')
  [x,y,fmin,fmax] = expsine(dt, tmin, tmax, f0, Q0, A0);
  
  orig = figure(); hold on;
  plot(x,y,'b.')
  orig_axis = axis();
  res.trace1.x = x;
  res.trace1.y = y;
  disp('=== Running ringdown ===')
  res_rd = ringdown(res)
  
  harminvDataFile = '~/tmpHarminvData.txt';
  
  fid = fopen(harminvDataFile,'w+');
  fprintf(fid,'%2.8e\r\n',y);
  fclose(fid);
  
  fmin
  fmax
  lambdaLow = get_c0()/fmax;
  lambdaHigh = get_c0()/fmin;
  
  disp('=== Running harminv ===')
  [ status, lambda, Q, outFile, err, minErrInd, frequency, decay_constant, amplitude, phase ] = doHarminv(harminvDataFile,dt,lambdaLow,lambdaHigh);
  
  if ( status == 0 )
    if ( length(Q) ~= 0 )
      % calculate time-domain fit based on harminv output
      harminv_time = zeros(size(x));
      %harminv_fig = figure(); hold on;
      figure(orig); hold on;
      for i=1:length(frequency)
        disp([num2str(frequency(i)),', ', num2str(decay_constant(i)),', ', num2str(Q(i)),', ', num2str(amplitude(i)),', ', num2str(phase(i)),', ', num2str(err(i))]);
        %harminv_time = harminv_time + amplitude(i)*sin(2*pi*frequency(i)*x+phase(i)).*exp(-decay_constant(i)*time_mus);
        %harminv_time = harminv_time + amplitude(i)*cos(-2*pi*frequency(i).*x+phase(i)).*exp(decay_constant(i).*x);
        %harminv_time = harminv_time + amplitude(i)*exp(-2*pi*frequency(i).*x+phase(i)).*exp(decay_constant(i).*x);
        harminv_time = harminv_time + amplitude(i) * exp(-1i*(2*pi*frequency(i)*x - phase(i)) - decay_constant(i)*x);
      end
      plot(x,harminv_time,'r');
      plot(x,y,'b.');
      
      ColorSet = varycolor(length(frequency));
      set(gca, 'ColorOrder', ColorSet);
      
      for i=1:length(frequency)
        plot(x, 2*amplitude(i)*exp(-decay_constant(i).*x),'g','LineWidth',10);
      end
      axis(orig_axis);
    else
      warning('harminv was unable to find peaks in the specified frequency range.');
    end
  else
    warning('harminv command failed.');
  end
  
end

function [x,y,fmin,fmax] = expsine(dt, tmin, tmax, f0, Q0, A0)
  x = tmin:dt:tmax;
  y = zeros(size(x));
  
  fmin_list = zeros(size(f0));
  fmax_list = zeros(size(f0));
  
  for i=1:length(f0)
    gamma0 = pi*f0(i)/Q0(i);
    y = y + A0(i)*sin(2*pi*f0(i)*x).*exp(-gamma0*x);

    delta_f0 = f0(i)/Q0(i);
    fmin_list(i) = f0(i) - 10*delta_f0;
    fmax_list(i) = f0(i) + 10*delta_f0;

  end
  
  fmin = min(fmin_list);
  fmax = max(fmax_list);

end
