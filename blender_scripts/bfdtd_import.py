#!BPY

"""
Name: 'Bristol FDTD (*.geo)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from Bristol FDTD'
"""

import Blender;
import bpy;
import BPyAddMesh;
import math;
import os;

Vector = Blender.Mathutils.Vector;
Matrix = Blender.Mathutils.Matrix;

# prepare base materials
material_dict={};
frequency_snapshot_material = Blender.Material.New('frequency_snapshot');
frequency_snapshot_material.rgbCol = 0.5, 0, 0;
time_snapshot_material = Blender.Material.New('time_snapshot');
time_snapshot_material.rgbCol = 0.5, 1, 0;
eps_snapshot_material = Blender.Material.New('eps_snapshot');
eps_snapshot_material.rgbCol = 0.5, 0, 1;
excitation_material = Blender.Material.New('excitation');
excitation_material.rgbCol = 1, 0, 0;
snapshot_materials = [ frequency_snapshot_material, time_snapshot_material, eps_snapshot_material ];

def materials(permittivity, conductivity):
    if permittivity not in material_dict:
        n = math.sqrt(permittivity)
        
        permittivity_material = Blender.Material.New('permittivity');
        permittivity_material.rgbCol = 0, permittivity/100.0, 1.0-permittivity/100.0;

        # conductivity_material = Blender.Material.New('conductivity')
        # conductivity_material.rgbCol = 0, 1.0-conductivity/100.0, 0;

        # refractive_index_material = Blender.Material.New('refractive_index')
        # if n!=0:
            # refractive_index_material.rgbCol = 0, 0, 1.0/n;
        # else:
            # refractive_index_material.rgbCol = 0, 0, 1.0;
            
        material_dict[permittivity] = permittivity_material;

    return [ material_dict[permittivity] ];

def GEOblock(lower, upper, permittivity, conductivity):
    scene = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cube(1.0);
    mesh.materials = materials(permittivity, conductivity);
    for f in mesh.faces:
        f.mat = 0;

    obj = scene.objects.new(mesh, 'block');
    pos = 0.5*(lower+upper);
    diag = upper-lower;
    obj.SizeX = abs(diag[0]);
    obj.SizeY = abs(diag[1]);
    obj.SizeZ = abs(diag[2]);
    obj.setLocation(pos[0], pos[1], pos[2]);
    return

def GEObox(lower, upper):
    scene = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cube(1.0);
    mesh.faces.delete(0, range(len(mesh.faces)));

    obj = scene.objects.new(mesh, 'box');
    pos = 0.5*(lower+upper);
    diag = upper-lower;
    obj.SizeX = abs(diag[0]);
    obj.SizeY = abs(diag[1]);
    obj.SizeZ = abs(diag[2]);
    obj.setLocation(pos[0], pos[1], pos[2]);
    return
    
def GEOcylinder(centre, R1, R2, H, permittivity, conductivity, angle):
    scene = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cylinder(32, 2*R2, H);
    mesh.materials = materials(permittivity, conductivity);
    for f in mesh.faces:
        f.mat = 0;

    obj = scene.objects.new(mesh, 'cylinder');
    obj.setLocation(centre[0], centre[1], centre[2]);
    obj.RotX = math.radians(-90); # because FDTD cylinders are aligned with the Y axis by default
    obj.RotY = 0;
    obj.RotZ = math.radians(angle);
    return

def GEOsphere(center, outer_radius, inner_radius, permittivity, conductivity):
    scene = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Icosphere(2, 2*outer_radius);
    mesh.materials = materials(permittivity, conductivity);
    for f in mesh.faces:
        f.mat = 0;

    obj = scene.objects.new(mesh, 'sphere');
    obj.setLocation(center[0], center[1], center[2]);
    return
    
def grid_index(Nx, Ny, Nz, i, j, k):
    return (Ny*Nz*i + Nz*j + k);
    
