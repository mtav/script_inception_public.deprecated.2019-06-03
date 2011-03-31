function [ filename, alphaID, pair ] = numID_to_alphaID(numID, snap_plane, probe_ident, snap_time_number)
  % Converts numeric IDs to alpha IDs used by Bristol FDTD 2003
  % function [ filename, alphaID, pair ] = numID_to_alphaID(numID, snap_plane, probe_ident, snap_time_number)
  % examples:
  % 26 -> z
  % 26+27 -> a{
  % MAXIMUM NUMBER OF SNAPSHOTS: 32767 (=(2^8)*(2^8)/2 -1)
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE RETURN to aa: 6938 = 26+256*27
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE DUPLICATE IDs: 4508 = 26+(6-(ord('a')-1)+256)*27+1 (6=character before non-printable bell character)
  % MAXIMUM NUMBER OF SNAPSHOTS BEFORE ENTERING DANGER AREA (non-printable characters): 836 = 26+(126-(ord('a')-1))*27

  if numID<1 | numID>836
    error('numID must be between 1 and 836 or else you will suffer death by monkeys!!!');
  end
  
  if exist('snap_plane','var')==0
    snap_plane = 'x';
  end

  if exist('probe_ident','var')==0
    probe_ident = 'id';
  end

  if exist('snap_time_number','var')==0
    snap_time_number = 0;
  end

  function ret = div(A,B)
    ret = idivide(int32(A),int32(B));
  end

  ilo = mod(snap_time_number,10);
  ihi = div(snap_time_number,10);
  
  if numID<27
    alphaID = char(numID + double('a')-1);
  else
    alphaID = strcat(char(div(numID, 27) + double('a')-1), char(mod(numID, 27) + double('a')));
  end

  filename = strcat({snap_plane}, alphaID, {probe_ident}, char(ihi + double('0')), char(ilo + double('0')), '.prn');
  pair = [num2str(numID),':',alphaID];
  % disp(filename);
  % disp(alphaID);
  % disp(pair);
  
  filename = char(filename);
end
