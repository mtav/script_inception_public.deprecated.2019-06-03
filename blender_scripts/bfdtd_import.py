#!BPY

"""
Name: 'Bristol FDTD (*.geo)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from Bristol FDTD'
"""

import Blender
import bpy
import BPyAddMesh
import math

Vector = Blender.Mathutils.Vector;
Matrix = Blender.Mathutils.Matrix;

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
    sc = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cube(1.0);
    mesh.materials = materials(permittivity, conductivity);
    for f in mesh.faces:
        f.mat = 0;

    obj = sc.objects.new(mesh, 'block');
    pos = 0.5*(lower+upper);
    diag = upper-lower;
    obj.SizeX = abs(diag[0]);
    obj.SizeY = abs(diag[1]);
    obj.SizeZ = abs(diag[2]);
    obj.setLocation(pos[0], pos[1], pos[2]);
    return

def GEObox(lower, upper):
    sc = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cube(1.0);
    mesh.faces.delete(0, range(len(mesh.faces)));

    obj = sc.objects.new(mesh, 'box');
    pos = 0.5*(lower+upper);
    diag = upper-lower;
    obj.SizeX = abs(diag[0]);
    obj.SizeY = abs(diag[1]);
    obj.SizeZ = abs(diag[2]);
    obj.setLocation(pos[0], pos[1], pos[2]);
    return
    
def GEOcylinder(centre, R1, R2, H, permittivity, conductivity, angle):
    sc = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cylinder(32, 2*R2, H);
    mesh.materials = materials(permittivity, conductivity);
    for f in mesh.faces:
        f.mat = 0;

    obj = sc.objects.new(mesh, 'cylinder');
    obj.setLocation(centre[0], centre[1], centre[2]);
    obj.RotX = math.radians(-90); # because FDTD cylinders are aligned with the Y axis by default
    obj.RotY = 0;
    obj.RotZ = math.radians(angle);
    return

def GEOsphere(center, outer_radius, inner_radius, permittivity, conductivity):
    sc = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Icosphere(2, 2*outer_radius);
    mesh.materials = materials(permittivity, conductivity);
    for f in mesh.faces:
        f.mat = 0;

    obj = sc.objects.new(mesh, 'sphere');
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
                print i, j, k, '->', x, y, z;
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
        
    # edges.append([0, 1]);
    # faces.append([0, 1, 2, 3]);

    BPyAddMesh.add_mesh_simple('mesh', verts, edges, faces);
    print 'Nverts=', len(verts);
    print 'Nverts=', Nx*Ny*Nz;

    print 'Nedges=', len(edges);
    print 'Nedges=', Nx*Ny + Ny*Nz+Nz*Nx;

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
    # BPy_Mesh  	Cone(verts, diameter, length)
    # Construct a conic mesh (ends filled).
    # BPy_Mesh  	Cylinder(verts, diameter, length)
    # Construct a cylindrical mesh (ends filled).
    
    # arrow dimensions:
    arrow_length = (P2-P1).length;
    cone_length = arrow_length/5.0;
    cylinder_length = 4*cone_length;
    cone_radius = arrow_length/20.0;
    cylinder_radius = cone_radius/2.0;
    cylinder_center = P1+2./5.*(P2-P1);
    cone_center = P1+4.5/5.*(P2-P1);
    
    print 'arrow_length=',arrow_length;
    print 'cylinder_length=',cylinder_length;
    
    axisZ = P2-P1;
    axisX = Orthogonal(axisZ);
    axisY = axisZ.cross(axisX);
    axisX.normalize();
    axisY.normalize();
    axisZ.normalize();
    rotmat = Matrix(axisX,axisY,axisZ);
    print rotmat;
    
    sc = Blender.Scene.GetCurrent();
    
    mesh = Blender.Mesh.Primitives.Cylinder(32, 2*cylinder_radius, cylinder_length);
    mesh.materials = [ excitation_material ];
    for f in mesh.faces:
        f.mat = 0;

    obj = sc.objects.new(mesh, 'arrow_cylinder');
    obj.setMatrix(rotmat);
    obj.setLocation(cylinder_center[0], cylinder_center[1], cylinder_center[2]);

    mesh = Blender.Mesh.Primitives.Cone(32, 2*cone_radius, cone_length);
    mesh.materials = [ excitation_material ];
    for f in mesh.faces:
        f.mat = 0;

    obj = sc.objects.new(mesh, 'arrow_cone');
    obj.setMatrix(rotmat);
    obj.setLocation(cone_center[0], cone_center[1], cone_center[2]);

    return

def snapshot2(plane, P1, P2, snapshot_type):
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

