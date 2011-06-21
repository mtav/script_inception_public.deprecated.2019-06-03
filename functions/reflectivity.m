function [ rg2 ] = reflectivity(n1,n2,m)
  %r = (n2-n1)/(n2+n1)
  %rg1 = tanh(m*ln((1+r)/(1-r)))
  rg2 = (1-(n1/n2)^m)/(1+(n1/n2)^m)
end
