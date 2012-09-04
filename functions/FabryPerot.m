% function [reflectance,transmittance] = FabryPerot(lambda,n_outside,n_inside,thickness,incidence_angle)
function [reflectance,transmittance] = FabryPerot(lambda,n_outside,n_inside,thickness,incidence_angle)
  % Normal Reflection Coefficient R
  R = ((n_inside-n_outside)/(n_inside+n_outside))^2;
  % The phase difference between each succeeding reflection is given by δ
  delta = (2*pi./lambda).*(2*n_inside*thickness*cos(incidence_angle));
  % finesse F
  F = (4*R)/(1-R)^2;
  transmittance = 1./(1+F*sin(delta/2).^2);
  reflectance = 1-transmittance;  
end
