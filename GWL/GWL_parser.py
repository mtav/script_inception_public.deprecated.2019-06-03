#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
#from numpy import *

class GWLobject:
  def __init__(self):
    self.GWL_voxels = []
    self.voxel_offset = [0,0,0,0]
  
  def addLine(self,P1,P2):
    write_sequence = [P1,P2]
    self.GWL_voxels.append(write_sequence)

  def addWrite(self):
    write_sequence = []
    self.GWL_voxels.append(write_sequence)

  def readGWL(self,filename):
    Nvoxels = 0
    write_sequence = []
    with open(filename, 'r') as file:
      for line in file:
        #print line
        line_stripped = line.strip()
        # TODO: handle comments and other commands
        if len(line_stripped)>0 and line_stripped[0]!='%':
          cmd = re.split('[^a-zA-Z0-9_+-.]+',line_stripped)
          #cmd = [ i.lower() for i in cmd ]
          #print cmd
          if re.match(r"[a-zA-Z]",cmd[0][0]) or cmd[0]=='-999':
            #print '=>COMMAND'
            if cmd[0].lower()=='-999':
              if cmd[1]=='-999':
                #print 'write'
                self.GWL_voxels.append(write_sequence)
                write_sequence = []
            else:
              if cmd[0].lower()=='write':
                #print 'write'
                self.GWL_voxels.append(write_sequence)
                write_sequence = []
              elif cmd[0].lower()=='include':
                print 'including cmd[1]'
                self.readGWL(cmd[1])
              elif cmd[0].lower()=='movestagex':
                print 'Moving X by '+cmd[1]
                self.voxel_offset[0] = self.voxel_offset[0] + float(cmd[1])
              elif cmd[0].lower()=='movestagey':
                print 'Moving Y by '+cmd[1]
                self.voxel_offset[1] = self.voxel_offset[1] + float(cmd[1])
              #elif cmd[0].lower()=='defocusfactor':
                #print 'defocusfactor'
              #elif cmd[0].lower()=='laserpower':
                #print 'laserpower'
              else:
                print('UNKNOWN COMMAND: '+cmd[0])
                #sys.exit(-1)
          else:
            #print '=>VOXEL'
            voxel = []
            for i in range(len(cmd)):
              voxel.append(float(cmd[i])+self.voxel_offset[i])
            #voxel = [ float(i) for i in cmd ]
            write_sequence.append(voxel)
            Nvoxels = Nvoxels + 1
            
    print('Nvoxels = '+str(Nvoxels))
    #return GWL_voxels
  
  def write_GWL(self,filename):
    print('Writing GWL to '+filename)
    with open(filename, 'w') as file:
      for write_sequence in self.GWL_voxels:
        for voxel in write_sequence:
          file.write(str(voxel[0])+'\t'+str(voxel[1])+'\t'+str(voxel[2])+'\n')
        file.write('-999\t-999\t-999\n')
          
if __name__ == "__main__":
  GWL_obj = GWLobject()
  GWL_obj.readGWL(sys.argv[1])
  #print GWL_obj.GWL_voxels
  GWL_obj.write_GWL('copy.gwl')
  
