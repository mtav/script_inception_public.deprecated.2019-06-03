function plotneff()
  %n_cavity = nGaAs;
  %n_mirror = nAlGaAs;
  n_inside = 2.4;
  n_outside = 1;
  lambda_nm = 637;

  radius_mum = [0:0.1:5];
  figure;
  
  L_vector = 0:4;
  M_vector = 1:4;
  %L_vector = [0,2];
  %M_vector = [1];
  v_cutoff_mat = zeros(length(L_vector),length(M_vector));
  
  for L_idx = 1:length(L_vector)
    for M_idx = 1:length(M_vector)
      L = L_vector(L_idx);
      M = M_vector(M_idx);
      
      [ real_neff_1,real_neff_2,real_neff_1_vector,real_neff_2_vector,radius_vector_mum, u, v, b, v_cutoff ] = get_neff_2(radius_mum,n_inside,n_outside,L,M,lambda_nm);
      v_cutoff_mat(L_idx,M_idx) = v_cutoff;
      
      subplot(3,1,1);
      grid on; hold on;
      plot(v,b,'r-','LineWidth',1);
      xlabel('v (no unit)');
      ylabel('b (no unit)');
      axis([ 0 12 0 1 ]);

      subplot(3,1,2);
      grid on; hold on;
      plot(v,real_neff_1_vector,'r-','LineWidth',1);
      plot(v,real_neff_2_vector,'b-','LineWidth',1);
      xlabel('v (no unit)');
      ylabel('n_{eff} (no unit)');
      axis([ 0 6.5 n_outside n_inside ]);
      legend('n_{eff} 1','n_{eff} 2');

      subplot(3,1,3);
      grid on; hold on;
      plot(radius_vector_mum,real_neff_1_vector,'r-','LineWidth',1);
      plot(radius_mum,real_neff_1,'ro','LineWidth',1);
      plot(radius_vector_mum,real_neff_2_vector,'b-','LineWidth',1);
      plot(radius_mum,real_neff_2,'bo','LineWidth',1);
      xlabel('radius (mum)');
      ylabel('n_{eff} (no unit)');
      legend('n_{eff} 1','n_{eff} 1','n_{eff} 2','n_{eff} 2');

    end
  end

  v_cutoff_mat

  rad1 = radius_mum;
  rad2 = radius_mum;
  [Rad1, Rad2]=meshgrid(rad1,rad2);
  [r, rg] = reflectivity(get_neff_2(Rad1),get_neff_2(Rad2),1);
  
  figure;
  surf(Rad1,Rad2,r);
  title('r');
  xlabel('radius 1 (mum)');
  ylabel('radius 2 (mum)');
  zlabel('r (no unit)');
  shading interp;
  
  figure;
  surf(Rad1,Rad2,rg);
  title('rg');
  xlabel('radius 1 (mum)');
  ylabel('radius 2 (mum)');
  zlabel('rg (no unit)');
  shading interp;

  delta = [0:0.01:1];
  [r, rg] = reflectivity(get_neff_2(0.5),get_neff_2(0.5+delta),1)
  
  figure;
  grid on; hold on;
  title('reflectivity as a function of delta=rad2-rad1 for rad1=1mum and m=1');
  xlabel('rad2-rad1 (mum)');
  ylabel('reflectivity (no unit)');
  plot(delta,r,'r-');
  plot(delta,rg,'b-');
  legend('r','rg');

  [r, rg] = reflectivity(get_neff_2(0.5),get_neff_2(0.6),1)

end
