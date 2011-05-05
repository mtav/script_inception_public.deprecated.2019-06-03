function [TYPE_ID, TYPE_NAME] = getDataType(FILE)
  [ folder, basename_noext, ext ] = fileparts(FILE);
  basename = [basename_noext, ext];
  unknown = 1;
  if ~isempty(regexp(basename,'^p.*\.(prn|dat)$','ignorecase'))
    unknown = 0;
    TYPE_ID = 1;
    TYPE_NAME = 'Probe';
  end
  if ~isempty(regexp(basename,'^[xyz]\d+.*\d\d\.(prn|dat)$','ignorecase'))
    unknown = 0;
    TYPE_ID = 2;
    TYPE_NAME = 'TimeSnapshot';
  end
  if ~isempty(regexp(basename,'^[xyz][a-z{|}~][a-z{]?.*\d\d\.(prn|dat)$','ignorecase'))
    unknown = 0;
    TYPE_ID = 3;
    TYPE_NAME = 'FrequencySnapshot';
  end
  if unknown & isempty(regexp(basename,'^ref\.(prn|dat)$','ignorecase'))
    disp(['WARNING: unknown data : ',basename])
    ok = 0;
    TYPE_ID = -1;
    TYPE_NAME = 'unknown';
    return
  end
end
