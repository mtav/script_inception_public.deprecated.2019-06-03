#!BPY

"""
Name: 'GWL (*.gwl)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from GWL file'
"""
###############################
# IMPORTS
###############################
from GWL.GWL_parser import *
import Blender
from Blender.Mathutils import Vector
import cPickle
import os
#from FDTDGeometryObjects import *
#from layer_manager import *
#from bfdtd.bristolFDTD_generator_functions import *

#import layer_manager
#from Blender import Draw, BGL, Text, Scene, Window, Object

# TODO: create linked duplicates of base voxel for faster loading! -> failed
# TODO: see how "Cells" voxelization script works and use that system for faster loading


###############################
# INITIALIZATIONS
###############################
#cfgfile = os.path.expanduser('~')+'/BlenderImportGWL.txt'
# official script data location :)
print('Blender.Get("datadir") = '+str(Blender.Get("datadir")))
if Blender.Get("datadir"):
  print('datadir defined')
  cfgfile = Blender.Get("datadir")+'/BlenderImportGWL.txt'
  substitutes_file = Blender.Get("datadir")+'/BlenderImportGWL_Substitutes.txt'
else:
  print('datadir not defined or somehow broken. Make sure the directory $HOME/.blender/scripts/bpydata is present and accessible.')
  sys.exit(0)

# Like pressing Alt+D
def linkedCopy(ob, position, scn=None): # Just like Alt+D
        if not scn:
          scn = Blender.Scene.GetCurrent()
        type = ob.getType()
        newOb = Blender.Object.New(type)
        if type != 'Empty':
          newOb.shareFrom(ob)
        scn.link(newOb)
        newOb.setMatrix(ob.getMatrix())
        # Copy other attributes.
        newOb.setDrawMode(ob.getDrawMode())
        newOb.setDrawType(ob.getDrawType())
        newOb.Layer = ob.Layer
        # Update the view 
        #ob.select(0)
        #newOb.select(1)
        newOb.setLocation(position[0],position[1],position[2])
        #return newOb
        return

def BlenderSphere(name, center, outer_radius):
    scene = Blender.Scene.GetCurrent()
    mesh = Blender.Mesh.Primitives.Icosphere(2, 2*outer_radius)
    #mesh.materials = self.materials(permittivity, conductivity)
    #for f in mesh.faces:
        #f.mat = 0
    obj = scene.objects.new(mesh, name)
    obj.setLocation(center[0], center[1], center[2])
    obj.transp = True
    obj.wireMode = True
    return obj

def BlenderBlock(name, center, outer_radius, scene, mesh):
    #scene = Blender.Scene.GetCurrent()
    #mesh = Blender.Mesh.Primitives.Cube(1.0)

    obj = scene.objects.new(mesh, name)
    pos = center
    diag = 2*outer_radius
    obj.SizeX = abs(diag)
    obj.SizeY = abs(diag)
    obj.SizeZ = abs(diag)
    obj.setLocation(pos[0], pos[1], pos[2])
    #obj.transp = True
    #obj.wireMode = True
    return obj

def BlenderBlock2(name, center, outer_radius):
    diag = 2*outer_radius
    return BlenderBlock2(name, center, abs(diag), abs(diag), abs(diag))

    #scene = Blender.Scene.GetCurrent()
    #mesh = Blender.Mesh.Primitives.Cube(1.0)

    #obj = scene.objects.new(mesh, name)
    #pos = center
    #diag = 2*outer_radius
    #obj.SizeX = abs(diag)
    #obj.SizeY = abs(diag)
    #obj.SizeZ = abs(diag)
    #obj.setLocation(pos[0], pos[1], pos[2])
    ##obj.transp = True
    ##obj.wireMode = True
    #return obj

def BlenderBlock2(name, center, SizeX, SizeY, SizeZ):
    scene = Blender.Scene.GetCurrent()
    mesh = Blender.Mesh.Primitives.Cube(1.0)

    obj = scene.objects.new(mesh, name)
    pos = center
    obj.SizeX = SizeX
    obj.SizeY = SizeY
    obj.SizeZ = SizeZ
    obj.setLocation(pos[0], pos[1], pos[2])
    #obj.transp = True
    #obj.wireMode = True
    return obj

#def BlenderLine(name,P1,P2,radius):
  
  
#def GEOcylinder(self, name, center, inner_radius, outer_radius, H, permittivity, conductivity, angle_X, angle_Y, angle_Z):
    #scene = Blender.Scene.GetCurrent();
    #mesh = Blender.Mesh.Primitives.Cylinder(32, 2*outer_radius, H);
    #mesh.materials = self.materials(permittivity, conductivity);
    #for f in mesh.faces:
        #f.mat = 0;

    #obj = scene.objects.new(mesh, name);
    #obj.setLocation(center[0], center[1], center[2]);
    #obj.RotX = angle_X;
    #obj.RotY = angle_Y;
    #obj.RotZ = angle_Z;
    #obj.transp = True; obj.wireMode = True;
    #return

