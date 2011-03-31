function [x0,y0,A,w] = getLorentzStartValues(X,Y,isInverted)
  if isInverted == 0
    index_max = find(Y == max(Y) );
    x0 = X(index_max);
    y0 = min(Y);
    X1=X(1:index_max);
    X2=X(index_max:length(X));
    Y1=Y(1:index_max);
    Y2=Y(index_max:length(Y));
    halfmax = (min(Y)+max(Y))/2;
    Ydiff1=abs(Y1-halfmax);
    Ydiff2=abs(Y2-halfmax);
    index_FWHM_1 = find( Ydiff1 == min(Ydiff1) );
    index_FWHM_2 = find( Ydiff2 == min(Ydiff2) );
    w = abs(X2(index_FWHM_2) - X1(index_FWHM_1));
    A = w*(pi*(max(Y)-y0))/2;
  else
    index_min = find(Y == min(Y) );
    x0 = X(index_min);
    y0 = max(Y);
    X1=X(1:index_min);
    X2=X(index_min:length(X));
    Y1=Y(1:index_min);
    Y2=Y(index_min:length(Y));
    halfmax = (min(Y)+max(Y))/2;
    Ydiff1=abs(Y1-halfmax);
    Ydiff2=abs(Y2-halfmax);
    index_FWHM_1 = find( Ydiff1 == min(Ydiff1) );
    index_FWHM_2 = find( Ydiff2 == min(Ydiff2) );
    w = abs(X2(index_FWHM_2) - X1(index_FWHM_1));
    A = w*(pi*(min(Y)-y0))/2;
  end
end
