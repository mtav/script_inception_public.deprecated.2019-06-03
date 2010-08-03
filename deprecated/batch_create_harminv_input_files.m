function batch_create_harminv_input_files(SRCDIR, DSTDIR)
	% UNFINISHED (identical to create_harminv_input_files at the moment)

	if exist('SRCDIR','var')==0
		disp('SRCDIR not given');
	    SRCDIR = uigetdir('D:\Simulations\BFDTD','SRCDIR');
	end
	if ~(exist(SRCDIR,'dir'))
		disp('dir not found');
		return;
	end

	if exist('DSTDIR','var')==0
		disp('DSTDIR not given');
	    DSTDIR = uigetdir('D:\Simulations\BFDTD','DSTDIR');
	end
	if ~(exist(DSTDIR,'dir'))
		disp('dir not found');
		return;
	end

	% ===================
	function [ vEnd, vStart, dt, fmin, fmax ] = processProbe(BASE)
		format long e
		INFILE = [ SRCDIR, filesep, BASE, '.prn' ];
		if ~(exist(INFILE,'file'))
			fprintf('WARNING: File %s not found\n',INFILE);
			vEnd=0;vStart=0;dt=0;fmin=0;fmax=0;
			return;
		end
		[header,data] = hdrload(INFILE);
		% Time Ex Ey Ez Hx Hy Hz 
		out = data(:,2);
		save([DSTDIR,filesep,BASE,'_Ex.prn'],'out','-ascii');
		
		[ vEnd, vStart, dt, fmin, fmax ] = analyzePRN(INFILE, [DSTDIR,filesep,BASE,'_bilan.txt'], 1/100);
	end
	
	% ===================
	function writeHarmInvArgs()
		%=======================================
		% analyze top probes from source pillar
		%=======================================
		% get pillar cavity frequency
		dt_vec = [0,0,0,0];
		fmin_vec = [0,0,0,0];
		fmax_vec = [0,0,0,0];
		[ vEnd1, vStart1, dt_vec(1), fmin_vec(1), fmax_vec(1) ] = processProbe('p62id');
		[ vEnd2, vStart2, dt_vec(2), fmin_vec(2), fmax_vec(2) ] = processProbe('p71id');
		[ vEnd3, vStart3, dt_vec(3), fmin_vec(3), fmax_vec(3) ] = processProbe('p80id');
		[ vEnd4, vStart4, dt_vec(4), fmin_vec(4), fmax_vec(4) ] = processProbe('p89id');
		
		for i=1:length(dt_vec)
			fprintf('%d: dt=%E fmin=%E fmax=%E\n', i, dt_vec(i), fmin_vec(i), fmax_vec(i));
		end
		dt = min(dt_vec);
		
		if dt==0
			return
		end
		
		fmin = min(fmin_vec);
		fmax = max(fmax_vec);
		%write parameters to file
		file = fopen([DSTDIR,filesep,'harminv_parameters.txt'],'w');
		fprintf('final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
		fprintf(file,'final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
		fclose(file);
		
	end
	% ===================
				
	writeHarmInvArgs();
	
end
