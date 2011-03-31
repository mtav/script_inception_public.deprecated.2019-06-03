function create_harminv_input_file(INFILE,OUTFILE,PARAMFILE,lambdamin_nm,lambdamax_nm)
  % create harminv input files from INFILE and store it in OUTFILE and PARAMFILE

  if ~(exist(INFILE,'file'))
    error([INFILE,' not found']);
  end

  format long e
  [header,data] = hdrload(INFILE);
  % Time Ex Ey Ez Hx Hy Hz 
  out = data(:,2);
  save(OUTFILE,'out','-ascii');
  
  fmin = 10^3*get_c0()/lambdamax_nm;
  fmax = 10^3*get_c0()/lambdamin_nm;

  dt = 1e-12*(data(2,1)-data(1,1));  % data(*,1) being in 10^-18 s, dt is in 10^-18 s/1e-12 = 10^-6 s
          
  %write parameters to file
  file = fopen(PARAMFILE,'w');
  fprintf('final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
  fprintf(file,'final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
  fclose(file);	
end