def GEOmesh(delta_X_vector, delta_Y_vector, delta_Z_vector):
    verts = [];
    edges = [];
    faces = [];
    
    Nx = len(delta_X_vector)+1;
    Ny = len(delta_Y_vector)+1;
    Nz = len(delta_Z_vector)+1;
    
    x=0;
    y=0;
    z=0;
    for i in range(Nx):
        if i>0:
            x+=delta_X_vector[i-1];
        y=0;
        for j in range(Ny):
            if j>0:
                y+=delta_Y_vector[j-1];
            z=0;
            for k in range(Nz):
                if k>0:
                    z+=delta_Z_vector[k-1];
                # print i, j, k, '->', x, y, z;
                verts.append(Vector(x, y, z));
    
    for i in range(Nx):
        for j in range(Ny):
            A = grid_index(Nx, Ny, Nz, i, j, 0);
            B = grid_index(Nx, Ny, Nz, i, j, Nz-1);
            edges.append([A, B]);

    for j in range(Ny):
        for k in range(Nz):
            A = grid_index(Nx, Ny, Nz, 0, j, k);
            B = grid_index(Nx, Ny, Nz, Nx-1, j, k);
            edges.append([A, B]);

    for k in range(Nz):
        for i in range(Nx):
            A = grid_index(Nx, Ny, Nz, i, 0, k);
            B = grid_index(Nx, Ny, Nz, i, Ny-1, k);
            edges.append([A, B]);
    
    BPyAddMesh.add_mesh_simple('mesh', verts, edges, faces);
    # print 'Nverts=', len(verts);
    # print 'Nverts=', Nx*Ny*Nz;

    # print 'Nedges=', len(edges);
    # print 'Nedges=', Nx*Ny + Ny*Nz+Nz*Nx;

    return
    
def Orthogonal(vec):
    xx = abs(vec.x);
    yy = abs(vec.y);
    zz = abs(vec.z);
    if (xx < yy):
        if xx < zz:
            return Vector(0,vec.z,-vec.y);
        else:
            return Vector(vec.y,-vec.x,0);
    else:
        if yy < zz:
            return Vector(-vec.z,0,vec.x)
        else:
            return Vector(vec.y,-vec.x,0);

def GEOexcitation(P1, P2):
    # arrow dimensions:
    arrow_length = (P2-P1).length;
    cone_length = arrow_length/5.0;
    cylinder_length = 4*cone_length;
    cone_radius = arrow_length/20.0;
    cylinder_radius = cone_radius/2.0;
    cylinder_center = P1+2./5.*(P2-P1);
    cone_center = P1+4.5/5.*(P2-P1);
        
    axisZ = -(P2-P1); # because the default primitive cone is oriented along -Z, unlike the one imported from Blender UI...
    axisX = Orthogonal(axisZ);
    axisY = axisZ.cross(axisX);
    axisX.normalize();
    axisY.normalize();
    axisZ.normalize();
    rotmat = Matrix(axisX,axisY,axisZ);
    
    scene = Blender.Scene.GetCurrent();
    
    mesh = Blender.Mesh.Primitives.Cylinder(32, 2*cylinder_radius, cylinder_length);
    mesh.materials = [ excitation_material ];
    for f in mesh.faces:
        f.mat = 0;

    arrow_cylinder_obj = scene.objects.new(mesh, 'excitation');
    arrow_cylinder_obj.setMatrix(rotmat);
    arrow_cylinder_obj.setLocation(cylinder_center[0], cylinder_center[1], cylinder_center[2]);

    mesh = Blender.Mesh.Primitives.Cone(32, 2*cone_radius, cone_length);
    mesh.materials = [ excitation_material ];
    for f in mesh.faces:
        f.mat = 0;

    arrow_cone_obj = scene.objects.new(mesh, 'arrow_cone');
    arrow_cone_obj.setMatrix(rotmat);

    arrow_cone_obj.setLocation(cone_center[0], cone_center[1], cone_center[2]);

    arrow_cylinder_obj.join([arrow_cone_obj]);
    scene.unlink(arrow_cone_obj);
    
    return

