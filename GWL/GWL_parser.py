#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

def readGWL(filename):
  
  GWL_object = []
  write_sequence = []
  with open(filename, 'r') as file:
    for line in file:
      #print line
      line_stripped = line.strip()
      # TODO: handle comments and other commands
      if len(line_stripped)>0:
        cmd = re.split('[^a-zA-Z0-9_+-.]+',line_stripped)
        cmd = [ i.lower() for i in cmd ]
        print cmd
        if cmd[0]=='-999' or cmd[0]=='write':
          print 'write'
          GWL_object.append(write_sequence)
          write_sequence = []
        else:
          print 'voxel'
          voxel = [ float(i) for i in cmd ]
          write_sequence.append(voxel)
      #pattern_objects = re.compile("\w")
      #objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]

    #read_data = f.read()
    
  ## open file
  #input = open(filename)
  ## read the whole file as one string
  #fulltext = input.read()
  ## close file
  #input.close()
  return GWL_object

def write_GWL(filename, GWL_object):
  with open(filename, 'w') as file:
    for write_sequence in GWL_object:
      for voxel in write_sequence:
        file.write(str(voxel[0])+'\t'+str(voxel[1])+'\t'+str(voxel[2])+'\n')
      file.write('-999\t-999\t-999\n')
        
if __name__ == "__main__":
  GWL_object = readGWL(sys.argv[1])
  print GWL_object
  write_GWL('tmp.txt',GWL_object)
