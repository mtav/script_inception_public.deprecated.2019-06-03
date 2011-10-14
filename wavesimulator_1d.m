function wavesimulator_1d(thickness_vector,n_vector,medium_color_vector,wave_color_vector,lambda,signal_origin,object_origin,x_range,n_outside)

  if exist('n_outside','var') == 0; n_outside = 1; end;
  if exist('x_range','var') == 0; x_range = [0,1]; end;
  if exist('signal_origin','var') == 0; signal_origin = 0; end;
  if exist('object_origin','var') == 0; object_origin = 0; end;
  if exist('lambda','var') == 0; lambda = 0.637; end;
  if exist('n_vector','var') == 0; n_vector = [2.4,1,2.4,1]; end;
  %if exist('thickness_vector','var') == 0; thickness_vector = [lambda/n_vector(1),lambda/(4*n_vector(2)),lambda/(4*n_vector(3)),lambda/(n_vector(4))]; end;
  if exist('thickness_vector','var') == 0; thickness_vector = [lambda/n_vector(1),lambda/(2*n_vector(2)),lambda/(2*n_vector(3)),lambda/(n_vector(4))]; end;
  if exist('medium_color_vector','var') == 0; medium_color_vector = {[0,0,1-0.5*n_vector(1)/2.4],[0,0,1-0.5*n_vector(2)/2.4],[0,0,1-0.5*n_vector(3)/2.4],[0,0,1-0.5*n_vector(4)/2.4]}; end;
  if exist('wave_color_vector','var') == 0; wave_color_vector = {[0,0,0],[1,0,0],[0,1,0],[1,1,0]}; end;

  figure;
  hold on;
  
  N = length(n_vector)
  L = sum(thickness_vector)
  
  x(1) = object_origin;
  T(1) = 1;
  t(1) = 1;
  phase(1) = -(2*pi*n_vector(1)/lambda)*signal_origin;
  reflected_amplitude(1) = 0
  transmitted_amplitude(1) = 1

  for i = 1:N
    k(i) = 2*pi*n_vector(i)/lambda;
    if (i>1)
      r(i) = (n_vector(i-1)-n_vector(i))/(n_vector(i-1)+n_vector(i));
      t(i) = (2*n_vector(i-1))/(n_vector(i-1)+n_vector(i));
      R(i) = ((n_vector(i-1)-n_vector(i))/(n_vector(i-1)+n_vector(i)))^2;
      T(i) = (4*n_vector(i-1)*n_vector(i))/(n_vector(i-1)+n_vector(i))^2;
      x(i) = x(i-1) + thickness_vector(i-1);
      phase(i) = phase(i-1) + (k(i-1)-k(i))*x(i)
      reflected_amplitude(i) = transmitted_amplitude(i-1)*R(i)
      transmitted_amplitude(i) = transmitted_amplitude(i-1)*T(i)
    end
  end
  x(N+1) = x(N) + thickness_vector(N);

  for i = 1:N
    if(i>1)
      reflected_wave_x{i} = linspace(x(i-1),x(i),100);
      reflected_wave_y{i} = reflected_amplitude(i)*sin(k(i-1)*reflected_wave_x{i} + phase(i-1));
    end
    transmitted_wave_x{i} = linspace(x(i),x(i+1),100);
    transmitted_wave_y{i} = transmitted_amplitude(i)*sin(k(i)*transmitted_wave_x{i} + phase(i));
  end

  for i = 1:N
    fill([x(i+1),x(i+1),x(i),x(i)],[1,-1,-1,1],medium_color_vector{i});
  end
  
  for i = 1:N
    plot(transmitted_wave_x{i},transmitted_wave_y{i},'Color',wave_color_vector{i},'LineWidth',5);
  end
  for i = 2:N
    plot(reflected_wave_x{i},reflected_wave_y{i},'Color',wave_color_vector{i},'LineWidth',5);
  end

end
