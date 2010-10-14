function writeBFDTD(DSTDIR, BASENAME, structured_entries)
	%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % writes out BFDTD files based on structured_entries input
	%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    if exist('BASENAME','var')==0
		disp('BASENAME not given');
	    BASENAME = 'unknown';
	end
	
	if exist('DSTDIR','var')==0
		disp('DSTDIR not given');
	    DSTDIR = uigetdir('H:\DATA','DSTDIR');
	end
	if ~(exist(DSTDIR,'dir'))
		error(['dir ',DSTDIR,' not found']);
	end
	mkdir([DSTDIR,filesep,BASENAME]);

    disp('----->Writing bristol FDTD files...');

    % structured_entries = 

              % all_snapshots: [1x3 struct]
             % time_snapshots: [1x2 struct]
        % frequency_snapshots: [1x1 struct]
                % excitations: [1x1 struct]
                      % xmesh: [4x1 double]
                      % ymesh: [3x1 double]
                      % zmesh: [2x1 double]
                       % flag: [1x1 struct]
                 % boundaries: [1x6 struct]
    
    
    % .geo file
	disp('Writing GEO file...');
	out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.geo'],'wt');

    % .inp file
	disp('Writing INP file...');
	out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.inp'],'wt');

    % .in file
	disp('Writing IN file...');
	out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'],'wt');

    % Box
    GEObox(structured_entries.box.lower, structured_entries.box.upper);
    % Mesh
    GEOmesh(structured_entries.xmesh,structured_entries.ymesh,structured_entries.zmesh);

    % Flag
    % structured_entries.flag;
    % Boundaries
    % structured_entries.boundaries;
    
    % Time_snapshot (time or EPS)
    for idx=1:length(structured_entries.time_snapshots)
        time_snapshot = structured_entries.time_snapshots(idx);
        if time_snapshot.eps == 0
            GEOtime_snapshot(time_snapshot.plane, time_snapshot.P1, time_snapshot.P2);
        else
            GEOeps_snapshot(time_snapshot.plane, time_snapshot.P1, time_snapshot.P2);
        end
    end
    
    % Frequency_snapshot
    for idx=1:length(structured_entries.frequency_snapshots)
        frequency_snapshot = structured_entries.frequency_snapshots(idx);
        GEOfrequency_snapshot(frequency_snapshot.plane, frequency_snapshot.P1, frequency_snapshot.P2);
    end

    % Excitation
    for idx=1:length(structured_entries.excitations)
        excitation = structured_entries.excitations(idx);
        GEOexcitation(excitation.P1, excitation.P2);
    end
    
    % Probe
    for idx=1:length(structured_entries.probe_list)
        probe = structured_entries.probe_list(idx);
        GEOprobe(probe.position);
    end
    
    % Sphere
    for idx=1:length(structured_entries.sphere_list)
        sphere = structured_entries.sphere_list(idx);
        GEOsphere(sphere.center, sphere.R1, sphere.R2, sphere.permittivity, sphere.conductivity);
    end
    
    % Block
    for idx=1:length(structured_entries.block_list)
        block = structured_entries.block_list(idx);
        GEOblock(block.lower, block.upper, block.permittivity, block.conductivity);
    end
    
    % Cylinder
    for idx=1:length(structured_entries.cylinder_list)
        cylinder = structured_entries.cylinder_list(idx);
        GEOcylinder(cylinder.center,cylinder.R1,cylinder.R2,cylinder.height,cylinder.permittivity,cylinder.conductivity,cylinder.angle);
    end

    % Rotation
    for idx=1:length(structured_entries.rotation_list)
        rotation = structured_entries.rotation_list(idx);
    end

    disp('...done');

end
