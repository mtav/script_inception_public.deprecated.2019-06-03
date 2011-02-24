function loncar_structure_wrapper(BASENAME, DSTDIR)
    ITERATIONS = [10,32000,261600];
    HOLE_TYPE = 3;
    pillar_radius = 1;
    
    lambda = 637*10^-3;%mum
    EXCITATION_FREQUENCY = get_c0()/lambda;

    lambda_res = 634.7730;

    SNAPSHOTS_FREQUENCY = [ get_c0()/lambda_res ];
    
    function gen_loncar(N, print_holes_top, print_holes_bottom)
        % for excitation_direction=1:12
        filename = [ BASENAME, '_', num2str(N), '_', num2str(print_holes_top), '_', num2str(print_holes_bottom) ];
        loncar_structure(filename, DSTDIR, N, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY);
        % BASENAME, DSTDIR, ITERATIONS, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY
        % end
    end
    
    for iter_index=1:length(ITERATIONS)
        N = ITERATIONS(iter_index);
        gen_loncar(N, true, true);
        gen_loncar(N, false, true);
        gen_loncar(N, true, false);
        gen_loncar(N, false, false);
    end
end
