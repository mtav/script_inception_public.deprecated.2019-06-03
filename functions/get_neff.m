function neff = get_neff(n_cavity,n_mirror)
  neff = sqrt(2*n_cavity^4/(3*n_cavity^2-n_mirror^2)); % average refractive index
end
