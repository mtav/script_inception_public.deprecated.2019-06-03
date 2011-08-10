#!/usr/bin/env python

import bpy

def testkubo():
  verts = [(1.0, 1.0, -1.0),
           (1.0, -1.0, -1.0),
          (-1.0, -1.0, -1.0),
          (-1.0, 1.0, -1.0),
           (1.0, 1.0, 1.0),
           (1.0, -1.0, 1.0),
          (-1.0, -1.0, 1.0),
          (-1.0, 1.0, 1.0)]
  
  #faces = [(0, 1, 2, 3),
           #(4, 7, 6, 5),
           #(0, 4, 5, 1),
           #(1, 5, 6, 2),
           #(2, 6, 7, 3),
           #(4, 0, 3, 7)]

  edges = [(0, 1),
          (1, 2),
          (2, 3),
          (3, 0),
          (4, 7),
          (7, 6),
          (6, 5),
          (5, 4),
          (0, 4),
          (5, 1),
          (2, 6),
          (7, 3)]
  
  faces = []
  
  mesh_data = bpy.data.meshes.new("cube_mesh_data")
  mesh_data.from_pydata(verts, edges, faces)
  mesh_data.update() # (calc_edges=True) not needed here
  
  cube_object = bpy.data.objects.new("superBox", mesh_data)
  
  scene = bpy.context.scene  
  scene.objects.link(cube_object)  
  cube_object.select = True

if __name__ == "__main__":
  testkubo()
