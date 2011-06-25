function [res, HFW] = getResolution(mag)
  HFW = 304000/mag; % Width of the horizontal scan (um).
  res = HFW/4096; % size of each pixel (mum/pxl).
end
