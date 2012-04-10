#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import numpy
import os

class GWLobject:
  def __init__(self):
    self.GWL_voxels = []
    self.voxel_offset = [0,0,0,0]
    self.stage_position = [0,0,0,0]
    self.LineNumber = 1
    self.LineDistance = 0
    self.PowerScaling = 1
    self.LaserPower = 100
    self.ScanSpeed = 200
    self.Repeat = 1
    self.path_substitutes = []
    
  def clear(self):
    self.GWL_voxels = []
    self.voxel_offset = [0,0,0,0]
  
  def addLine(self,P1,P2):
    write_sequence = [P1,P2]
    self.GWL_voxels.append(write_sequence)

  def addHorizontalGrating(self, P1, P2, LineNumber, LineDistance):
    u = numpy.array(P2)-numpy.array(P1)
    u = u*1.0/numpy.sqrt(pow(u[0],2)+pow(u[1],2)+pow(u[2],2))
    v = numpy.array([-u[1],u[0],0])
    L = (LineNumber-1)*LineDistance    
    P1_min = P1 - 0.5*L*v
    
    plist = []
    for k in range(LineNumber):
        A = P1_min + k*LineDistance*v
        B = A + (P2-P1)
        plist.append((A,B))

    counter = 0
    for (A,B) in plist:
      if counter%2 == 0:
        self.GWL_voxels.append([A,B])
      else:
        self.GWL_voxels.append([B,A])
      counter = counter + 1
    
  def addZGrating(self, P1, P2, LineNumber, LineDistance, BottomToTop = False):
    Zcenter = 0.5*(P1[2] + P2[2])
    zlist = []
    L = (LineNumber-1)*LineDistance
    if BottomToTop:
      zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber)
    else:
      zlist = numpy.linspace(Zcenter+0.5*L, Zcenter-0.5*L, LineNumber)
    #if LineNumber%2: #odd LineNumber
      #zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber)
    #else: #even LineNumber
      #zlist = numpy.arange(Zcenter-LineNumber/2*LineDistance, Zcenter+((LineNumber-1)/2+1)*LineDistance, LineDistance)
    counter = 0
    for z in zlist:
      A = [P1[0],P1[1],z]
      B = [P2[0],P2[1],z]
      if counter%2 == 0:
        self.GWL_voxels.append([A,B])
      else:
        self.GWL_voxels.append([B,A])
      counter = counter + 1

  def addXblock(self, P1, P2, LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop = False):
    Xcenter = 0.5*(P1[0] + P2[0])
    Ycenter = 0.5*(P1[1] + P2[1])
    Zcenter = 0.5*(P1[2] + P2[2])
    #print Zcenter
    #print LineNumber_Vertical

    ylist = []
    L = (LineNumber_Horizontal-1)*LineDistance_Horizontal
    ylist = numpy.linspace(Ycenter-0.5*L, Ycenter+0.5*L, LineNumber_Horizontal)
    
    zlist = []
    L = (LineNumber_Vertical-1)*LineDistance_Vertical
    if BottomToTop:
      zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber_Vertical)
    else:
      zlist = numpy.linspace(Zcenter+0.5*L, Zcenter-0.5*L, LineNumber_Vertical)

    counter = 0
    for z in zlist:
      for y in ylist:
        A = [P1[0],y,z]
        B = [P2[0],y,z]
        if counter%2 == 0:
          self.GWL_voxels.append([A,B])
        else:
          self.GWL_voxels.append([B,A])
        counter = counter + 1

  def addYblock(self, P1, P2, LineNumber_Horizontal, LineDistance_Horizontal, LineNumber_Vertical, LineDistance_Vertical, BottomToTop = False):
    Xcenter = 0.5*(P1[0] + P2[0])
    Ycenter = 0.5*(P1[1] + P2[1])
    Zcenter = 0.5*(P1[2] + P2[2])

    xlist = []
    L = (LineNumber_Horizontal-1)*LineDistance_Horizontal
    xlist = numpy.linspace(Xcenter-0.5*L, Xcenter+0.5*L, LineNumber_Horizontal)
    
    zlist = []
    L = (LineNumber_Vertical-1)*LineDistance_Vertical
    if BottomToTop:
      zlist = numpy.linspace(Zcenter-0.5*L, Zcenter+0.5*L, LineNumber_Vertical)
    else:
      zlist = numpy.linspace(Zcenter+0.5*L, Zcenter-0.5*L, LineNumber_Vertical)

    counter = 0
    for z in zlist:
      for x in xlist:
        A = [x,P1[1],z]
        B = [x,P2[1],z]
        if counter%2 == 0:
          self.GWL_voxels.append([A,B])
        else:
          self.GWL_voxels.append([B,A])
        counter = counter + 1

  def addHorizontalCircle(self, center, radius, power, PointDistance):
    #print radius
    write_sequence = []
    if radius < 0.5*PointDistance:
      write_sequence.append(center)
    else:
      #print(('PointDistance = ', PointDistance))
      #print radius
      #print PointDistance/float(2*radius)
      alphaStep = 2*numpy.arcsin(PointDistance/float(2*radius))
      N = int(2*numpy.pi/alphaStep)
      for i in range(N):
        if 0<=power and power<=100:
          P = [center[0]+radius*numpy.cos(i*2*numpy.pi/float(N)),center[1]+radius*numpy.sin(i*2*numpy.pi/float(N)),center[2],power]
        else:
          P = [center[0]+radius*numpy.cos(i*2*numpy.pi/float(N)),center[1]+radius*numpy.sin(i*2*numpy.pi/float(N)),center[2]]
        write_sequence.append(P)
    self.GWL_voxels.append(write_sequence)

  def addHorizontalDisk(self, center, radius, power, PointDistance):
    N = int(radius/float(PointDistance))
    #print(('N = ',N))
    for i in range(N+1):
      if i==0:
        self.addHorizontalCircle(center, 0, power, PointDistance)
        ##print center
        #self.GWL_voxels.append([center])
      else:
        self.addHorizontalCircle(center, i*radius/float(N), power, PointDistance)

  def addSphere(self, center, radius, power, HorizontalPointDistance, VerticalPointDistance, solid = False):

    PointDistance = numpy.sqrt(pow(HorizontalPointDistance,2)+pow(VerticalPointDistance,2))
    #print PointDistance
    if radius == 0:
      self.GWL_voxels.append([center])
    else:
      alphaStep = 2*numpy.arcsin(PointDistance/float(2*radius))
      N = int(0.5*numpy.pi/alphaStep)
      zlist = []
      for i in range(N+1):
        #print(('i = ',i,' N = ',N))
        z = radius*numpy.cos(i*0.5*numpy.pi/float(N))
        zlist.append(z)
        
      # symetrify list
      zlist = zlist + [ -i for i in zlist[len(zlist)-2::-1] ]
        
      for z in zlist:
        local_radius = numpy.sqrt(pow(radius,2)-pow(z,2))
        #print(('local_radius 1 = ',local_radius))
        #local_radius = radius*numpy.sin(i*numpy.pi/float(N))
        #print(('local_radius 2 = ',local_radius))
        if solid:
          self.addHorizontalDisk([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)
        else:
          self.addHorizontalCircle([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)

    #N = int(radius/float(VerticalPointDistance))
    #for i in range(-N,N+1):
      #z = i*radius/float(N)
      #local_radius = numpy.sqrt(pow(radius,2)-pow(z,2))
      ##print 'local_radius = ', local_radius
      #if solid:
        #self.addHorizontalDisk([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)
      #else:
        #self.addHorizontalCircle([center[0],center[1],center[2]+z], local_radius, power, HorizontalPointDistance)

  def addWrite(self):
    write_sequence = []
    self.GWL_voxels.append(write_sequence)

  def readSubstitutes(self, subsFile):
    print('Reading substitution pairs from '+subsFile)
    self.path_substitutes = []
    try:
      with open(subsFile, 'r') as file:
        for line in file:
          t = line.strip().split('->')
          if len(t)==2:
            old = t[0].strip()
            new = t[1].strip()
            old = old.replace('\\',os.path.sep).replace('/',os.path.sep)
            new = new.replace('\\',os.path.sep).replace('/',os.path.sep)
            print(old+' -> '+new)
            self.path_substitutes.append((old,new))
    except IOError as (errno, strerror):
      print "I/O error({0}): {1}".format(errno, strerror)
      print 'Failed to open '+subsFile

    return self.path_substitutes

  def readGWL(self, filename):
    Nvoxels = 0
    write_sequence = []
    try:
      with open(filename, 'r') as file:
        for line in file:
          #print line
          line_stripped = line.strip()
          # TODO: handle comments and other commands
          if len(line_stripped)>0 and line_stripped[0]!='%':
            #print 'pre-split: ', line_stripped
            #cmd = re.split('[^a-zA-Z0-9_+-.]+',line_stripped)
            #cmd = re.split('[^a-zA-Z0-9_+-.:\\/]+',line_stripped)
            #cmd = re.split('[ \t]',line_stripped)
            cmd = re.split('\s+',line_stripped)
            #cmd = [ i.lower() for i in cmd ]
            #print 'post-split: ', cmd
            stopRepeat = True
            for i in range(self.Repeat):
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
                    # TODO: custom replacement strings read from a config file to replace for example C:\utilities with ~/GWLstuff and vice-versa
                    
                    
                    #self.path_substitutes = [('C:','D:'),('C:','E:'),('C:','F:')]
                    #self.path_substitutes = readSubstitutes(subsFile)
                    
                    print('line_stripped = ' + line_stripped)
                    file_to_include = re.split('\s+',line_stripped,1)[1]
                    print('including file_to_include = ' + file_to_include)
                    print('Fixing file separators')
                    file_to_include = file_to_include.replace('\\',os.path.sep).replace('/',os.path.sep)
                    print('including file_to_include = ' + file_to_include)                    
                    #self.readGWL('C:\\Users\\User\\Desktop\\Daniel+Mike\\nanoscribe_sample_2012-02-29'+os.path.sep+cmd[1])
                    #print('file_to_include[0:3] = ' + file_to_include[0:3])
                    
                    file_to_include_fullpath = os.path.normpath(os.path.join(os.path.dirname(filename), os.path.expanduser(file_to_include)))

                    #if file_to_include[0:3] == 'C:\\':
                      #file_to_include = file_to_include
                    #else:
                      ##file_to_include = os.path.dirname(filename) + os.path.sep + file_to_include
                      #file_to_include = os.path.normpath(os.path.join(os.path.dirname(filename), file_to_include))
                    print(file_to_include_fullpath)
                    if not os.path.isfile(file_to_include_fullpath):
                      print('WARNING: File not found. Attempting path substitutions')
                      for (old,new) in self.path_substitutes:
                        file_to_try = file_to_include.replace(old,new)
                        print('file_to_try = ',file_to_try)
                        print('filename = ',filename)
                        print('os.path.dirname(filename) = ',os.path.dirname(filename))
                        file_to_try = os.path.normpath(os.path.join(os.path.dirname(filename), os.path.expanduser(file_to_try)))
                        print('file_to_try = ',file_to_try)
                        print('Trying file_to_try = ' + file_to_try)
                        if os.path.isfile(file_to_try):
                          file_to_include_fullpath = file_to_try
                          break
                    self.readGWL(file_to_include_fullpath)
                    
                  elif cmd[0].lower()=='movestagex':
                    print('Moving X by '+cmd[1])
                    self.stage_position[0] = self.stage_position[0] + float(cmd[1])
                  elif cmd[0].lower()=='movestagey':
                    print('Moving Y by '+cmd[1])
                    self.stage_position[1] = self.stage_position[1] + float(cmd[1])
                    
                  elif cmd[0].lower()=='addxoffset':
                    print 'Adding X offset of '+cmd[1]
                    self.voxel_offset[0] = self.voxel_offset[0] + float(cmd[1])
                  elif cmd[0].lower()=='addyoffset':
                    print 'Adding Y offset of '+cmd[1]
                    self.voxel_offset[1] = self.voxel_offset[1] + float(cmd[1])
                  elif cmd[0].lower()=='addzoffset':
                    print 'Adding Z offset of '+cmd[1]
                    self.voxel_offset[2] = self.voxel_offset[2] + float(cmd[1])
                    
                  elif cmd[0].lower()=='xoffset':
                    print 'Setting X offset to '+cmd[1]
                    self.voxel_offset[0] = float(cmd[1])
                  elif cmd[0].lower()=='yoffset':
                    print 'Setting Y offset to '+cmd[1]
                    self.voxel_offset[1] = float(cmd[1])
                  elif cmd[0].lower()=='zoffset':
                    print 'Setting Z offset to '+cmd[1]
                    self.voxel_offset[2] = float(cmd[1])

                  elif cmd[0].lower()=='linenumber':
                    print 'Setting LineNumber to '+cmd[1]
                    self.LineNumber = float(cmd[1])
                  elif cmd[0].lower()=='linedistance':
                    print 'Setting LineDistance to '+cmd[1]
                    self.LineDistance = float(cmd[1])
                  elif cmd[0].lower()=='powerscaling':
                    print 'Setting PowerScaling to '+cmd[1]
                    self.PowerScaling = float(cmd[1])
                  elif cmd[0].lower()=='laserpower':
                    print 'Setting LaserPower to '+cmd[1]
                    self.LaserPower = float(cmd[1])
                  elif cmd[0].lower()=='scanspeed':
                    print 'Setting ScanSpeed to '+cmd[1]
                    self.ScanSpeed = float(cmd[1])

                  elif cmd[0].lower()=='repeat':
                    print 'Repeating next command '+cmd[1]+' times.'
                    self.Repeat = float(cmd[1])
                    stopRepeat = False
                    
                  #elif cmd[0].lower()=='defocusfactor':
                    #print 'defocusfactor'
                  else:
                    print('UNKNOWN COMMAND: '+cmd[0])
                    #sys.exit(-1)
              else:
                #print '=>VOXEL'
                voxel = []
                for i in range(len(cmd)):
                  voxel.append(float(cmd[i])+self.voxel_offset[i]+self.stage_position[i])
                #voxel = [ float(i) for i in cmd ]
                write_sequence.append(voxel)
                Nvoxels = Nvoxels + 1
                  
            # reset repeat
            if stopRepeat:
                self.Repeat = 1
    except IOError as (errno, strerror):
      print "I/O error({0}): {1}".format(errno, strerror)
      print 'Failed to open '+filename
            
    print('Nvoxels = '+str(Nvoxels))
    #return GWL_voxels
  
  def write_GWL(self,filename):
    print('Writing GWL to '+filename)
    with open(filename, 'w') as file:
      for write_sequence in self.GWL_voxels:
        for voxel in write_sequence:
          for i in range(len(voxel)):
            file.write(str(voxel[i]))
            if i<len(voxel)-1:
              file.write('\t')
            else:
              file.write('\n')
        #file.write('-999\t-999\t-999\n')
        file.write('Write\n')
        
if __name__ == "__main__":
  #GWL_obj = GWLobject()
  #GWL_obj.readGWL(sys.argv[1])
  ##print GWL_obj.GWL_voxels
  #GWL_obj.write_GWL('copy.gwl')

  GWL_obj = GWLobject()
  GWL_obj.addXblock([0,0,0],[1,0,0],2,0.050,3,0.100)
  GWL_obj.addXblock([0,0,1.5],[1,0,1.5],2,0.050,3,0.100)
  GWL_obj.addXblock([0,0,2.75],[1,0,2.75],2,0.050,3,0.100)
  z = 7.1038825; GWL_obj.addXblock([0,0,z],[1,0,z],2,0.050,3,0.100)

  power = 75
  
  center = [0,0,3]
  HorizontalPointDistance = 0.050
  VerticalPointDistance = 0.100
  radius = 1
  
  #print 'addHorizontalCircle'
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  #print 'addHorizontalDisk'
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  #print 'addSphere non-solid'
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  #print 'addSphere solid'
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 0.100
  VerticalPointDistance = 0.200
  center = [10,0,3]
  radius = 2
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 1
  VerticalPointDistance = 0.5
  center = [30,0,3]
  radius = 3
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 1
  VerticalPointDistance = 1
  center = [40,0,3]
  radius = 3
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  HorizontalPointDistance = 1
  VerticalPointDistance = 2
  center = [50,0,3]
  radius = 3
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  print '300'
  HorizontalPointDistance = 0.050
  VerticalPointDistance = 0.100
  center = [60,0,3]
  radius = 0.5*0.300
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  print '350'
  center = [70,0,3]
  radius = 0.5*0.350
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)

  print '400'
  center = [80,0,3]
  radius = 0.5*0.400
  GWL_obj.addHorizontalCircle(center, radius, power, HorizontalPointDistance)
  GWL_obj.addHorizontalDisk([center[0],center[1],center[2]+1], radius, power, HorizontalPointDistance)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+11], radius, power, HorizontalPointDistance, VerticalPointDistance, False)
  GWL_obj.addSphere([center[0],center[1],center[2]+1+22], radius, power, HorizontalPointDistance, VerticalPointDistance, True)


  GWL_obj.write_GWL('xblock.gwl')

  GWL_obj.clear()
  GWL_obj.addXblock([0,0,2.75],[10,0,2.75],5,0.050,8,0.100)
  GWL_obj.addYblock([1,0,2.75],[1,20,2.75],5,0.050,8,0.100)
  GWL_obj.write_GWL('xblock2.gwl')
