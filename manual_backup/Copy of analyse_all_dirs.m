function analyse_all_dirs(SRCDIR, DSTDIR)
	
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
	function processProbe(SUBDIR,BASE)
		format long e
		INFILE = [SRCDIR,filesep,SUBDIR,filesep,BASE,'.prn'];
		if ~(exist(INFILE,'file'))
			fprintf('WARNING: File %s not found\n',INFILE);
			return;
		end
		[header,data] = hdrload(INFILE);
		% Time Ex Ey Ez Hx Hy Hz 
		out = data(:,2);
		save([DSTDIR,filesep,SUBDIR,filesep,BASE,'_Ex.prn'],'out','-ascii');
	end
	% ===================
	function writeHarmInvArgs(SUBDIR)
		%=======================================
		% analyze top probes from source pillar
		%=======================================
		% get pillar cavity frequency
		dt_vec = [0,0,0,0];
		fmin_vec = [0,0,0,0];
		fmax_vec = [0,0,0,0];
		[ vEnd1, vStart1, dt_vec(1), fmin_vec(1), fmax_vec(1) ] = analyzePRN([ SRCDIR, filesep, SUBDIR, filesep, 'p62id.prn'], 1/4);
		[ vEnd2, vStart2, dt_vec(2), fmin_vec(2), fmax_vec(2) ] = analyzePRN([ SRCDIR, filesep, SUBDIR, filesep, 'p71id.prn'], 1/4);
		[ vEnd3, vStart3, dt_vec(3), fmin_vec(3), fmax_vec(3) ] = analyzePRN([ SRCDIR, filesep, SUBDIR, filesep, 'p80id.prn'], 1/4);
		[ vEnd4, vStart4, dt_vec(4), fmin_vec(4), fmax_vec(4) ] = analyzePRN([ SRCDIR, filesep, SUBDIR, filesep, 'p89id.prn'], 1/4);
		for i=1:length(dt_vec)
			fprintf('%d: dt=%E fmin=%E fmax=%E\n', i, dt_vec(i), fmin_vec(i), fmax_vec(i));
		end
		dt = min(dt_vec);
		fmin = min(fmin_vec);
		fmax = max(fmax_vec);
		%write parameters to file
		file = fopen([DSTDIR,filesep,SUBDIR,filesep,'harminv_parameters.txt'],'w');
		fprintf('final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
		fprintf(file,'final: dt=%E fmin=%E fmax=%E\n', dt, fmin, fmax);
		fclose(file);
		
	end
	% ===================
	
	cd(SRCDIR)
	DIRS = dir('pillar_*');
	for i=1:length(DIRS)
		close all;
		fprintf('===>Processing %s\n',DIRS(i).name);
		% [ SRCDIR,filesep,DIRS(i).name ];
		% [ DSTDIR,filesep,DIRS(i).name ];
				
		mkdir([DSTDIR,filesep,DIRS(i).name]);
		writeHarmInvArgs(DIRS(i).name);
		processProbe(DIRS(i).name,'p62id');
		processProbe(DIRS(i).name,'p71id');
		processProbe(DIRS(i).name,'p80id');
		processProbe(DIRS(i).name,'p89id');

		% cd(SRCDIR);
		% generate_resonance_pillar(DIRS(i).name, 'D:\Floflo');

	end
	
end
