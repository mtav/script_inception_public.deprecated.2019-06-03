function [ E, lambda, radius_vector, E_vector, lambda_vector ] = resonanceEnergy(nGaAs, nAlGaAs, n0, Lcav, radius)
  %resonanceEnergy(3.521,2.973,1,253,radius)
  %input:
  % nGaAs=3.521;%no unit
  % nAlGaAs=2.973;%no unit
  % n0 = 1; % air refractive index
  % Lcav = 253; % (nm)
  % radius (mum) of micropillar microcavity (kn in nm^-1 and v has no unit)
  %output:
  % E (meV)
  % lambda (nm)
  
  neff = sqrt(2*nGaAs^4/(3*nGaAs^2-nAlGaAs^2)); % average refractive index

  % Mode LPlm
  L = 0;
  M = 1;

  racines_l = zero_besselj(L);
  racines_l_moins_1 = zero_besselj(L-1);

  switch L
    case {0},
       borne_u_inf = racines_l_moins_1(M);
       borne_u_sup = racines_l(M);
    case {1},
       borne_u_inf = racines_l_moins_1(M);
       borne_u_sup = racines_l(M+1);
    otherwise,
       borne_u_inf = racines_l_moins_1(M+1);
       borne_u_sup = racines_l(M+1);
  end

  v_cutoff = borne_u_inf;
  v_max =100;
  % v_max =12;
  v = (v_cutoff+0.01):0.2:v_max; % waveguide parameter
  n_points = length(v);
  u = zeros(n_points, 1);

  u_min = borne_u_inf + sqrt(eps);

  for i = 1:n_points,
     u_max = min( v(i)-sqrt(eps), abs(borne_u_sup-sqrt(eps)));
     if sign(eq_transc_bv(u_min, v(i), L)) ~= sign(eq_transc_bv(u_max, v(i), L)),
      opts = optimset('Display', 'off', 'TolX', 1e-5); 
      u(i) = fzero('eq_transc_bv', [u_min u_max], opts, v(i), L);
     else
     u(i) = v(i);
     end 
  end

  b = 1 - (u.^2 ./ v'.^2); % = u^2/v^2
  w = sqrt(v'.^2 - u.^2);

  lambda_vector = sqrt(b.*(neff^2-n0^2)+n0^2)*Lcav*(nGaAs/neff); % (nm)
  E_vector = (get_h()*get_c0()/get_e())./(lambda_vector.*10^(-9)); %energy (eV)
  E_vector = E_vector'*1000; % energy (meV)
  k0 = 2*pi./lambda_vector; % free space wave number
  kn = k0.*sqrt(neff^2-n0^2); 
  radius_vector = v./(kn'*1000); % radius (mum) of micropillar microcavity (kn in nm^-1 and v has no unit)
  % lambda_vector = 10^9*get_h()*get_c0()./(E_vector*10^-3*get_e()); % nm

  % subplot(2,1,1);
  % plot(radius_vector,E_vector,'k-','LineWidth',1);
  % grid on;
  % hold on;
  % xlabel('Radius (\mum)');
  % ylabel('dE (meV)');

  % subplot(2,1,2);
  % plot(radius_vector,lambda_vector,'k-','LineWidth',1);
  % grid on;
  % hold on;
  % xlabel('Radius (\mum)');
  % ylabel('\lambda (nm)');
  
  function ret = interpolate(x_vector,y_vector,idx1,idx2,x)
    ret = y_vector(idx1) + (y_vector(idx2)-y_vector(idx1))/(x_vector(idx2)-x_vector(idx1))*(x-x_vector(idx1));
  end
  
  E=[];
  lambda=[];
  for i=1:length(radius)
    r = radius(i);
    idx = find(min(abs(radius_vector-r))==abs(radius_vector-r));
    if r<radius_vector(idx)
      if idx-1>0
        E = [E, interpolate(radius_vector, E_vector, idx-1, idx, r)];
        lambda = [lambda, interpolate(radius_vector, lambda_vector, idx-1, idx, r)];
      else
        E=[E,E_vector(1)];
        lambda=[lambda,lambda_vector(1)];
      end
    else
      if idx+1 <= length(radius_vector)
        E = [E, interpolate(radius_vector, E_vector, idx, idx+1, r)];
        lambda = [lambda, interpolate(radius_vector, lambda_vector, idx, idx+1, r)];
      else
        E=[E,E_vector(length(radius_vector))];
        lambda=[lambda,lambda_vector(length(radius_vector))];
      end
    end
  end

end
