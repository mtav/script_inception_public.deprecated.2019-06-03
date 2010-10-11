#!BPY

"""
Name: 'Bristol FDTD (*.in,*.geo,*.inp)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from Bristol FDTD'
"""

import Blender;
import bpy;
import BPyAddMesh;
import math;
import os;
import sys;
import re;
import array;
from bfdtd_parser import *;

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
        
        max_permittivity = 25.0;
        permittivity_material = Blender.Material.New('permittivity');
        permittivity_material.rgbCol = 0, permittivity/max_permittivity, 1.0-permittivity/max_permittivity;

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
    Nx = len(delta_X_vector)+1;
    Ny = len(delta_Y_vector)+1;
    Nz = len(delta_Z_vector)+1;
    
    # verts = array.array('d',range());
    verts = range(Nx*Ny*Nz);
    edges = range(Nx*Ny + Ny*Nz + Nz*Nx);
    faces = [];
    
    x=0;
    y=0;
    z=0;
    vert_idx = 0;
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
                verts[vert_idx] = Vector(x, y, z); vert_idx+=1;
    
    edge_idx = 0;
    for i in range(Nx):
        for j in range(Ny):
            A = grid_index(Nx, Ny, Nz, i, j, 0);
            B = grid_index(Nx, Ny, Nz, i, j, Nz-1);
            edges[edge_idx] = [A, B]; edge_idx+=1;

    for j in range(Ny):
        for k in range(Nz):
            A = grid_index(Nx, Ny, Nz, 0, j, k);
            B = grid_index(Nx, Ny, Nz, Nx-1, j, k);
            edges[edge_idx] = [A, B]; edge_idx+=1;

    for k in range(Nz):
        for i in range(Nx):
            A = grid_index(Nx, Ny, Nz, i, 0, k);
            B = grid_index(Nx, Ny, Nz, i, Ny-1, k);
            edges[edge_idx] = [A, B]; edge_idx+=1;
    
    # print verts;
    BPyAddMesh.add_mesh_simple('mesh', verts, edges, faces);
    # print 'Nverts=', len(verts);
    # print 'Nverts=', Nx*Ny*Nz;

    # print 'Nedges=', len(edges);
    # print 'Nedges=', Nx*Ny + Ny*Nz + Nz*Nx;

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
    scene.objects.unlink(arrow_cone_obj);
    
    return

def snapshot(plane, P1, P2, snapshot_type):

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
  
def importBristolFDTD(filename):
    print '----->Importing bristol FDTD geometry...';
    Blender.Window.WaitCursor(1);

    structured_entries = readBristolFDTD(filename);
    
    # Box
    GEObox(Vector(structured_entries.box.lower), Vector(structured_entries.box.upper));
    GEOmesh(structured_entries.xmesh,structured_entries.ymesh,structured_entries.zmesh);

    # print structured_entries.xmesh;
    # print structured_entries.ymesh;
    # print structured_entries.zmesh;
    
    # Time_snapshot (time or EPS)
    for time_snapshot in structured_entries.time_snapshot_list:
        if time_snapshot.eps == 0:
            GEOtime_snapshot(time_snapshot.plane, time_snapshot.P1, time_snapshot.P2);
        else:
            GEOeps_snapshot(time_snapshot.plane, time_snapshot.P1, time_snapshot.P2);
    # Frequency_snapshot
    for frequency_snapshot in structured_entries.frequency_snapshot_list:
        GEOfrequency_snapshot(frequency_snapshot.plane, frequency_snapshot.P1, frequency_snapshot.P2);

    # Excitation
    for excitation in structured_entries.excitation_list:
        GEOexcitation(Vector(excitation.P1), Vector(excitation.P2));
    # Probe
    for probe in structured_entries.probe_list:
        GEOprobe(Vector(probe.position));
    # Sphere
    for sphere in structured_entries.sphere_list:
        GEOsphere(Vector(sphere.center), sphere.R1, sphere.R2, sphere.permittivity, sphere.conductivity);
    # Block
    for block in structured_entries.block_list:
        GEOblock(Vector(block.lower), Vector(block.upper), block.permittivity, block.conductivity);
    # Cylinder
    for cylinder in structured_entries.cylinder_list:
        GEOcylinder(Vector(cylinder.center),cylinder.R1,cylinder.R2,cylinder.height,cylinder.permittivity,cylinder.conductivity,cylinder.angle);

    #########################
    # Not yet implemented:
    # Rotation
    # for rotation in structured_entries.rotation_list:
    # Flag
    # structured_entries.flag;
    # Boundaries
    # structured_entries.boundaries;
    #########################

    scene = Blender.Scene.GetCurrent();
    scene.update(0);
    Blender.Window.RedrawAll();
    Blender.Window.WaitCursor(0);
    print '...done';

Blender.Window.FileSelector(importBristolFDTD, "Import"); #, Blender.sys.makename(path='H:\\DATA\\foo',ext='.in'));
# importBristolFDTD('H:\\MATLAB\\blender_scripts\\rotated_cylinder.in');
