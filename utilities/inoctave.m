function in = inoctave()
  persistent inout;
  inout = exist('OCTAVE_VERSION','builtin') ~= 0;
  in = inout; % exist('OCTAVE_VERSION','builtin') ~= 0;
end

% possible alternative code
%if size(ver('Octave'),1)
    %OctaveMode = 1;
%else
    %OctaveMode = 0;
%end
