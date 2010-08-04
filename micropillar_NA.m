function micropillar_NA(DIR)
	if exist('DIR','var')==0
		disp('DIR not given');
	    DIR = uigetdir(getuserdir(),'DIR');
	end
	if ~(exist(DIR,'dir'))
		error('dir not found');
	end
	
	[ folder, basename, ext ] = fileparts(DIR);
	
	INP_FILE = fullfile(DIR, [basename,'.inp']);
	if ~(exist(INP_FILE,'file'))
		error([INP_FILE, ' not found']);
	end
	
	INP_FILE
	
	[ entries, structured_entries ] = GEO_INP_reader(INP_FILE);
	Nx = 6;
	Ny = 12;
	Nz = 11;
	Nfs = length(structured_entries.frequency_snapshots)
	Nts = length(structured_entries.time_snapshots)
	
	% normal case:
	% Nfs = (Nx+Ny+Nz+6)*(Nfreq+1)
	% abnormal case:
	% Nfs = (Nx+Ny+Nz)*(Nfreq+1)+6*1
	% Nts = (Nx+Ny+Nz+6)
	
	% normal case:
	Nfreq = Nfs/(Nx+Ny+Nz+6)-1
	% abnormal case:
	% Nfreq = (Nfs-6)/(Nx+Ny+Nz)-1
	
	if Nfs ~= (Nx+Ny+Nz+6)*(Nfreq+1)
		error('Nfs incorrect');
	end
	
	if Nts ~= (Nx+Ny+Nz+6)
		error('Nts incorrect');
	end

	return;
	
	numID = 1;
	
	snap_plane = 'y';
	probe_ident = 'id';
	snap_time_number = 0;
	[ PRN_FILE, alphaID, pair ] = numID_to_alphaID(numID, snap_plane, probe_ident, snap_time_number)

	if ~(exist(PRN_FILE,'file'))
		error([PRN_FILE, ' not found']);
	end
	
	PRN_FILE
	
	NA = calculateNA(INP_FILE, PRN_FILE, 50)
	
end
