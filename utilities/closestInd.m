% Finds the index of the closest point of a given vector or matrix to the
% given point.

function [ind,val]=closestInd(M,p)
  N=abs(M-p);
  err=N;
  for m=1:ndims(N)
    err=min(err);
  end
  ind=find(N==err);
  val=M(ind);
end
