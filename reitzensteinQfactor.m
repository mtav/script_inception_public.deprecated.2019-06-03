function Q = reitzensteinQfactor(ngaas,nalas,dgaas,dalas,ncav,dcav,lambda,n0,ml,mu)
  meff = 1/2*(ngaas+nalas)/(ngaas-nalas);
  neff = (2*ngaas*nalas)/(ngaas+nalas);
  Lm = meff*(dgaas+dalas);
  Leff = ncav*dcav + 2*neff*Lm
  rl = reitzenstein_reflectivity(n0,nalas,ngaas,ml);
  ru = reitzenstein_reflectivity(n0,nalas,ngaas,mu);
  Q = (2*Leff)/(lambda)*(pi)/(1-rl*ru);
end

function r = reitzenstein_reflectivity(n0,nalas,ngaas,m)
  r = (n0-(nalas/ngaas)^(2*m))/(n0+(nalas/ngaas)^(2*m));
end