#def GEOcylinder_matrix(self, name, rotation_matrix, inner_radius, outer_radius, H, permittivity, conductivity):
    #scene = Blender.Scene.GetCurrent();
    #mesh = Blender.Mesh.Primitives.Cylinder(32, 2*outer_radius, H);
    #mesh.materials = self.materials(permittivity, conductivity);
    #for f in mesh.faces:
        #f.mat = 0;

    #obj = scene.objects.new(mesh, name)
    #obj.setMatrix(rotation_matrix);
    #obj.transp = True; obj.wireMode = True;
    #return

###############################
# IMPORT FUNCTION
###############################
def importGWL(filename):
    ''' import GWL geometry from .gwl file and create corresponding structure in Blender '''
    print('----->Importing GWL geometry: '+filename)
    Blender.Window.WaitCursor(1);

    # save import path
    # Blender.Set('tempdir',os.path.dirname(filename));
    FILE = open(cfgfile, 'w');
    cPickle.dump(filename, FILE);
    FILE.close();
    
    scene = Blender.Scene.GetCurrent()
    mesh = Blender.Mesh.Primitives.Cube(1.0)
    
    # parse file
    GWL_obj = GWLobject()
    GWL_obj.readSubstitutes(substitutes_file)
    GWL_obj.readGWL(filename)
    Nvoxel = 0
    verts = []
    for write_sequence in GWL_obj.GWL_voxels:
      for voxel in write_sequence:
        #print voxel
        #BlenderSphere('voxel', Vector(voxel), 0.100)
        #BlenderBlock('voxel_'+str(Nvoxel), Vector(voxel), 0.100, scene, mesh)
        verts.append( Vector(voxel[0:3]) )

        #if Nvoxel == 0:
          #first_voxel = BlenderBlock('voxel', Vector(voxel), 0.100)
        #else:
          ##new_voxel = first_voxel.copy()
          ##new_voxel = linkedCopy(first_voxel,scene)
          ##Redraw()
          ##new_voxel.setLocation(voxel[0],voxel[1],voxel[2])
          #linkedCopy(first_voxel,voxel,scene)
        Nvoxel = Nvoxel + 1
      
    mesh_new = Blender.Mesh.New("voxelposition_mesh")
    mesh_new.verts = None
    mesh_new.verts.extend(verts)
    scene = Blender.Scene.GetCurrent()
    object_new = scene.objects.new(mesh_new,"voxelposition_object")
  
    #cell = BlenderBlock2('voxel',Vector(0,0,0),0.100)
    cell = BlenderBlock2('voxel',Vector(0,0,0),0.100,0.100,0.200)
    cell.layers = object_new.layers
    scene.update()
    object_new.makeParent([cell])
    object_new.enableDupVerts = True

    
    
    print('Nvoxel = '+str(Nvoxel))
    Blender.Scene.GetCurrent().update(0)
    Blender.Window.RedrawAll()
    Blender.Window.WaitCursor(0)
    #Blender.Scene.GetCurrent().setLayers([1,3,4,5,6,7,8,9,10]);
    print('...done')

###############################
# MAIN FUNCTION
###############################
def main():
  ''' MAIN FUNCTION '''
  print('sys.argv=' + str(sys.argv))
  print('len(sys.argv)=' + str(len(sys.argv)))
  
  # arg[0]='blender'
  # arg[1]='-P'
  # arg[2]='scriptname'
  # arg[3]='--'
  
  if len(sys.argv)>4:
      for i in range(len(sys.argv)- 4):
          print('Importing ' + sys.argv[4+i])
          importGWL(sys.argv[4+i]);
  else:
      ###################
      # load import path
      ###################
      # print('tempdir=',Blender.Get('tempdir'))
      # print('soundsdir=',Blender.Get('soundsdir'))
  
      # default_path = Blender.Get('tempdir');
      # if not default_path:
          # default_path = os.getenv('DATADIR');
          
      default_path = os.getenv('DATADIR')
      print('cfgfile = ', cfgfile)
  
      if os.path.isfile(cfgfile) and os.path.getsize(cfgfile) > 0:
          with open(cfgfile, 'r') as FILE:
              default_path = cPickle.load(FILE);
  
      ###################
  
      ###################
      # import file
      ###################
      Blender.Window.FileSelector(importGWL, "Import GWL file...", default_path);
      # TestObjects();

if __name__ == "__main__":
  main()
