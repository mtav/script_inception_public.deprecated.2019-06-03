function BFDTDtoMEEP(geofile, inpfile)
	%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	% Written by Erman Engin, University of Bristol
	% 
	% NOTES:
	% The code might give errors if INP file has other sources than a Gaussian pulse
	% Only one field in the excitation component defined in INP should be one.
	% That is either Ex or Ey ... Hx...etc;  Otherwise the first nonzero
	% component will be translated to ctl.

	% PML Layer translation should be implemented using the data in
	% inpEntries.boundaries

	%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
	if exist('geofile','var') == 0
		disp('geofile not given');
		[GeoFileName,GeoPathName] = uigetfile('*.geo','Select GEO file',getuserdir());
		geofile=[GeoPathName,GeoFileName];
	end

	if exist(geofile,'file') ~= 2
		error(['file ', geofile, ' not found or not a file']);
		return;
	end

	[GeoPathName, GeoFileName_basename, ext] = fileparts(geofile);
	GeoFileName = [GeoFileName_basename, ext];
	
	if exist('inpfile','var') == 0
		disp('inpfile not given');
		[InpFileName,InpPathName] = uigetfile('*.inp','Select INP file',GeoPathName);
		inpfile=[InpPathName,InpFileName];
	end

	if exist(inpfile,'file') ~= 2
		error(['file ', inpfile, ' not found or not a file']);
		return;
	end
		
	[geoEntries]=GEO_INP_reader(geofile);
	[jj2,inpEntries]=GEO_INP_reader(inpfile);

	projectPath = [GeoPathName, filesep, 'ctlConversion'];
	mkdir(projectPath);
	filename = [projectPath, filesep, GeoFileName_basename, '.ctl'];
	fid = fopen(filename, 'w+');


	%% GEO FILE%
	for m=1:length(geoEntries)
		if strcmp(lower(geoEntries{m}.type),'box')
			data=geoEntries{m}.data;
			xl=data(1);
			yl=data(2);
			zl=data(3);
			xu=data(4);
			yu=data(5);
			zu=data(6);
		end
	end

	simSize=[xu-xl yu-yl zu-zl];
	geoCenter=simSize'/2;

	xmesh=inpEntries.xmesh; if ~length(xmesh); xmesh=-1; end
	ymesh=inpEntries.ymesh; if ~length(ymesh); ymesh=-1; end
	zmesh=inpEntries.zmesh; if ~length(zmesh); zmesh=-1; end

	dxyz=min([min(xmesh),min(ymesh),min(zmesh)]);
	resolution=1/dxyz;

	numSteps=inpEntries.flag.numSteps;
	fprintf(fid,'(set-param! resolution %2.6f )\r\n',resolution);
	fprintf(fid,['(set! geometry-lattice (make lattice (size ',num2str(simSize,'%2.5f '),')))\r\n\r\n;geometry specification\r\n(set! geometry\r\n(list\r\n']);
	fprintf(fid,'\r\n');

	for m=1:length(geoEntries)
	   type=geoEntries{m}.type;
	   data=geoEntries{m}.data;
	   
	   switch lower(type)
	   case 'block'
		   data(1:6)=data(1:6)-[geoCenter;geoCenter];
		   xl=data(1); yl=data(2);zl=data(3);xu=data(4);yu=data(5);zu=data(6);eps=data(7);
		   w=data(4)-data(1);h=data(5)-data(2);d=data(6)-data(3);
		   
		   text=meepBlock([xl+w/2,yl+h/2,zl+d/2],[w,h,d],eps);
		   fprintf(fid,text);
	   case 'cylinder'
		   data(1:3)=data(1:3)-geoCenter;
		   xc=data(1);yc=data(2);zc=data(3);ri=data(4);ro=data(5);h=data(6);eps=data(7);
		   
		   text=meepCylinder([xc,yc,zc],ro,h,[0 1 0],eps);
		   fprintf(fid,text);
	   case 'sphere'
		   data(1:3)=data(1:3)-geoCenter;
		   xc=data(1);yc=data(2);zc=data(3);ri=data(4);ro=data(5);h=data(6);eps=data(7);
		   
		   text=meepSphere([xc,yc,zc],ri,eps);
		   fprintf(fid,text);
	   end   
	end

	%% INP FILE

	% Excitations
	fields={'Ex','Ey','Ez','Hx','Hy','Hz'};
	for m=1:length(inpEntries.excitations)
		entry=inpEntries.excitations(m);
		excFrequency=entry.frequency/get_c0();
		excComponent=fields{find([entry.E,entry.H]==1)};
		excSize=abs(entry.P1-entry.P2);
		excCenter=(entry.P1+entry.P2)/2-geoCenter';
		excWidth=entry.time_constant*get_c0();
		fprintf(fid,[';;excitations specification\r\n(set! sources\r\n(list\r\n(make source\r\n(src (make gaussian-src (frequency ',num2str(excFrequency,'%2.7f'),') (width ',num2str(excWidth,'%2.7f'),')\r\n))\r\n(component ',excComponent,')\r\n(center ',num2str(excCenter,'%2.5f '),')\r\n(size ',num2str(excSize,'%2.5f '),'))\r\n)\r\n)\r\n']);

	end

	% PML Layers
	pmlThickness=0.3;
	fprintf(fid,';boundaries specification\r\n(set! pml-layers\r\n(list\r\n');

	fprintf(fid,['(make pml (direction X) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
	fprintf(fid,['(make pml (direction Y) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
	fprintf(fid,['(make pml (direction Z) (side Low) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
	fprintf(fid,['(make pml (direction X) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
	fprintf(fid,['(make pml (direction Y) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
	fprintf(fid,['(make pml (direction Z) (side High) (thickness ',num2str(pmlThickness,'%2.6f'),'))\r\n']);
	fprintf(fid,'))\r\n');

	%%%%%%%%%%%%%%%%%%%%%%
	
	abc=0;
	mag=0;
	elec=0;
	boundary_types=zeros(1,6);
	abc_pars=[8,2,0.001];

	fprintf(fid,'\r\n;boundaries specification\r\n');


	% Assign boundaries: 0 Mag, 1 Elec, 2 Absorbing (PML)
	for i=1:6
		if inpEntries.boundaries(i).type==10
			boundary_types(i)=2;
			if abc == 0
				abc_pars(0)=inpEntries.boundaries(1).p(1);
				abc_pars(1)=inpEntries.boundaries(2).p(2);
				abc_pars(2)=inpEntries.boundaries(3).p(3);
			end
			abc = abc + 1;
		elseif inpEntries.boundaries(i).type>1
			boundary_types(i)=2;
			abc = abc+1;
		elseif inpEntries.boundaries(i).type==0
			boundary_types(i)=0;
			mag = mag+1;
		elseif inpEntries.boundaries(i).type==1
			boundary_types(i)=1;
			elec = elec+1;
		end
	end
	
		% if (abc==6) {
			% of << "(set! pml-layers (list (make pml (thickness " << abc_pars[0]*(1/trans->resolution) << "))))\n";
		% }
		% else {
			% if (abc!=0) {
				% of << "(set! pml-layers\n";
				% of << "\t(list\n";
				% for (int i=0;i<6;++i) {
					% if (boundary_types[i]==2) {
						% of << "\t\t(make pml (direction ";
						% if ((i==0) || (i==3)) { of << "X"; }
						% if ((i==1) || (i==4)) { of << "Y"; }
						% if ((i==2) || (i==5)) { of << "Z"; }
						% of << ") (side ";
						% if (i<3) { of << "Low) (thickness "; }
						% if (i>2) { of << "High) (thickness "; }

						% for (int idx=0;idx<3;idx++) cout << "abc_pars["<<idx<<"] = " << abc_pars[idx] << endl;
						% cout << "trans->resolution = " << trans->resolution <<endl;
						% cout << "abc_pars[0]*(1/trans->resolution) = " << abc_pars[0]*(1/trans->resolution) << endl;

						% of << abc_pars[0]*(1/trans->resolution) << "))\n";

					% }
				% }
				% of << "\t))\n";
			% }

			fclose(fid);return;

			% if ((elec>0) || (mag>0)) {
				% of << "(init-fields)\n";
				% if (bpars_[0].type==0) { of << "(meep-fields-set-boundary fields Low X Magnetic)\n"; }
				% else if (bpars_[0].type==1) { of << "(meep-fields-set-boundary fields Low X Metallic)\n"; }
				% if (bpars_[1].type==0) { of << "(meep-fields-set-boundary fields Low Y Magnetic)\n"; }
				% else if (bpars_[1].type==1) { of << "(meep-fields-set-boundary fields Low Y Metallic)\n"; }
				% if (bpars_[2].type==0) { of << "(meep-fields-set-boundary fields Low Z Magnetic)\n"; }
				% else if (bpars_[2].type==1) { of << "(meep-fields-set-boundary fields Low Z Metallic)\n"; }
				% if (bpars_[3].type==0) { of << "(meep-fields-set-boundary fields High X Magnetic)\n"; }
				% else if (bpars_[3].type==1) { of << "(meep-fields-set-boundary fields High X Metallic)\n"; }
				% if (bpars_[4].type==0) { of << "(meep-fields-set-boundary fields High Y Magnetic)\n"; }
				% else if (bpars_[4].type==1) { of << "(meep-fields-set-boundary fields High Y Metallic)\n"; }
				% if (bpars_[5].type==0) { of << "(meep-fields-set-boundary fields High Z Magnetic)\n"; }
				% else if (bpars_[5].type==1) { of << "(meep-fields-set-boundary fields High Z Metallic)\n"; }
			% }
		% }

		% cout << "===> print_boundaries done" << endl;

	%%%%%%%%%%%%%%%%%%%%%%
	
	% Run Command
	fprintf(fid,'(init-fields)\r\n');
	runUntil=2*dxyz*numSteps;
	fprintf(fid,['(run-until ',num2str(runUntil),'\r\n']);
	fprintf(fid,'(at-beginning output-epsilon)\r\n');
	for m=1:length(inpEntries.all_snapshots)
		entry=inpEntries.all_snapshots(m);
		sliceCenter=(entry.P1+entry.P2)/2-geoCenter';
		sliceSize=abs(entry.P1-entry.P2);
		atEverySlice=2*dxyz*entry.repetition;
		fprintf(fid,sprintf('(to-appended "Slice%i"\r\n(at-every %2.4g\r\n(in-volume (volume (center %f %f %f) (size %f %f %f))\r\noutput-efield-x)))\r\n',m,atEverySlice,sliceCenter,sliceSize));
		fprintf(fid,'\r\n');
	end
	fprintf(fid,')\r\n');


	fclose(fid);
	
	disp(['Created ', filename]);
end
