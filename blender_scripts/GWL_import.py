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

# TODO: create linked duplicates of base voxel for faster loading!

###############################
# INITIALIZATIONS
###############################
#cfgfile = os.path.expanduser('~')+'/BlenderImport.txt'
# official script data location :)
cfgfile = Blender.Get("datadir")+'/BlenderImport.txt'

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
    return

def BlenderBlock(name, center, outer_radius):
    scene = Blender.Scene.GetCurrent()
    mesh = Blender.Mesh.Primitives.Cube(1.0)

    obj = scene.objects.new(mesh, name)
    pos = center
    diag = 2*outer_radius
    obj.SizeX = abs(diag)
    obj.SizeY = abs(diag)
    obj.SizeZ = abs(diag)
    obj.setLocation(pos[0], pos[1], pos[2])
    obj.transp = True
    obj.wireMode = True
    return;

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
    
    # parse file
    GWL_obj = GWLobject()
    GWL_obj.readGWL(filename)
    for write_sequence in GWL_obj.GWL_voxels:
      for voxel in write_sequence:
        #BlenderSphere('voxel', Vector(voxel), 0.100)
        BlenderBlock('voxel', Vector(voxel), 0.100)
    
    Blender.Scene.GetCurrent().update(0);
    Blender.Window.RedrawAll();
    Blender.Window.WaitCursor(0);
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
