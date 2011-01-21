function loncar_structure_wrapper(BASENAME, DSTDIR)
    ITERATIONS = [10,32000,261600];
    HOLE_TYPE = 3;
    pillar_radius = 1;
    
    function gen_loncar(N, print_holes_top, print_holes_bottom)
        filename = [ BASENAME, '_', num2str(N), '_', num2str(print_holes_top), '_', num2str(print_holes_bottom) ];
        for excitation_direction=1:12
            loncar_structure(filename, DSTDIR, N, excitation_direction, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius);
        end
    end
    
    for iter_index=1:length(ITERATIONS)
        N = ITERATIONS(iter_index);
        gen_loncar(N, true, true);
        gen_loncar(N, false, true);
        gen_loncar(N, true, false);
        gen_loncar(N, false, false);
    end
end
