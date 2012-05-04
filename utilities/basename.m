% DESCRIPTION
%        Returns NAME with any leading directory components removed.  If specified, also remove a trailing SUFFIX.

function ret = basename(NAME,SUFFIX)
  ret = '';
  [pathstr, namestr, ext] = fileparts(NAME);
  if exist('SUFFIX','var')==1 && strcmp(ext,SUFFIX)
    ret = namestr;
  else
    ret = [namestr,ext];
  end
end
