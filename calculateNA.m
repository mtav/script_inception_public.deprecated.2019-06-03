function NA = calculateNA(INP_FILE, PRN_FILE, center_offset)
	% calculates the numerical aperture
	% function NA = calculateNA(INP_FILE, PRN_FILE, center_offset)

	%arguments
	if exist('INP_FILE','var')==0
		disp('INP_FILE not given');
		[FileName,PathName] = uigetfile('*.inp','Select the INP file');
		INP_FILE = [PathName, filesep, FileName];
	end

	if ~(exist(INP_FILE,'file'))
		error( ['File not found: ',INP_FILE] );
		return;
	end

	if exist('PRN_FILE','var')==0
		disp('PRN_FILE not given');
		[FileName,PathName] = uigetfile('*.prn','Select the PRN file');
		PRN_FILE = [PathName, filesep, FileName];
	end

	if ~(exist(PRN_FILE,'file'))
		error( ['File not found: ',PRN_FILE] );
		return;
	end

	if exist('center_offset','var')==0
		disp('center_offset not given');
		center_offset = 1;
	end

	[ entries, structured_entries ] = GEO_INP_reader(INP_FILE);
	frequency = structured_entries.excitations(1).frequency;
	Nx = length(structured_entries.xmesh); % number of X cells in mesh
	Ny = length(structured_entries.ymesh); % number of Y cells in mesh
	Nz = length(structured_entries.zmesh); % number of Z cells in mesh
	
	x_index = (Nx-1)-center_offset; % we take the X line slightly off the middle
	if ( x_index<0 | x_index>Nx-1 )
		x_index
		Nx
		error('index out of range');
	end
	lambda = getC0()/frequency; % mum

	%read file
	[header, data_orig] = hdrload(PRN_FILE);

	% extract all lines starting with 1
	% mat = [1,2,3;,1,5,6;7,8,9;1,4,5]
	% ind = find(mat(:,1) == 1)
	% mat(ind,:)

	%take line at index x_index
	first = 1 + x_index*Nz;
	last = 1 + x_index*Nz + (Nz-1);
	Nx
	Ny
	Nz
	first
	last
	data = data_orig(first:last,:);

	% get columns
	x = data(:,1);
	z = data(:,2);
	Exmod = data(:,3);
	Exre = data(:,4);
	Exim = data(:,5);
	Eymod = data(:,6);
	Eyre = data(:,7);
	Eyim = data(:,8);
	Ezmod = data(:,9);
	Ezre = data(:,10);
	Ezim = data(:,11);
	Hxmod = data(:,12);
	Hxre = data(:,13);
	Hxim = data(:,14);
	Hymod = data(:,15);
	Hyre = data(:,16);
	Hyim = data(:,17);
	Hzmod = data(:,18);
	Hzre = data(:,19);
	Hzim = data(:,20);

	% power density 
	for n = 1:Nz
		powerXYZ(n,:) = sqrt(Exmod(n,1)^2+Eymod(n,1)^2+Ezmod(n,1)^2);
		powerX(n,:) = Exmod(n,1)^2;
		powerY(n,:) = Eymod(n,1)^2;
		powerZ(n,:) = Ezmod(n,1)^2;
		poynting(n,:) = 0.5*real((Exre(n,1)+i*Exim(n,1)).*conj(Hzre(n,1)+i*Hzim(n,1))-(Ezre(n,1)+i*Ezim(n,1)).*conj(Hxre(n,1)+i*Hxim(n,1)));
	end

	% plot(z,powerXYZ,z,powerX,z,powerY,z,powerZ),
	% xlabel('Z'),
	% ylabel('power'),
	% legend('powerXYZ','powerX','powerY','powerZ')

	% fit_input = poynting
	% fit_input = powerXYZ
	fit_input = powerX;

	%% fitting
	[sigma,mu,A] = mygaussfit(z,fit_input);
	fit_output = A*exp(-(z-mu).^2/(2*sigma^2));
	
	disp(['sigma = ',num2str(sigma)]);
	disp(['mu = ',num2str(mu)]);
	disp(['A = ',num2str(A)]);

	w0 = sqrt(4*sigma^2);
	disp(['w0 = ',num2str(w0)]);

	NA = lambda/(pi*w0);

	disp(['NA = ',num2str(NA)]);

	% plotting
	plot(z,fit_input);
	hold on;
	plot(z,fit_output,'.r');
	xlabel('Z (\mum)');
	ylabel('power (W*\mum^(-2))');
	legend('data','fit');
end
