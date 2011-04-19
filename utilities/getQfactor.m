function [Q, vStart, vEnd] = getQfactor(X,Y,xmin,xmax)
  % limit the data to an [xmin,xmax] fitting range based on the previous plot
  [Xzoom,Yzoom]=zoomPlot(X,Y,xmin,xmax);
  
  % calculate some fit start values from the peak
  [x0, y0, A, FWHM] = getLorentzStartValues(Xzoom, Yzoom, 0);
  vStart = [x0, y0, A, FWHM];
  
  % fit the peak with a lorentz function
  [x0, y0, A, FWHM] = mylorentzfit(Xzoom, Yzoom, vStart, 0);
  vEnd = [x0, y0, A, FWHM];
  
  % calculate the Q factor
  Q = vEnd(1)/vEnd(4);
end