def snapshot(plane, P1, P2, snapshot_type):
    # print "snapshot 2 called"

    verts = [];
    if plane == 1:
        #X
        A = Vector(0.5*(P1[0]+P2[0]), P1[1], P1[2]);
        B = Vector(0.5*(P1[0]+P2[0]), P2[1], P1[2]);
        C = Vector(0.5*(P1[0]+P2[0]), P2[1], P2[2]);
        D = Vector(0.5*(P1[0]+P2[0]), P1[1], P2[2]);
        verts = [ A, B, C, D ];
    elif plane == 2:
        #Y        
        A = Vector(P1[0], 0.5*(P1[1]+P2[1]), P1[2]);
        B = Vector(P1[0], 0.5*(P1[1]+P2[1]), P2[2]);
        C = Vector(P2[0], 0.5*(P1[1]+P2[1]), P2[2]);
        D = Vector(P2[0], 0.5*(P1[1]+P2[1]), P1[2]);
        verts = [ A, B, C, D ];
    else:
        #Z
        A = Vector(P1[0], P1[1], 0.5*(P1[2]+P2[2]));
        B = Vector(P2[0], P1[1], 0.5*(P1[2]+P2[2]));
        C = Vector(P2[0], P2[1], 0.5*(P1[2]+P2[2]));
        D = Vector(P1[0], P2[1], 0.5*(P1[2]+P2[2]));
        verts = [ A, B, C, D ];
    
    edges = [];
    faces = [ 0, 1, 2, 3 ];
    name = 'snapshot';
    if snapshot_type == 0:
        name = 'freq_snapshot';
    elif snapshot_type == 1:
        name = 'time_snapshot';
    else:
        name = 'eps_snapshot';
    
    # print "Adding plane at ", A, B, C, D;
    BPyAddMesh.add_mesh_simple(name, verts, edges, faces);
    obj = Blender.Object.GetSelected()[0];
    mesh = Blender.Mesh.Get( obj.data.name );
    mesh.materials = snapshot_materials;
    for f in mesh.faces:
        f.mat = snapshot_type;

def GEOfrequency_snapshot(plane, P1, P2):
    snapshot(plane, P1, P2, 0);
    return
    
def GEOtime_snapshot(plane, P1, P2):
    snapshot(plane, P1, P2, 1);
    return

def GEOeps_snapshot(plane, P1, P2):
    snapshot(plane, P1, P2, 2);
    return

def GEOprobe(position):
    scene = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cube(0.1);

    obj = scene.objects.new(mesh, 'probe');
    obj.setLocation(position[0], position[1], position[2]);
    return

def TestObjects():
    GEOmesh([1, 1], [1, 2, 3], [4, 3, 2, 1]);
    
    GEOexcitation(Vector(0,0,0), Vector(1,0,0));
    GEOexcitation(Vector(0,0,0), Vector(0,1,0));
    GEOexcitation(Vector(0,0,0), Vector(0,0,1));

    GEOexcitation(Vector(1,0,0), Vector(2,0,0));
    GEOexcitation(Vector(0,1,0), Vector(0,2,0));
    GEOexcitation(Vector(0,0,1), Vector(0,0,2));

    GEOexcitation(Vector(0,0,0), Vector(1,1,1));
    GEOexcitation(Vector(1,1,1), Vector(2,2,2));
    GEOexcitation(Vector(2,2,2), Vector(3,3,3));

    GEOexcitation(Vector(1,1,1), Vector(2,1,2));
    GEOexcitation(Vector(2,1,2), Vector(2,2,3));
    GEOexcitation(Vector(2,2,3), Vector(1,2,4));

    # The death spiral!
    # x1=0;y1=0;z1=0;
    # x2=0;y2=0;z2=0;
    # for i in range(10*36):
        # x2=math.cos(math.radians(10*i));
        # y2=math.sin(math.radians(10*i));
        # z2=(10.*i)/360.;
        # GEOexcitation(Vector(x1,y1,z1), Vector(x2,y2,z2));
        # x1=x2;y1=y2;z1=z2;

    GEOfrequency_snapshot(1, Vector(-1, -1, -1), Vector(1, 1, 1));
    GEOfrequency_snapshot(2, Vector(-1, -1, -1), Vector(1, 1, 1));
    GEOfrequency_snapshot(3, Vector(-1, -1, -1), Vector(1, 1, 1));

    GEOtime_snapshot(1, Vector(2, -1, -1), Vector(4, 1, 1));
    GEOtime_snapshot(2, Vector(2, -1, -1), Vector(4, 1, 1));
    GEOtime_snapshot(3, Vector(2, -1, -1), Vector(4, 1, 1));

    GEOeps_snapshot(1, Vector(5, -1, -1), Vector(7, 1, 1));
    GEOeps_snapshot(2, Vector(5, -1, -1), Vector(7, 1, 1));
    GEOeps_snapshot(3, Vector(5, -1, -1), Vector(7, 1, 1));

    GEOfrequency_snapshot(1, Vector(-1, -1, -1), Vector(-1, 1, 1));
    GEOfrequency_snapshot(2, Vector(-1, -1, -1), Vector(1, -1, 1));
    GEOfrequency_snapshot(3, Vector(-1, -1, -1), Vector(1, 1, -1));

    GEOtime_snapshot(1, Vector(2, -1, -1), Vector(2, 1, 1));
    GEOtime_snapshot(2, Vector(2, -1, -1), Vector(4, -1, 1));
    GEOtime_snapshot(3, Vector(2, -1, -1), Vector(4, 1, -1));

    GEOeps_snapshot(1, Vector(5, -1, -1), Vector(5, 1, 1));
    GEOeps_snapshot(2, Vector(5, -1, -1), Vector(7, -1, 1));
    GEOeps_snapshot(3, Vector(5, -1, -1), Vector(7, 1, -1));

    for i in range(11):
        GEOblock(Vector(0, 0, i), Vector(1, 1, i+1), 10*i, 0);
        GEObox(Vector(1, 1, i), Vector(2, 2, i+1));
        GEOblock(Vector(2, 2, i), Vector(3, 3, i+1), 10*i, 100);
        GEOcylinder(Vector(3.5, 3.5, i+0.5), 0, 0.5, 1, 100-10*i, 200, 0);
        GEOcylinder(Vector(4.5, 4.5, i+0.5), 0, 0.5, 1, 10*i, 200, 45);
        GEOsphere(Vector(5.5, 5.5, i+0.5), 0.5, 0, i, 0);
        GEOprobe(Vector(0, 0, i));

