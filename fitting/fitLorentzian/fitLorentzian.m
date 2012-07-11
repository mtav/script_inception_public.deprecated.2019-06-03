% [Q, vStart, vEnd] = fitLorentzian(X, Y, xmin, xmax)
%
% This function tries to fit Y using the following function:
%  y = y0 + (2*A/pi).*(w./(4*(x-x0).^2+w.^2))
%
% return values:
% vStart = [x0, y0, A, FWHM] from a simple look at data properties like min, max, etc
% vEnd = [x0, y0, A, FWHM] from the real fitting function
% Q = vEnd(1)/vEnd(4) -> the Q factor
% 
% NOTE: Used to be named getQfactor() before.
function [Q, vStart, vEnd] = fitLorentzian(X, Y, xmin, xmax)

  % limit the data to an [xmin,xmax] fitting range based on the previous plot
  [Xzoom,Yzoom] = zoomPlot(X,Y,xmin,xmax);
  
  % calculate some fit start values from the peak
  [x0, y0, A, FWHM] = getLorentzStartValues(Xzoom, Yzoom, 0);
  vStart = [x0, y0, A, FWHM];
  
  % fit the peak with a lorentz function
  [x0, y0, A, FWHM] = getLorentzEndValues(Xzoom, Yzoom, vStart, 0);
  vEnd = [x0, y0, A, FWHM];
  
  % calculate the Q factor
  Q = vEnd(1)/vEnd(4);
end
