function create_harminv_input_files(SRCDIR, DSTDIR)

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
	
	cd(SRCDIR);

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
	
	%loop through directories
	DIRS = dir('pillar_*');
	for i=1:length(DIRS)
		fprintf('%s\n',DIRS(i).name);
		mkdir([DSTDIR,filesep,DIRS(i).name]);
		processProbe(DIRS(i).name,'p62id');
		processProbe(DIRS(i).name,'p71id');
		processProbe(DIRS(i).name,'p80id');
		processProbe(DIRS(i).name,'p89id');
	end

end
