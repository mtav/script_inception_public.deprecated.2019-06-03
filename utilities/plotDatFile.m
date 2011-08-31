function plotDatFile(DATFILE)
  % CLEAR ALL removes all variables, globals, functions and MEX links.
  %clear all
  % CLC clears the command window and homes the cursor.
  %clc
  format long e
  
  [header, fin1] = hdrload(DATFILE);
  
  x= fin1(:,1);
  z= fin1(:,2);
  Exre = fin1(:,3);
  
  plot3(x,z,Exre)
  
  %plot(x,Exre)
  %plot(z,Exre)
end
