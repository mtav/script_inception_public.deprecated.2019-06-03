function GEOshellscript(filename, BASENAME, EXE, WORKDIR, WALLTIME, NODES, PPN)
	disp('Writing shellscript...')

	%open file
	out = fopen(strcat(filename,'.sh'),'wt');


	if exist('EXE','var')==0
		% disp('EXE not given');
		% EXE = '$HOME/bin/fdtd64_2003';
		EXE = '$HOME/bin/fdtd';
		disp(['EXE not given. Using default: EXE=',EXE]);
	end

	if exist('WORKDIR','var')==0
		% disp('WORKDIR not given');
	    % WORKDIR = '$(dirname "$0")';
		%TODO: Is WORKDIR even necessary in the script? O.o
	    WORKDIR = '$JOBDIR';
		disp(['WORKDIR not given. Using default: WORKDIR=',WORKDIR]);
	end
	
	if exist('WALLTIME','var')==0
	    WALLTIME = 12;
		disp(['WALLTIME not given. Using default: WALLTIME=',WALLTIME]);
	end

	if exist('NODES','var')==0
	    NODES = 1;
		disp(['NODES not given. Using default: NODES=',NODES]);
	end

	if exist('PPN','var')==0
	    PPN = 4;
		disp(['PPN not given. Using default: PPN=',PPN]);
	end

	%write file
	fprintf(out,'#!/bin/bash\n');
	fprintf(out,'#\n');
	fprintf(out,'#PBS -l walltime=%d:00:00\n',WALLTIME);
	fprintf(out,'#PBS -mabe\n');
	fprintf(out,'#PBS -joe\n');
	fprintf(out,'#PBS -l nodes=%d:ppn=%d\n',NODES,PPN);
	fprintf(out,'#\n');
	fprintf(out,'\n');
	fprintf(out,'\n');
	fprintf(out,'export WORKDIR=%s\n',WORKDIR);
	fprintf(out,'export EXE=%s\n',EXE);
	fprintf(out,'\n');
	fprintf(out,'cd $WORKDIR\n');
	fprintf(out,'\n');
	fprintf(out,'$EXE %s.in > %s.out\n', BASENAME, BASENAME);

	%close file
	fclose(out);
	disp('...done')
end
