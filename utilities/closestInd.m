% Finds the index of the closest point of a given vector or matrix 'M' to the
% given point 'p'.
% WARNING: ind, val and abs_err can be vectors!!!
function [ind,val,abs_err]=closestInd(M,p)
  % create absolute error array
  abs_err_array = abs(M-p);
  % get minimum in each direction
  minerr = min(abs_err_array);
  for i=2:ndims(abs_err_array)
    minerr = min(minerr);
  end
  % set return variables
  ind = find(abs_err_array == minerr);
  val = M(ind);
  abs_err = abs_err_array(ind);
end
