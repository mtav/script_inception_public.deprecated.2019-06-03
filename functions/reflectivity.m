function [ r, rg ] = reflectivity(n1,n2,m)
  r = (n2-n1)./(n2+n1);
  %rg = tanh(m*ln((1+r)/(1-r)))
  rg = (1-(n1./n2).^(2*m))./(1+(n1./n2).^(2*m));
end
