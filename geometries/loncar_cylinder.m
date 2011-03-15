function INFILENAME = loncar_cylinder(BASENAME, DSTDIR, ITERATIONS, print_holes_top, print_holes_bottom, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY)
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % description:
      %  function loncar_structure(BASENAME, DSTDIR, HOLE_TYPE, pillar_radius, EXCITATION_FREQUENCY, SNAPSHOTS_FREQUENCY)
      %  creates a Loncar type structure (cylinder with transverse circular holes)
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % Settings
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      print_mesh = true;
      print_holes = true;
      % print_holes_top = true;
      % print_holes_bottom = true;
      print_pillar = true;
      print_podium = true;
      print_freqsnap = true;
      print_timesnap = true;
      print_epssnap = true;
      print_excitation = true;
      print_probes = true;
      SNAPSHOTS_ON = 1;

      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % arguments
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      disp('Reading input parameters...');

      if exist('BASENAME','var')==0
              disp('BASENAME not given');
          BASENAME = 'loncar_structure';
      end
      
      if exist('DSTDIR','var')==0
              disp('DSTDIR not given');
          DSTDIR = uigetdir(getuserdir(),'DSTDIR');
      end
      if ~(exist(DSTDIR,'dir'))
              error(['dir ',DSTDIR,' not found']);
              return;
      end
      mkdir([DSTDIR,filesep,BASENAME]);

      %wavelength
      lambda = 637*10^-3;%mum

      if exist('print_holes_bottom','var')==0
              error('print_holes_bottom not given');
      end

      if exist('print_holes_top','var')==0
              error('print_holes_top not given');
      end
      
      if exist('EXCITATION_FREQUENCY','var')==0
              disp('EXCITATION_FREQUENCY not given');
              EXCITATION_FREQUENCY = get_c0()/lambda;
      end

      % pillar radius
      if exist('pillar_radius','var')==0
              disp('pillar_radius not given');
              pillar_radius = 2;%mum
      end
      
      if exist('HOLE_TYPE','var')==0
              disp('HOLE_TYPE not given');
              HOLE_TYPE=1;
      end
      
      % refractive indices
      n_Diamond = 2.4;%no unit
      n_Air = 1;%no unit
      n_bottom_square=3.5214;%no unit
      % distance between holes
      d_holes = lambda/(4*n_Diamond)+lambda/(4*n_Air);%mum
      % hole radius
      hole_radius_toto = (lambda/(4*n_Air))/2;%mum
      hole_radius_z = pillar_radius - (d_holes-2*hole_radius_toto);%mum
      % number of holes on bottom
      bottom_N = 6;%no unit
      % number of holes on top
      top_N = 3;%no unit
      % distance between 2 holes around cavity
      d_holes_cavity = lambda/n_Diamond + 2*hole_radius_toto;%mum
      Lcav = d_holes_cavity - d_holes; % mum
      % d_holes_cavity = Lcav + d_holes;
      % top box offset
      top_box_offset=1;%mum
      %bottom square thickness
      h_bottom_square=0.5;%mum
      
      % ITERATIONS = 261600;%no unit
      % ITERATIONS = 32000;%no unit
      % ITERATIONS = 10;%no unit
      TIMESTEP=0.9;%mus
      TIME_CONSTANT=4.000000E-09;%mus
      AMPLITUDE=1.000000E+01;%V/mum???
      TIME_OFFSET=2.700000E-08;%mus
              
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % additional calculations
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      
      % max mesh intervals
      delta_bottom_square = lambda/(10*n_bottom_square);
      delta_hole = lambda/(10*n_Air);
      delta_diamond = lambda/(10*n_Diamond);
      delta_outside = lambda/(4*n_Air);
      delta_center = lambda/(15*n_Diamond);
      delta_boundary = delta_diamond;
      
      % center area where excitation takes place (for meshing)
      center_radius = 4*delta_center;

      % buffers (area outside pillar where mesh is fine)
      x_buffer = 4*delta_diamond;%mum
      y_buffer = 32*delta_diamond;%mum
      z_buffer = 4*delta_diamond;%mum

      % dimension and position parameters
      Xmax = 2*(pillar_radius + 4*delta_diamond + 4*delta_outside);%mum
      pillar_height = (bottom_N+top_N)*d_holes + Lcav;
      totomax = h_bottom_square + pillar_height + y_buffer + top_box_offset;%mum
      Zmax = Xmax;%mum
      
      pillar_centre_X = Xmax/2;
      pillar_centre_toto = h_bottom_square + bottom_N*d_holes + Lcav/2;
      pillar_centre_Z = Zmax/2;

      % meshing parameters
      thicknessVector_toto = [ h_bottom_square ];
      max_delta_Vector_toto = [ delta_bottom_square ];
      for i=1:bottom_N
              thicknessVector_toto = [ thicknessVector_toto, d_holes/2 - hole_radius_toto, 2*hole_radius_toto, d_holes/2 - hole_radius_toto ];
              max_delta_Vector_toto = [ max_delta_Vector_toto, delta_diamond, delta_hole, delta_diamond ];
      end
      thicknessVector_toto = [ thicknessVector_toto, Lcav/2-center_radius, 2*center_radius, Lcav/2-center_radius ];
      max_delta_Vector_toto = [ max_delta_Vector_toto, delta_diamond, delta_center, delta_diamond ];
      for i=1:top_N
              thicknessVector_toto = [ thicknessVector_toto, d_holes/2 - hole_radius_toto, 2*hole_radius_toto, d_holes/2 - hole_radius_toto ];
              max_delta_Vector_toto = [ max_delta_Vector_toto, delta_diamond, delta_hole, delta_diamond ];
      end
      thicknessVector_toto = [ thicknessVector_toto, y_buffer, top_box_offset ];
      max_delta_Vector_toto = [ max_delta_Vector_toto, delta_boundary, delta_outside ];

      delta_min = min(max_delta_Vector_toto);

      thicknessVector_X = [ Xmax/2-pillar_radius-x_buffer, x_buffer, pillar_radius-center_radius, center_radius ];
      max_delta_Vector_X = [ delta_outside, delta_boundary, delta_diamond, delta_center ];

      if HOLE_TYPE == 1
        thicknessVector_Z_1 = [ Zmax/2-pillar_radius-z_buffer, z_buffer, pillar_radius-hole_radius_toto, hole_radius_toto-center_radius, center_radius ];
      elseif HOLE_TYPE == 2
        thicknessVector_Z_1 = [ Zmax/2-pillar_radius-z_buffer, z_buffer, pillar_radius-hole_radius_toto, hole_radius_toto-center_radius, center_radius ];
      else
        thicknessVector_Z_1 = [ Zmax/2-pillar_radius-z_buffer, z_buffer, pillar_radius-2*hole_radius_toto, 2*hole_radius_toto-center_radius, center_radius ];
      end

      thicknessVector_Z_2 = fliplr(thicknessVector_Z_1);
      thicknessVector_Z = [ thicknessVector_Z_1, thicknessVector_Z_2 ];
      max_delta_Vector_Z_1 = [ delta_outside, delta_boundary, delta_diamond, delta_hole, delta_center ];
      max_delta_Vector_Z_2 = fliplr(max_delta_Vector_Z_1);
      max_delta_Vector_Z = [ max_delta_Vector_Z_1, max_delta_Vector_Z_2 ];
      
      [ delta_X_vector, local_delta_X_vector ] = subGridMultiLayer(max_delta_Vector_X,thicknessVector_X);
      [ delta_toto_vector, local_delta_toto_vector ] = subGridMultiLayer(max_delta_Vector_toto,thicknessVector_toto);
      [ delta_Z_vector, local_delta_Z_vector ] = subGridMultiLayer(max_delta_Vector_Z,thicknessVector_Z);

      % for the frequency snapshots
      Xplanes = [ 0,
      Xmax/2-pillar_radius-x_buffer,
      Xmax/2-pillar_radius,
      Xmax/2-2*delta_center,
      Xmax/2-delta_center,
      Xmax/2 ];
      
      totoplanes = [ 0,
      h_bottom_square,
      h_bottom_square + bottom_N/2*d_holes,
      pillar_centre_toto-delta_center,
      pillar_centre_toto,
      pillar_centre_toto+delta_center,
      h_bottom_square + bottom_N*d_holes + Lcav + top_N/2*d_holes,
      h_bottom_square + pillar_height,
      h_bottom_square + pillar_height+1*delta_boundary,
      h_bottom_square + pillar_height+8*delta_boundary,
      h_bottom_square + pillar_height+32*delta_boundary,
      totomax ];
      
      Zplanes = [ 0,
      Zmax/2-pillar_radius-z_buffer,
      Zmax/2-pillar_radius,
      Zmax/2-hole_radius_toto,
      Zmax/2-2*delta_center,
      Zmax/2-delta_center,
      Zmax/2,
      Zmax/2+delta_center,
      Zmax/2+2*delta_center,
      Zmax/2+hole_radius_toto,
      Zmax/2+pillar_radius,
      Zmax/2+pillar_radius+z_buffer,
      Zmax ];
      
      % for probes
      probes_X_vector = Xplanes(2:4);
      probes_toto_vector = totoplanes(2:11);
      probes_Z_vector = Zplanes(2:8);
      
      probes_toto_vector_center = totoplanes(4:6);
      probes_Z_vector_center = [Zplanes(6),Zplanes(8)];
      
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % Files to generate:
      % .lst
      % .in
      % .sh
      % .cmd
      % .geo
      % .inp
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % .lst file
      %~ copyfile(fullfile(getuserdir(),'MATLAB','entity.lst'),[DSTDIR,filesep,BASENAME]);
      % .in file
      INFILENAME = [DSTDIR,filesep,BASENAME,filesep,BASENAME,'.in'];
      GEOin(INFILENAME, { [BASENAME,'.inp'],[BASENAME,'.geo'] });
      % .sh file
      %TODO: improve this
      % WORKDIR = ['$HOME/loncar_structure','/',BASENAME];
      GEOshellscript([DSTDIR,filesep,BASENAME,filesep,BASENAME], BASENAME, '$HOME/bin/fdtd', '$JOBDIR', 200, 1, 4);

      % .cmd file
      GEOcommand([DSTDIR,filesep,BASENAME,filesep,BASENAME], BASENAME);
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      % .geo file
      disp('Writing GEO file...');

      % open file
      out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.geo'],'wt');

      % write header
      fprintf(out,'**GEOMETRY FILE\n');
      fprintf(out,'\n');

      % initialize current y
      toto_current=0;

      if print_podium
          % create bottom block
          L = [ 0, 0, 0 ];
          U = [ toto_current + h_bottom_square, Xmax, Zmax ];
          GEOblock(out, L, U, n_bottom_square^2, 0);
      end

      toto_current = toto_current + h_bottom_square;
          
      if print_pillar
          % create main pillar
          L = [ toto_current, Xmax/2 - pillar_radius, Zmax/2 - pillar_radius ];
          U = [ toto_current + pillar_height, Xmax/2 + pillar_radius, Zmax/2 + pillar_radius ];
          GEOblock(out, L, U, n_Diamond^2, 0);
      end

      toto_current = toto_current + d_holes/2;

      if print_holes
          % hole settings
          permittivity = n_Air^2;
          conductivity = 0;
          
          % create bottom holes
          for i=1:bottom_N
          
              if print_holes_bottom
                  centre = [ toto_current, Xmax/2, Zmax/2 ];
                  if HOLE_TYPE == 1
                  GEOcylinder(out, centre, 0, hole_radius_toto, 2*pillar_radius, permittivity, conductivity, 0);
                  elseif HOLE_TYPE == 2
                  lower = [ toto_current - hole_radius_toto, Xmax/2 - pillar_radius, Zmax/2 - hole_radius_toto];
                  upper = [ toto_current + hole_radius_toto, Xmax/2 + pillar_radius, Zmax/2 + hole_radius_toto];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  else
                  lower = [ toto_current - hole_radius_toto, Xmax/2 - pillar_radius, Zmax/2 - hole_radius_z];
                  upper = [ toto_current + hole_radius_toto, Xmax/2 + pillar_radius, Zmax/2 + hole_radius_z];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  end
              end

              toto_current = toto_current + d_holes;
          end

          toto_current = toto_current - d_holes + d_holes_cavity;

          % create top holes
          for i=1:top_N
          
              if print_holes_top
                  centre = [ toto_current, Xmax/2, Zmax/2 ];
                  if HOLE_TYPE == 1
                  GEOcylinder(out, centre, 0, hole_radius_toto, 2*pillar_radius, permittivity, conductivity, 0);
                  elseif HOLE_TYPE == 2
                  lower = [ toto_current - hole_radius_toto, Xmax/2 - pillar_radius, Zmax/2 - hole_radius_toto];
                  upper = [ toto_current + hole_radius_toto, Xmax/2 + pillar_radius, Zmax/2 + hole_radius_toto];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  else
                  lower = [ toto_current - hole_radius_toto, Xmax/2 - pillar_radius, Zmax/2 - hole_radius_z];
                  upper = [ toto_current + hole_radius_toto, Xmax/2 + pillar_radius, Zmax/2 + hole_radius_z];
                  GEOblock(out, lower, upper, permittivity, conductivity);
                  end
              end
              
              toto_current = toto_current + d_holes;
          end
          
      end

          %write box
          L = [ 0, 0, 0 ];
          U = [ totomax, Xmax/2, Zmax ];
          GEObox(out, L, U);

          %write footer
          fprintf(out,'end\n'); %end the file

          %close file
          fclose(out);
          disp('...done');
          
          %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
          % .inp file
          disp('Writing INP file...');

          % open file
          out = fopen([DSTDIR,filesep,BASENAME,filesep,BASENAME,'.inp'],'wt');

      if print_excitation
          P_Xm = [ pillar_centre_toto, pillar_centre_X-2*delta_center, pillar_centre_Z ];
          P_Xp = [ pillar_centre_toto, pillar_centre_X+2*delta_center, pillar_centre_Z ];
          P_totom = [ pillar_centre_toto-2*delta_center, pillar_centre_X, pillar_centre_Z ];
          P_totop = [ pillar_centre_toto+2*delta_center, pillar_centre_X, pillar_centre_Z ];
          P_Zm = [ pillar_centre_toto, pillar_centre_X, pillar_centre_Z-2*delta_center ];
          P_Zp = [ pillar_centre_toto, pillar_centre_X, pillar_centre_Z+2*delta_center ];
          P_center = [ pillar_centre_toto, pillar_centre_X, pillar_centre_Z ];
          E = [ 0, 1, 0 ];
          H = [ 0, 0, 0 ];
          type = 10;
          
          GEOexcitation(out, 7, P_Xm, P_center, E, H, type, TIME_CONSTANT, AMPLITUDE, TIME_OFFSET, EXCITATION_FREQUENCY, 0, 0, 0, 0);
          
          end

          totopos_bc = 1; totopos_param = [1,1,0];
          Xpos_bc = 2; Xpos_param = [1,1,0];
          Zpos_bc = 2; Zpos_param = [1,1,0];
          totoneg_bc = 2; totoneg_param = [1,1,0];
          Xneg_bc = 2; Xneg_param = [1,1,0];
          Zneg_bc = 2; Zneg_param = [1,1,0];
          GEOboundary(out, Xpos_bc, Xpos_param, totopos_bc, totopos_param, Zpos_bc, Zpos_param, Xneg_bc, Xneg_param, totoneg_bc, totoneg_param, Zneg_bc, Zneg_param);
          
          iteration_method = 5;
          propagation_constant = 0;
          flag_1 = 0;
          flag_2 = 0;
          id_character = 'id';
          GEOflag(out, iteration_method, propagation_constant, flag_1, flag_2, ITERATIONS, TIMESTEP, id_character);

          if print_mesh
          GEOmesh(out, delta_toto_vector, delta_X_vector, delta_Z_vector);
      end
          
      % frequency snapshots
      first = ITERATIONS;
      repetition = ITERATIONS;
      interpolate = 1;
      real_dft = 0;
      mod_only = 0;
      mod_all = 1;
      starting_sample = 0;
      E=[1,1,1];
      H=[1,1,1];
      J=[0,0,0];
      power = 0;
          
      if SNAPSHOTS_ON == 1
              for iX = 1:length(Xplanes)
                      plane = 2;
                      P1 = [0, Xplanes(iX), 0];
                      P2 = [totomax, Xplanes(iX), Zmax];
                      GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
                      GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
              end
              for itoto = 1:length(totoplanes)
                      plane = 1;
                      P1 = [totoplanes(itoto), 0, 0];
                      P2 = [totoplanes(itoto), Xmax/2, Zmax];
                      GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
                      GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
              end
              for iZ = 1:length(Zplanes)
                      plane = 3;
                      P1 = [0, 0, Zplanes(iZ)];
                      P2 = [totomax, Xmax/2, Zplanes(iZ)];
                      GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, SNAPSHOTS_FREQUENCY, starting_sample, E, H, J);
                      GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0);
              end
      end

      if print_probes
          % probes
          step=10;
          E=[1,1,1];
          H=[1,1,1];
          J=[0,0,0];
          power = 0;
          for itoto =1:length(probes_toto_vector)
              % Xtoto probes
              for iX =1:length(probes_X_vector)
                  GEOprobe(out, [probes_toto_vector(itoto), probes_X_vector(iX), Zplanes(6)], step, E, H, J, power );
              end
              % Ztoto probes
              for iZ =1:length(probes_Z_vector)
                  GEOprobe(out, [probes_toto_vector(itoto), Xplanes(5), probes_Z_vector(iZ)], step, E, H, J, power );
              end
          end
          
          % Ztoto center probes
          for itoto =1:length(probes_toto_vector_center)
              for iZ =1:length(probes_Z_vector_center)
                  GEOprobe(out, [probes_toto_vector_center(itoto), Xplanes(4), probes_Z_vector_center(iZ)], step, E, H, J, power );
              end
          end
      end
      
      %write footer
      fprintf(out,'end\n'); %end the file

      %close file
      fclose(out);
      disp('...done');
end
