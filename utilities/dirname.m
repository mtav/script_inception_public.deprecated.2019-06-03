function dir = dirname(path)
  curDir = pwd;
  [pathstr, name, ext] = fileparts(GetFullPath(path));
  cd(pathstr);
  dir = pwd; % full (absolute) path
  cd(curDir); % get back to where you were
end