def read_input_file(filename):
    print 'Processing ', filename;
    box_read=False;
    xmesh_read=False;
    
    # open file
    input = open(filename);
    # read the whole file as one string
    fulltext = input.read();

    # remove comments
	pattern_stripcomments = '\*\*.*$';
	cleantext =  regexprep(fulltext, pattern_stripcomments, '\n', 'lineanchors', 'dotexceptnewline', 'warnings');

    # close file
    input.close();

	# extract blocks
	pattern_blocks = '^(?<type>\w+).*?\{(?<data>[^\{\}]*?)\}';
	[tokens_blocks match_blocks names_blocks] =  regexp(cleantext, pattern_blocks, 'tokens', 'match', 'names', 'lineanchors', 'warnings');

	time_snapshots=struct('first',{},'repetition',{},'plane',{},'P1',{},'P2',{},'E',{},'H',{},'J',{},'power',{});
	frequency_snapshots=struct('first',{},'repetition',{},'interpolate',{},'real_dft',{},'mod_only',{},'mod_all',{},'plane',{},'P1',{},'P2',{},'frequency',{},'starting_sample',{},'E',{},'H',{},'J',{});
	all_snapshots=struct('first',{},'repetition',{},'interpolate',{},'real_dft',{},'mod_only',{},'mod_all',{},'plane',{},'P1',{},'P2',{},'frequency',{},'starting_sample',{},'E',{},'H',{},'J',{},'power',{});
	excitations=struct('current_source',{},'P1',{},'P2',{},'E',{},'H',{},'type',{},'time_constant',{},'amplitude',{},'time_offset',{},'frequency',{},'param1',{},'param2',{},'param3',{},'param4',{});
	boundaries=struct('type',{},'p',{});
	
	xmesh = [];
	ymesh = [];
	zmesh = [];
    flag=[];
    boundaries=[];

	entries={};
	# process blocks
	for i=1:length(names_blocks)

		type = names_blocks(:,i).type;
		data = names_blocks(:,i).data;
		# disp(['===>type=',type]);

		dataV=[];
		# remove empty lines
		lines = strread(data,'%s','delimiter','\r');
		cellFlag=0;
		for L=1:length(lines)
			if ~length(lines{L})
				continue;
			end

			dd=str2num(lines{L});

			if cellFlag
				if length(dd)  %% dd is num
					dataV{length(dataV)+1}=dd;
				else           %% dd is not num
					dataV{length(dataV)+1}=lines{L};
				end
			else
			   if length(dd)  %% dd is num
					dataV=[dataV,dd];
				else           %% dd is not num
					cellFlag=1;
					dataV=num2cell(dataV);
					dataV{length(dataV)+1}=lines{L};
				end
			end
		end % end of loop through lines

		entry.type=type;
		entry.data=dataV';
		entries{length(entries)+1}=entry;

		switch upper(entry.type)
			case {'FREQUENCY_SNAPSHOT','SNAPSHOT'}
				snapshot = add_snapshot(entry);
				all_snapshots = [ all_snapshots snapshot ];
				if strcmpi(entry.type,'FREQUENCY_SNAPSHOT')
					snapshot = add_frequency_snapshot(entry);
					frequency_snapshots = [ frequency_snapshots snapshot ];
				elseif strcmpi(entry.type,'SNAPSHOT')
					snapshot = add_time_snapshot(entry);
					time_snapshots = [ time_snapshots snapshot ];                    
				else
					error('Sense, it makes none.');
				end
			case {'EXCITATION'}
				current_excitation = add_excitation(entry);
				excitations = [ excitations current_excitation ];
			case {'XMESH'}
				xmesh = entry.data;
			case {'YMESH'}
				ymesh = entry.data;
			case {'ZMESH'}
				zmesh = entry.data;
            case {'FLAG'}
				flag = add_flag(entry);
            case {'BOUNDARY'}
                boundaries = add_boundary(entry);
			otherwise
				% disp('Unknown type.');
		end # end of switch

	end #end of loop through blocks

	structured_entries.all_snapshots = all_snapshots;
	structured_entries.time_snapshots = time_snapshots;
	structured_entries.frequency_snapshots = frequency_snapshots;
	structured_entries.excitations = excitations;
	structured_entries.xmesh = xmesh;
	structured_entries.ymesh = ymesh;
	structured_entries.zmesh = zmesh;
    structured_entries.flag=flag;
    structured_entries.boundaries=boundaries;

