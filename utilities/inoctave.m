function in = inoctave ()
  persistent inout;
  inout = exist('OCTAVE_VERSION','builtin') ~= 0;
  in = inout; % exist('OCTAVE_VERSION','builtin') ~= 0;
end