def snapshot(plane, P1, P2, snapshot_type):
    sc = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Plane(1.0);
    mesh.materials = snapshot_materials;
    for f in mesh.faces:
        f.mat = snapshot_type;

    if snapshot_type == 0:
        obj = sc.objects.new(mesh, 'frequency_snapshot');
    elif snapshot_type == 1:
        obj = sc.objects.new(mesh, 'time_snapshot');
    elif snapshot_type == 2:
        obj = sc.objects.new(mesh, 'eps_snapshot');
    else:
        Blender.Draw.PupMenu('Error: Unknown snapshot_type');
        return;

    # use plane primitive or build mesh manually (just 4 points + 4 edges)?
    pos = 0.5*(P1+P2);
    obj.setLocation(pos[0], pos[1], pos[2]);
    diag = P2-P1;
    if plane == 1:
        #X
        obj.SizeX = abs(diag[0]);
        obj.SizeY = abs(diag[1]);
        obj.SizeZ = abs(diag[2]);
        obj.RotX = 0;
        obj.RotY = math.radians(90);
        obj.RotZ = 0;
    elif plane == 2:
        #Y
        obj.SizeX = abs(diag[0]);
        obj.SizeY = abs(diag[1]);
        obj.SizeZ = abs(diag[2]);
        obj.RotX = math.radians(-90);
        obj.RotY = 0;
        obj.RotZ = 0;
    else:
        #Z
        obj.SizeX = abs(diag[0]);
        obj.SizeY = abs(diag[1]);
        obj.SizeZ = abs(diag[2]);
        obj.RotX = 0;
        obj.RotY = 0;
        obj.RotZ = 0;
    return

def GEOfrequency_snapshot(plane, P1, P2):
    # print "GEOfrequency_snapshot called"
    snapshot2(plane, P1, P2, 0);
    return
    
def GEOtime_snapshot(plane, P1, P2):
    snapshot2(plane, P1, P2, 1);
    return

def GEOeps_snapshot(plane, P1, P2):
    snapshot2(plane, P1, P2, 2);
    return

def GEOprobe(position):
    sc = Blender.Scene.GetCurrent();
    mesh = Blender.Mesh.Primitives.Cube(0.1);

    obj = sc.objects.new(mesh, 'probe');
    obj.setLocation(position[0], position[1], position[2]);
    return

def readBristolFDTD(filename):
# should read .in file to get all .inp + .geo

# TODO:
# cylinder
# block
# box
# sphere
# mesh
# excitation
# flags
# frequency snapshot
# time snapshot

  Blender.Window.WaitCursor(1);
  
  in_file = file(filename, "r");
  line = in_file.readline();
  
  # Nobjects = int(line)
  # #print "Nobjects=", Nobjects
  # object_names = []
  # for i in range(0, Nobjects):
    # line = in_file.readline()
    # object_names.append(line.strip())
  
  # #print "object_names=", object_names
  
  # global_verts = []
  # offset = 0
  # for i_object in range(0, Nobjects):
    # line = in_file.readline()
    # words = line.split()
    # Nverts = int(words[0])
    # Nfaces = int(words[1])
    # #print "Nverts=", Nverts
    # #print "Nfaces=", Nfaces
    
    # local_verts = []
    # for i_vert in range(0, Nverts):
      # line = in_file.readline()
      # words = line.split()
      # x = float(words[0])
      # y = float(words[1])
      # z = float(words[2])
      # #print "x, y, z=", x, y, z
      # local_verts.append( Vector(x, y, z) )
      # global_verts.append( Vector(x, y, z) )
    
    # faces = []
    # for i_face in range(0, Nfaces):
          # line = in_file.readline()
          # words = line.split()
          # if len(words) < 3:
            # Blender.Draw.PupMenu('Error%t|File format error 4')
            # return
          # Nverts_in_face = int(words[0])
          # if len(words) != 1 + Nverts_in_face:
            # Blender.Draw.PupMenu('Error%t|File format error 5')
            # return
          # face_verts = []
          # for i_face_vert in range(0, Nverts_in_face):
            # idx = int(words[i_face_vert + 1]) - offset
            # face_verts.append(idx)
          # #print "face_verts=", face_verts
          # faces.append(face_verts)
    
    # # print "Adding object ", object_names[i_object]
    # BPyAddMesh.add_mesh_simple(object_names[i_object], local_verts, [], faces)

    # offset += Nverts

  in_file.close()

