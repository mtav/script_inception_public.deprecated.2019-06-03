#!BPY

"""
Name: 'Bristol FDTD (*.in,*.geo,*.inp)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from Bristol FDTD'
"""
###############################
# IMPORTS
###############################
from bfdtd_parser import *;
from FDTDGeometryObjects import *

###############################
# INITIALIZATIONS
###############################
cfgfile = os.path.expanduser('~')+'/BlenderImport.txt';

###############################
# IMPORT FUNCTION
###############################
def importBristolFDTD(filename):
    ''' import BristolFDTD geometry from .in,.geo or .inp and create corresponding structure in Blender'''
    print('----->Importing bristol FDTD geometry: '+filename)
    Blender.Window.WaitCursor(1);

    # save import path
    # Blender.Set('tempdir',os.path.dirname(filename));
    FILE = open(cfgfile, 'w');
    cPickle.dump(filename, FILE);
    FILE.close();
    
    # create structured_entries
    structured_entries = readBristolFDTD(filename);
    
    FDTDGeometryObjects_obj = FDTDGeometryObjects()
    
    Blender.Window.RedrawAll(); # This must be called before any SetActiveLayer calls!
    
    # Box
    Blender.Window.SetActiveLayer(1<<0);
    FDTDGeometryObjects_obj.GEObox(Vector(structured_entries.box.lower), Vector(structured_entries.box.upper));
    
    # mesh
    Blender.Window.SetActiveLayer(1<<1);
    FDTDGeometryObjects_obj.GEOmesh(False, structured_entries.xmesh,structured_entries.ymesh,structured_entries.zmesh);
    
    # Time_snapshot (time or EPS)
    for time_snapshot in structured_entries.time_snapshot_list:
        if time_snapshot.eps == 0:
            Blender.Window.SetActiveLayer(1<<2);
            FDTDGeometryObjects_obj.GEOtime_snapshot(time_snapshot.plane, time_snapshot.P1, time_snapshot.P2);
        else:
            Blender.Window.SetActiveLayer(1<<3);
            FDTDGeometryObjects_obj.GEOeps_snapshot(time_snapshot.plane, time_snapshot.P1, time_snapshot.P2);
    # Frequency_snapshot
    Blender.Window.SetActiveLayer(1<<4);
    for frequency_snapshot in structured_entries.frequency_snapshot_list:
        FDTDGeometryObjects_obj.GEOfrequency_snapshot(frequency_snapshot.plane, frequency_snapshot.P1, frequency_snapshot.P2);

    # Excitation
    Blender.Window.SetActiveLayer(1<<5);
    for excitation in structured_entries.excitation_list:
        FDTDGeometryObjects_obj.GEOexcitation(Vector(excitation.P1), Vector(excitation.P2));
    # Probe
    Blender.Window.SetActiveLayer(1<<6);
    for probe in structured_entries.probe_list:
        # print('probe = ',Vector(probe.position))
        FDTDGeometryObjects_obj.GEOprobe(Vector(probe.position));
    
    # Sphere
    Blender.Window.SetActiveLayer(1<<7);
    for sphere in structured_entries.sphere_list:
        # variables
        center = Vector(sphere.center)

        # initialise rotation_matrix
        rotation_matrix = Blender.Mathutils.Matrix()
        rotation_matrix.identity();

        # position object
        T = Blender.Mathutils.TranslationMatrix(center)
        rotation_matrix *= T;
        
        # add rotations
        for r in sphere.rotation_list:
          rotation_matrix *= rotationMatrix(r.axis_point, r.axis_direction, r.angle_degrees);
          
        # create object
        FDTDGeometryObjects_obj.GEOsphere_matrix(rotation_matrix, sphere.outer_radius, sphere.inner_radius, sphere.permittivity, sphere.conductivity);
        
    # Block
    Blender.Window.SetActiveLayer(1<<8);
    for block in structured_entries.block_list:
        # variables
        lower = Vector(block.lower)
        upper = Vector(block.upper)
        pos = 0.5*(lower+upper);
        diag = upper-lower;

        # initialise rotation_matrix
        rotation_matrix = Blender.Mathutils.Matrix()
        rotation_matrix.identity();

        # scale object
        Sx=Blender.Mathutils.ScaleMatrix(abs(diag[0]),4,Blender.Mathutils.Vector(1,0,0))
        Sy=Blender.Mathutils.ScaleMatrix(abs(diag[1]),4,Blender.Mathutils.Vector(0,1,0))
        Sz=Blender.Mathutils.ScaleMatrix(abs(diag[2]),4,Blender.Mathutils.Vector(0,0,1))
        rotation_matrix *= Sx*Sy*Sz;
        # position object
        T = Blender.Mathutils.TranslationMatrix(pos)
        rotation_matrix *= T;
        
        # add rotations
        for r in block.rotation_list:
          rotation_matrix *= rotationMatrix(r.axis_point, r.axis_direction, r.angle_degrees);

        # create object
        FDTDGeometryObjects_obj.GEOblock_matrix(rotation_matrix, block.permittivity, block.conductivity);
    
    # Cylinder
    Blender.Window.SetActiveLayer(1<<9);
    for cylinder in structured_entries.cylinder_list:
      
        # initialise rotation_matrix
        rotation_matrix = Blender.Mathutils.Matrix()
        rotation_matrix.identity();

        # because FDTD cylinders are aligned with the Y axis by default
        rotation_matrix *= rotationMatrix(Blender.Mathutils.Vector(0,0,0), Blender.Mathutils.Vector(1,0,0), -90)
        
        # position object
        T = Blender.Mathutils.TranslationMatrix(Blender.Mathutils.Vector(cylinder.center[0],cylinder.center[1],cylinder.center[2]))
        rotation_matrix *= T;
        
        # add rotations
        for r in cylinder.rotation_list:
          rotation_matrix *= rotationMatrix(r.axis_point, r.axis_direction, r.angle_degrees);
        
        # create object
        FDTDGeometryObjects_obj.GEOcylinder_matrix(rotation_matrix, cylinder.inner_radius,cylinder.outer_radius,cylinder.height,cylinder.permittivity,cylinder.conductivity);

    #########################
    # Not yet implemented:
    # Flag
    # structured_entries.flag;
    # Boundaries
    # structured_entries.boundaries;
    #########################

    scene = Blender.Scene.GetCurrent();
    scene.update(0);
    Blender.Window.RedrawAll();
    Blender.Window.WaitCursor(0);
    Blender.Scene.GetCurrent().setLayers([1,3,4,5,6,7,8,9,10]);
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
          importBristolFDTD(sys.argv[4+i]);
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
      Blender.Window.FileSelector(importBristolFDTD, "Import Bristol FDTD file...", default_path);
      # TestObjects();

if __name__ == "__main__":
  main()
