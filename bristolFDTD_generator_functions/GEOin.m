function GEOin(filename, BASENAME)
    %TODO: input should be a list of files instead of just BASENAME

	%IN file generation
	disp('Writing IN file...');

	%open file
	out = fopen(strcat(filename,'.in'),'wt');

	%write file
	fprintf(out,'%s\n',BASENAME);
	fprintf(out,'%s\n',BASENAME);

	%close file
	fclose(out);
	disp('...done');
end