end % end of function

    
    return [ xmesh_read, box_read ];

def getname(filename, default_extension):
    
    extension = getExtension(filename);
    if extension == 'geo' or extension == 'inp':
        return filename;
    else:
        return filename + '.' + default_extension;
    
def read_inputs(filename):

    box_read=False;
    xmesh_read=False;
    
    f=open(filename, 'r');
    for line in f:
        subfile = os.path.join(os.path.dirname(filename),line.strip());
        if (not xmesh_read):
            subfile = getname(subfile,'inp');
        else:
            subfile = getname(subfile,'geo');
        [ xmesh_read, box_read ] = read_input_file(subfile);
    f.close();
    if (not xmesh_read):
        print 'WARNING: mesh not found';
    if (not box_read):
        print 'WARNING: box not found';
    
def getExtension(filename):
    return filename.split(".")[-1];
    
def readBristolFDTD(filename):
    # should read .in (=>.inp+.geo), .geo or .inp
    extension = getExtension(filename);
    if extension == 'in':
        print '.in file detected';
        read_inputs(filename);
    elif extension == 'inp':
        print '.inp file detected';
        read_input_file(filename);
    elif extension == 'geo':
        print '.geo file detected';
        read_input_file(filename);
    elif extension == 'prn':
        print '.prn file detected: Not supported yet';
    else:
        print 'Unknown file format:', extension;
    
    # extList = ["swf", "html", "exe"]
    # filename = "python.exe"
    # splitFilename = 
    # if filename.split(".")[-1] == '.in'in extList: return True
    # else: return False

    # in_file = file(filename, "r");
    # line = in_file.readline();

    # Nobjects = int(line)
    # #print "Nobjects=", Nobjects
    # object_names = []
    # for i in range(0, Nobjects):
        # line = in_file.readline()
        # object_names.append(line.strip())

    # in_file.close()
    
print '----->Importing bristol FDTD geometry...';
Blender.Window.WaitCursor(1);
# Blender.Window.FileSelector(readBristolFDTD, "Import", Blender.sys.makename(path='H:\\DATA\\foo',ext='.in'));

# readBristolFDTD('rotated_cylinder.in');
# getname('tettte.in','.in');
readBristolFDTD('H:\\DATA\\rotated_cylinder\\rotated_cylinder.in');
# readBristolFDTD('H:\\DATA\\rotated_cylinder\\rotated_cylinder.inp');
# readBristolFDTD('H:\\DATA\\rotated_cylinder\\rotated_cylinder.geo');

# TestObjects();

scene = Blender.Scene.GetCurrent();
scene.update(0);
Blender.Window.RedrawAll();
Blender.Window.WaitCursor(0);
print '...done';