def TestObjects():
    sc = Blender.Scene.GetCurrent()

    cube = Blender.Mesh.Primitives.Cube(1.0)

    ####################
    # first object in selection list
    # ob = Blender.Object.GetSelected()[0] 

    # get the Mesh version of our cube, not NMesh
    # me = Blender.Mesh.Get( ob.data.name ) 

    # create some materials

    red = Blender.Material.New('Red')
    red.rgbCol = 1, 0, 0  # red, green, blue values

    green = Blender.Material.New('Green')
    green.rgbCol = 0, 1, 0  # red, green, blue values

    blue = Blender.Material.New('Blue')
    blue.rgbCol = 0, 0, 1  # red, green, blue values

    # add the material list to our ObData
    cube.materials = [red, green, blue ]

    # set the face materials of our cube

    # we can set all faces the same color like this
    for f in cube.faces:
        f.mat = 0

    # or for fun, we can alternate colors like this
    for i in range(len(cube.faces)):
        cube.faces[i].mat = i % 3
    ####################

    sc.objects.new(cube, 'Mesh')

    cylinder = Blender.Mesh.Primitives.Cylinder(32, 2.0, 6.0)
    # print cylinder.faces[0]
    # cylinder.faces.clear()
    
    cylinder.faces.delete(0, range(len(cylinder.faces)));
    
    # cylinder.RotX = math.radians( 90 )
    
    obj = sc.objects.new(cylinder, 'Mesh')
    obj.RotX = math.radians( 45 )
    obj.RotY = math.radians( 45 )
    obj.RotZ = math.radians( 45 )
    obj.LocX = 0
    obj.LocY = 0
    obj.LocZ = 5
    obj.setLocation(1, 2, 3)
    # obj.setEuler([math.radians( 90 ), 0, 0])

    # uvsphere = Blender.Mesh.Primitives.UVsphere(32, 32, 3.0)
    # sc.objects.new(uvsphere, 'Mesh')

    # icosphere = Blender.Mesh.Primitives.Icosphere(2, 4.0)
    # sc.objects.new(icosphere, 'Mesh')

    # grid = Blender.Mesh.Primitives.Grid(32, 32, 5.0)
    # sc.objects.new(grid, 'Mesh')

    # plane = Blender.Mesh.Primitives.Plane(6.0)
    # sc.objects.new(plane, 'Mesh')
  

	# verts = []
	# faces = []
		
	# verts.append([-(PREF_WIDTH/2), (PREF_HEIGHT/2), 0.0])
	# verts.append([-(PREF_WIDTH/2), -(PREF_HEIGHT/2), 0.0])
	# verts.append([(PREF_WIDTH/2), -(PREF_HEIGHT/2), 0.0])
	# verts.append([(PREF_WIDTH/2), (PREF_HEIGHT/2), 0.0])
	
	# faces.append([0, 1, 2, 3])
	
	# BPyAddMesh.add_mesh_simple('MyBlock', verts, [], faces)
  
# Blender.Window.FileSelector(readBristolFDTD, "Import", Blender.sys.makename(ext='.geo'))
# TestObjects()

# GEOmesh([1, 1], [1, 2, 3], [4, 3, 2, 1]);

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

# GEOfrequency_snapshot(1, Vector(-1, -1, -1), Vector(1, 1, 1));
# GEOfrequency_snapshot(2, Vector(-1, -1, -1), Vector(1, 1, 1));
# GEOfrequency_snapshot(3, Vector(-1, -1, -1), Vector(1, 1, 1));

# GEOtime_snapshot(1, Vector(2, -1, -1), Vector(4, 1, 1));
# GEOtime_snapshot(2, Vector(2, -1, -1), Vector(4, 1, 1));
# GEOtime_snapshot(3, Vector(2, -1, -1), Vector(4, 1, 1));

# GEOeps_snapshot(1, Vector(5, -1, -1), Vector(7, 1, 1));
# GEOeps_snapshot(2, Vector(5, -1, -1), Vector(7, 1, 1));
# GEOeps_snapshot(3, Vector(5, -1, -1), Vector(7, 1, 1));

# GEOfrequency_snapshot(1, Vector(-1, -1, -1), Vector(-1, 1, 1));
# GEOfrequency_snapshot(2, Vector(-1, -1, -1), Vector(1, -1, 1));
# GEOfrequency_snapshot(3, Vector(-1, -1, -1), Vector(1, 1, -1));

# GEOtime_snapshot(1, Vector(2, -1, -1), Vector(2, 1, 1));
# GEOtime_snapshot(2, Vector(2, -1, -1), Vector(4, -1, 1));
# GEOtime_snapshot(3, Vector(2, -1, -1), Vector(4, 1, -1));

# GEOeps_snapshot(1, Vector(5, -1, -1), Vector(5, 1, 1));
# GEOeps_snapshot(2, Vector(5, -1, -1), Vector(7, -1, 1));
# GEOeps_snapshot(3, Vector(5, -1, -1), Vector(7, 1, -1));

# for i in range(11):
    # GEOblock(Vector(0, 0, i), Vector(1, 1, i+1), 10*i, 0);
    # GEObox(Vector(1, 1, i), Vector(2, 2, i+1));
    # GEOblock(Vector(2, 2, i), Vector(3, 3, i+1), 10*i, 100);
    # GEOcylinder(Vector(3.5, 3.5, i+0.5), 0, 0.5, 1, 100-10*i, 200, 0);
    # GEOcylinder(Vector(4.5, 4.5, i+0.5), 0, 0.5, 1, 10*i, 200, 45);
    # GEOsphere(Vector(5.5, 5.5, i+0.5), 0.5, 0, i, 0);
    # GEOprobe(Vector(0, 0, i));

Blender.Window.RedrawAll()
Blender.Window.WaitCursor(0)
