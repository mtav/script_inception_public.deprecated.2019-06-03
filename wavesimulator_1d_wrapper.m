function wavesimulator_1d_wrapper()
  lambda = 0.637;
  n_vector = [2.4,1,2.4,1];
  thickness_vector = [lambda/n_vector(1),lambda/(4*n_vector(2)),lambda/(4*n_vector(3)),lambda/(n_vector(4))];
  wavesimulator_1d(thickness_vector);
  thickness_vector = [lambda/n_vector(1),lambda/(2*n_vector(2)),lambda/(2*n_vector(3)),lambda/(n_vector(4))];
  wavesimulator_1d(thickness_vector);
end
