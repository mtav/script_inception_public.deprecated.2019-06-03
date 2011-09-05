function plotDatFile(DATFILE,column)
  % CLEAR ALL removes all variables, globals, functions and MEX links.
  %clear all
  % CLC clears the command window and homes the cursor.
  %clc
  format long e
  
  [header, data] = hdrload(DATFILE);
  
  x = data(:,1);
  y = data(:,2);
  out = data(:,column);
  plot3(x,y,out)
end
