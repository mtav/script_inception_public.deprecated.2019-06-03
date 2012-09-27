#!/usr/bin/env python
# -*- coding: utf-8 -*-
# parses BFDTD files

import math
import os
import sys
import re
from utilities.common import *
from bfdtd.bristolFDTD_generator_functions import *
from meshing.subGridMultiLayer import *
from bfdtd.excitation import *
from bfdtd.meshobject import *
from constants.constants import *
#from bfdtd.meshbox import *

#==== CLASSES START ====#

# TODO: Add function to easily change basename
# TODO: Add check for negative values in mesh.
# TODO: refactor class names with "_", get rid of unused lists or use them
# TODO: Add check for more than 99/100 snapshots (number only go from 0/1 to 99)
# TODO: create ref document about .prn files numbering, bfdtd output files, etc

# mandatory objects
class Flag(object):
  def __init__(self):
    self.name = 'flag'
    self.layer = 'flag'
    self.group = 'flag'
    self.iterationMethod = 5
    self.propagationConstant = 0
    self.flagOne = 0
    self.flagTwo = 0
    self.iterations = 25000
    self.timeStep = 0.9; #mus
    self.id_string = '_id_'
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'iMethod = ' + str(self.iterationMethod) + '\n' +\
    'propCons = ' + str(self.propagationConstant) + '\n' +\
    'flagOne = ' + str(self.flagOne) + '\n' +\
    'flagTwo = ' + str(self.flagTwo) + '\n' +\
    'iterations = ' + str(self.iterations) + '\n' +\
    'timeStep = ' + str(self.timeStep) + '\n' +\
    'id = ' + self.id_string
    return ret
  def read_entry(self, entry):
    if entry.name:
      self.name = entry.name
    self.iterationMethod = float(entry.data[0])
    self.propagationConstant = float(entry.data[1])
    self.flagOne = float(entry.data[2])
    self.flagTwo = float(entry.data[3])
    self.iterations = float(entry.data[4])
    self.timeStep = float(entry.data[5])
    self.id_string = entry.data[6]
  def write_entry(self, FILE):
    FILE.write('FLAG  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%d **ITERATION METHOD\n" % self.iterationMethod)
    FILE.write("%E **PROPAGATION CONSTANT (IGNORED IN 3D MODEL)\n" % self.propagationConstant)
    FILE.write("%d **FLAG ONE\n" % self.flagOne)
    FILE.write("%d **FLAG TWO\n" % self.flagTwo)
    FILE.write("%d **ITERATIONS\n" % self.iterations)
    FILE.write("%E **TIMESTEP as a proportion of the maximum allowed\n" % self.timeStep)
    FILE.write("\"%s\" **ID CHARACTER (ALWAYS USE QUOTES)\n" % self.id_string.strip('"'))
    FILE.write('}\n')
    FILE.write('\n')

class Boundaries(object):
  '''
  The following ABC algorithms are available in the FDTD program
  0. Magnetic Wall
  1. Metal wall.
  2. Mur 1st.
  6. Dispersive.
  7. Higdon 1st.
  9. Higdon 2nd
  10. PML
  
  The parameters are for the second order and Perfectly Matched Layer boundary conditions and have the following
  meanings:
  i. Dispersive ABC Parameter 1 and parameter2 are the values of effective permittivity for
    which perfect absorption may be expected
  ii. Higdon ABC Parameter 1 and parameter 2 are the values for the angle of incidence
                ( in degrees ) at which perfect absorption may be expected
  iii. PML Parameter 1 is the number of layers in the PML region, parameter 2 is
          the grading index, normally 2, parameter 3 is the minimum reflection
         coefficient, try 0.01 - 0.001. This is not critical.
  '''
  def __init__(self):
    self.name = 'boundaries'
    self.layer = 'boundaries'
    self.group = 'boundaries'

    # PML=10, symmetry=1, normal=2
    self.Xpos_bc = 2
    self.Ypos_bc = 2
    self.Zpos_bc = 2
    self.Xneg_bc = 2
    self.Yneg_bc = 2
    self.Zneg_bc = 2

    self.Xpos_param = [1,1,0]
    self.Ypos_param = [1,1,0]
    self.Zpos_param = [1,1,0]
    self.Xneg_param = [1,1,0]
    self.Yneg_param = [1,1,0]
    self.Zneg_param = [1,1,0]
    
  def setBoundaryConditionsXposToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Xpos_bc = 10
    self.Xpos_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsYposToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Ypos_bc = 10
    self.Ypos_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsZposToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Zpos_bc = 10
    self.Zpos_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsXnegToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Xneg_bc = 10
    self.Xneg_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsYnegToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Yneg_bc = 10
    self.Yneg_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsZnegToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.Zneg_bc = 10
    self.Zneg_param = [ number_of_layers, grading_index, min_reflection_coeff ]
  def setBoundaryConditionsToPML(self, number_of_layers=8, grading_index=2, min_reflection_coeff=1e-3):
    self.setBoundaryConditionsXnegToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsYnegToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsZnegToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsXposToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsYposToPML(number_of_layers, grading_index, min_reflection_coeff)
    self.setBoundaryConditionsZposToPML(number_of_layers, grading_index, min_reflection_coeff)
      
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'X+: Type = '+str(self.Xpos_bc)+' parameters = '+str(self.Xpos_param)+'\n'
    ret += 'Y+: Type = '+str(self.Ypos_bc)+' parameters = '+str(self.Ypos_param)+'\n'
    ret += 'Z+: Type = '+str(self.Zpos_bc)+' parameters = '+str(self.Zpos_param)+'\n'
    ret += 'X-: Type = '+str(self.Xneg_bc)+' parameters = '+str(self.Xneg_param)+'\n'
    ret += 'Y-: Type = '+str(self.Yneg_bc)+' parameters = '+str(self.Yneg_param)+'\n'
    ret += 'Z-: Type = '+str(self.Zneg_bc)+' parameters = '+str(self.Zneg_param)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    i = 0
    if len(entry.data) == 6:
      self.Xpos_bc = int(entry.data[i]); self.Xpos_param = float_array([1,1,0]); i+=1
      self.Ypos_bc = int(entry.data[i]); self.Ypos_param = float_array([1,1,0]); i+=1
      self.Zpos_bc = int(entry.data[i]); self.Zpos_param = float_array([1,1,0]); i+=1
      self.Xneg_bc = int(entry.data[i]); self.Xneg_param = float_array([1,1,0]); i+=1
      self.Yneg_bc = int(entry.data[i]); self.Yneg_param = float_array([1,1,0]); i+=1
      self.Zneg_bc = int(entry.data[i]); self.Zneg_param = float_array([1,1,0]); i+=1
    elif len(entry.data) == 24:
      self.Xpos_bc = int(entry.data[4*i]); self.Xpos_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Ypos_bc = int(entry.data[4*i]); self.Ypos_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Zpos_bc = int(entry.data[4*i]); self.Zpos_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Xneg_bc = int(entry.data[4*i]); self.Xneg_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Yneg_bc = int(entry.data[4*i]); self.Yneg_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
      self.Zneg_bc = int(entry.data[4*i]); self.Zneg_param = float_array(entry.data[1+4*i:4+4*i]); i+=1
    else:
      print('ERROR: incorrect number of elements in boundary object')
      sys.exit(-1)
    return(0)
  def write_entry(self, FILE):
    FILE.write('BOUNDARY  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%d %E %E %E **X+\n" % (self.Xpos_bc, self.Xpos_param[0], self.Xpos_param[1], self.Xpos_param[2]))
    FILE.write("%d %E %E %E **Y+\n" % (self.Ypos_bc, self.Ypos_param[0], self.Ypos_param[1], self.Ypos_param[2]))
    FILE.write("%d %E %E %E **Z+\n" % (self.Zpos_bc, self.Zpos_param[0], self.Zpos_param[1], self.Zpos_param[2]))
    FILE.write("%d %E %E %E **X-\n" % (self.Xneg_bc, self.Xneg_param[0], self.Xneg_param[1], self.Xneg_param[2]))
    FILE.write("%d %E %E %E **Y-\n" % (self.Yneg_bc, self.Yneg_param[0], self.Yneg_param[1], self.Yneg_param[2]))
    FILE.write("%d %E %E %E **Z-\n" % (self.Zneg_bc, self.Zneg_param[0], self.Zneg_param[1], self.Zneg_param[2]))
    FILE.write('}\n')
    FILE.write('\n')

class Box(object):
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    lower = None,
    upper = None):

    if name is None: name = 'box'
    if layer is None: layer = 'box',
    if group is None: group = 'box',
    if lower is None: lower = numpy.array([0,0,0])
    if upper is None: upper = numpy.array([1,1,1])
    
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
  def setLower(self,lower):
    self.lower = numpy.array(lower)
  def setUpper(self,upper):
    self.upper = numpy.array(upper)
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.lower = float_array(entry.data[0:3])
    self.upper = float_array(entry.data[3:6])
  def write_entry(self, FILE):
    self.lower, self.upper = fixLowerUpper(self.lower, self.upper)
    FILE.write('BOX  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XL\n" % self.lower[0])
    FILE.write("%E **YL\n" % self.lower[1])
    FILE.write("%E **ZL\n" % self.lower[2])
    FILE.write("%E **XU\n" % self.upper[0])
    FILE.write("%E **YU\n" % self.upper[1])
    FILE.write("%E **ZU\n" % self.upper[2])
    FILE.write('}\n')
    FILE.write('\n')

  def translate(self, vec3):
    self.lower = numpy.array(self.lower)
    self.upper = numpy.array(self.upper)
    self.lower = self.lower + vec3
    self.upper = self.upper + vec3

  def getCentro(self):
    return numpy.array([ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ])
  def setCentro(self, nova_centro):
    nova_centro = numpy.array(nova_centro)    
    nuna_centro = self.getCentro()
    self.translate(nova_centro - nuna_centro)
    
  def getSize(self):
    return numpy.array(self.upper)-numpy.array(self.lower)
  def setSize(self, size_vec3):
    C = self.getCentro()
    self.lower = C - 0.5*numpy.array(size_vec3)
    self.upper = C + 0.5*numpy.array(size_vec3)
    return
    
  # convenience get functions, to get numpy arrays directly
  def getLower(self):
    return numpy.array(self.lower)
  def getUpper(self):
    return numpy.array(self.upper)

# geometry objects
class Geometry_object(object):
  def __init__(self):
    self.name = 'geometry object'
    self.rotation_list = []
    self.meshing_parameters = MeshingParameters()
    self.permittivity = 1
    self.conductivity = 0
  def __str__(self):
    ret = '--->object rotation_list'
    for i in range(len(self.rotation_list)):
      ret += '\n'
      ret += '-->object rotation '+str(i)+':\n'
      ret += self.rotation_list[i].__str__()
    return(ret)
  def setRefractiveIndex(self,n):
    self.permittivity = pow(n,2)
    self.conductivity = 0

  def getRefractiveIndex(self,n):
    # TODO: Use conductivity?
    return numpy.sqrt(self.permittivity)
    
  # this function requires the child objects to define a getCentro() and translate() method
  def setCentro(self, nova_centro):
    nova_centro = numpy.array(nova_centro)    
    nuna_centro = self.getCentro()
    self.translate(nova_centro - nuna_centro)

class Sphere(Geometry_object):
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    centre = None,
    outer_radius = None,
    inner_radius = None,
    permittivity = None,
    conductivity = None):

    if name is None: name = 'sphere'
    if layer is None: layer = 'sphere'
    if group is None: group = 'sphere'
    if centre is None: centre = [0,0,0]
    if outer_radius is None: outer_radius = 0.5
    if inner_radius is None: inner_radius = 0
    if permittivity is None: permittivity = 1
    if conductivity is None: conductivity = 0

    Geometry_object.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.centre = centre
    self.outer_radius = outer_radius
    self.inner_radius = inner_radius
    self.permittivity = permittivity
    self.conductivity = conductivity
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'centre = ' + str(self.centre) + '\n' +\
    'outer_radius = ' + str(self.outer_radius) + '\n' +\
    'inner_radius = ' + str(self.inner_radius) + '\n' +\
    'permittivity = ' + str(self.permittivity) + '\n' +\
    'conductivity = ' + str(self.conductivity)+'\n'
    ret += Geometry_object.__str__(self)
    return ret

  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.centre = float_array([entry.data[0],entry.data[1],entry.data[2]])
    self.outer_radius = float(entry.data[3])
    self.inner_radius = float(entry.data[4])
    self.permittivity = float(entry.data[5])
    self.conductivity = float(entry.data[6])
    return(0)
    
  def write_entry(self, FILE):
    ''' sphere
    {
     1-5 Coordinates of the sphere ( xc yc zc r1 r2 )
     6 permittivity
     7 conductivity
    } '''
    FILE.write('SPHERE  **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XC\n" % self.centre[0])
    FILE.write("%E **YC\n" % self.centre[1])
    FILE.write("%E **ZC\n" % self.centre[2])
    FILE.write("%E **outer_radius\n" % self.outer_radius)
    FILE.write("%E **inner_radius\n" % self.inner_radius)
    FILE.write("%E **relative permittivity\n" % self.permittivity)
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')

  def getCentro(self):
    return numpy.array(self.centre)
    
  def translate(self, vec3):
    self.centre = numpy.array(self.centre)
    self.centre = self.centre + vec3

class Block(Geometry_object):
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    lower = None,
    upper = None,
    permittivity = None,
    conductivity = None):

    if name is None: name = 'block'
    if layer is None: layer = 'block'
    if group is None: group = 'block'
    if lower is None: lower = [0,0,0]
    if upper is None: upper = [1,1,1]
    if permittivity is None: permittivity = 1 # vacuum by default
    if conductivity is None: conductivity = 0
  
    Geometry_object.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
    self.permittivity = permittivity
    self.conductivity = conductivity
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += Geometry_object.__str__(self)
    return ret
    
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.lower = float_array(entry.data[0:3])
    self.upper = float_array(entry.data[3:6])
    self.permittivity = float(entry.data[6])
    self.conductivity = float(entry.data[7])
    
  def write_entry(self, FILE):
    self.lower, self.upper = fixLowerUpper(self.lower, self.upper)
    FILE.write('BLOCK **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **XL\n" % self.lower[0])
    FILE.write("%E **YL\n" % self.lower[1])
    FILE.write("%E **ZL\n" % self.lower[2])
    FILE.write("%E **XU\n" % self.upper[0])
    FILE.write("%E **YU\n" % self.upper[1])
    FILE.write("%E **ZU\n" % self.upper[2])
    FILE.write("%E **relative permittivity\n" % self.permittivity)
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')
    
  def getCentro(self):
    return numpy.array([ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ])
    
  def translate(self, vec3):
    self.lower = numpy.array(self.lower)
    self.upper = numpy.array(self.upper)
    self.lower = self.lower + vec3
    self.upper = self.upper + vec3
  
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.lower[0],self.upper[0]])
    objy = numpy.sort([self.lower[1],self.upper[1]])
    objz = numpy.sort([self.lower[2],self.upper[2]])
    eps = self.permittivity
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz
    
  def getSize(self):
    return abs(numpy.array(self.upper)-numpy.array(self.lower))

  def setSize(self, size_vec3):
    C = self.getCentro()
    self.lower = C - 0.5*numpy.array(size_vec3)
    self.upper = C + 0.5*numpy.array(size_vec3)
    return

class Distorted(Geometry_object):
  '''
  0,1,2,3 = top face numbered clockwise viewed from outside
  4,5,6,7 = bottom face numbered clockwise viewed from outside
  3 connected to 4
  2 connected to 5
  0 connected to 7
  1 connected to 6
  Normal faces viewed from outside:
    [3,2,1,0]
    [7,6,5,4]
    [0,1,6,7]
    [1,2,5,6]
    [2,3,4,5]
    [3,0,7,4]
  '''
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    vertices = None,
    permittivity = None,
    conductivity = None):

    if name is None: name = 'distorted'
    if layer is None: layer = 'distorted',
    if group is None: group = 'distorted',
    if vertices is None: vertices = [[1,0,1],[0,0,1],[0,1,1],[1,1,1],[1,1,0],[0,1,0],[0,0,0],[1,0,0]]
                                   #0        1       2       3       4       5        6      7
    if permittivity is None: permittivity = 1 # vacuum by default
    if conductivity is None: conductivity = 0
    
    Geometry_object.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.vertices = vertices
    self.permittivity = permittivity
    self.conductivity = conductivity
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'vertices = '+str(self.vertices)+'\n'
    ret += 'permittivity = '+str(self.permittivity)+'\n'
    ret += 'conductivity = '+str(self.conductivity)+'\n'
    ret += Geometry_object.__str__(self)
    return ret
    
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    for i in range(8):
      self.vertices[i] = float_array(entry.data[3*i:3*i+3])
    self.permittivity = float(entry.data[8*3])
    self.conductivity = float(entry.data[8*3+1])
    
  def write_entry(self, FILE):
    FILE.write('DISTORTED **name='+self.name+'\n')
    FILE.write('{\n')
    for i in range(len(self.vertices)):
      FILE.write("%E **XV%d\n" % (self.vertices[i][0],i) )
      FILE.write("%E **YV%d\n" % (self.vertices[i][1],i) )
      FILE.write("%E **ZV%d\n" % (self.vertices[i][2],i) )
    FILE.write("%E **relative permittivity\n" % self.permittivity)
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write('}\n')
    FILE.write('\n')
    
  def translate(self, vec3):
    for i in range(len(self.vertices)):
      self.vertices[i] = numpy.array(self.vertices[i]) + numpy.array(vec3)
  
  def getCentro(self):
    S = numpy.array([0,0,0])
    for v in self.vertices:
      #print('S='+str(S)+' + v='+str(v))
      S = S + numpy.array(v)
      #print('= S='+str(S))
    return 1./len(self.vertices)*S
    
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    # TODO: improve meshing system + add support for rotations
    
    # determine lower and upper points of distorted object
    vertex_min = numpy.array(self.vertices[0])
    vertex_max = numpy.array(self.vertices[0])
    for vertex in self.vertices:
      #print('vertex = '+str(vertex))
      for i in range(3):
        if vertex[i]<vertex_min[i]: vertex_min[i] = vertex[i]
        if vertex[i]>vertex_max[i]: vertex_max[i] = vertex[i]
    
    #print('vertex_min = '+str(vertex_min))
    #print('vertex_max = '+str(vertex_max))
    
    objx = numpy.sort([vertex_min[0],vertex_max[0]])
    objy = numpy.sort([vertex_min[1],vertex_max[1]])
    objz = numpy.sort([vertex_min[2],vertex_max[2]])
    eps = self.permittivity
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz

class Cylinder(Geometry_object):
  def __init__(self,
    name = None,
    centre = None,
    inner_radius = None,
    outer_radius = None,
    height = None,
    permittivity = None,
    conductivity = None,
    angle_deg = None,
    layer = None,
    group = None):

    if name is None: name = 'cylinder'
    if centre is None: centre = [0,0,0]
    if inner_radius is None: inner_radius = 0
    if outer_radius is None: outer_radius = 0.5
    if height is None: height = 1
    if permittivity is None: permittivity = 0
    if conductivity is None: conductivity = 0
    if angle_deg is None: angle_deg = 0
    if layer is None: layer = 'cylinder'
    if group is None: group = 'cylinder'
    
    Geometry_object.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.centre = centre
    self.inner_radius = inner_radius
    self.outer_radius = outer_radius
    self.height = height
    self.permittivity = permittivity
    self.conductivity = conductivity
    self.angle_deg = angle_deg
  
  def getLower(self):
    return [self.centre[0]-self.outer_radius,self.centre[1]-0.5*self.height,self.centre[2]-self.outer_radius]
  def getUpper(self):
    return [self.centre[0]+self.outer_radius,self.centre[1]+0.5*self.height,self.centre[2]+self.outer_radius]
  
  def setDiametre(self,diametre):
    self.outer_radius = 0.5*diametre

  def getCentro(self):
    return numpy.array(self.centre)
    
  def translate(self, vec3):
    self.centre = numpy.array(self.centre)
    self.centre = self.centre + vec3
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'centre = ' + str(self.centre) + '\n' +\
    'inner_radius = ' + str(self.inner_radius) + '\n' +\
    'outer_radius = ' + str(self.outer_radius) + '\n' +\
    'height = ' + str(self.height) + '\n' +\
    'permittivity = ' + str(self.permittivity) + '\n' +\
    'conductivity = ' + str(self.conductivity) + '\n' +\
    'angle_deg = ' + str(self.angle_deg) + '\n'
    ret += Geometry_object.__str__(self)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.centre = float_array([entry.data[0],entry.data[1],entry.data[2]])
    self.inner_radius = float(entry.data[3])
    self.outer_radius = float(entry.data[4])
    self.height = float(entry.data[5])
    self.permittivity = float(entry.data[6])
    self.conductivity = float(entry.data[7])
    if(len(entry.data)>8): self.angle_deg = float(entry.data[8])
    return(0)
  def write_entry(self, FILE):
    ''' # cylinder
    # {
    # 1-7 Coordinates of the material volume ( xc yc zc r1 r2 h )
    # 7 permittivity
    # 8 conductivity
    # 9 angle_deg of inclination
    # }
    # xc, yc and zc are the coordinates of the centre of the cylinder. r1 and r2 are the inner and outer
    # radius respectively, h is the cylinder height, is the angle_deg of inclination. The cylinder is aligned
    # with the y direction if =0 and with the x direction if =90
    #
    # i.e. angle_deg = Angle of rotation in degrees around -Z=(0,0,-1) '''
  
    FILE.write('CYLINDER **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **X CENTRE\n" % self.centre[0])
    FILE.write("%E **Y CENTRE\n" % self.centre[1])
    FILE.write("%E **Z CENTRE\n" % self.centre[2])
    FILE.write("%E **inner_radius\n" % self.inner_radius)
    FILE.write("%E **outer_radius\n" % self.outer_radius)
    FILE.write("%E **HEIGHT\n" % self.height)
    FILE.write("%E **relative permittivity\n" % self.permittivity)
    FILE.write("%E **relative conductivity\n" % self.conductivity)
    FILE.write("%E **Angle of rotation in degrees around -Z=(0,0,-1)\n" % self.angle_deg)
    FILE.write('}\n')
    FILE.write('\n')

  # TODO: take inner_radius into account, create 4 square meshing regions, implement per object meshing finesse (for all object types)
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.centre[0]-self.outer_radius,self.centre[0]+self.outer_radius])
    objy = numpy.sort([self.centre[1]-0.5*self.height,self.centre[1]+0.5*self.height])
    objz = numpy.sort([self.centre[2]-self.outer_radius,self.centre[2]+self.outer_radius])
    eps = self.permittivity
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz
    
  def getSize(self):
    # TODO: Take rotations into account?
    return numpy.array([2*self.outer_radius, self.height, 2*self.outer_radius])

# TODO: meshing params in case of rotations
class Rotation(object):
  def __init__(self,
      name = None,
      axis_point = None,
      axis_direction = None,
      angle_degrees = None):
      
    if name is None: name = 'rotation'
    if axis_point is None: axis_point = [0,0,0]
    if axis_direction is None: axis_direction = [0,0,0]
    if angle_degrees is None: angle_degrees = 0
    
    self.name = name
    self.axis_point = axis_point
    self.axis_direction = axis_direction
    self.angle_degrees = angle_degrees
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'axis_point = ' + str(self.axis_point) + '\n'
    ret += 'axis_direction = ' + str(self.axis_direction) + '\n'
    ret += 'angle_degrees = ' + str(self.angle_degrees)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.axis_point = float_array(entry.data[0:3])
    self.axis_direction = float_array(entry.data[3:6])
    self.angle_degrees = float(entry.data[6])
  def write_entry(self, FILE):
    # rotation structure. Actually affects previous geometry object in Prof. Railton's modified BrisFDTD. Not fully implemented yet.
    # Should be integrated into existing structures using a directional vector anyway, like in MEEP. BrisFDTD hacking required... :)
    FILE.write('ROTATION **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **X axis_point\n" % self.axis_point[0])
    FILE.write("%E **Y axis_point\n" % self.axis_point[1])
    FILE.write("%E **Z axis_point\n" % self.axis_point[2])
    FILE.write("%E **X axis_direction\n" % self.axis_direction[0])
    FILE.write("%E **Y axis_direction\n" % self.axis_direction[1])
    FILE.write("%E **Z axis_direction\n" % self.axis_direction[2])
    FILE.write("%E **angle_degrees\n" % self.angle_degrees)
    FILE.write('}\n')
    FILE.write('\n')

# measurement objects
class Time_snapshot(object):
  '''
  One or more field components may be sampled over a specified plane in the structure after a specified number of iterations.
  It is possible to take snapshots after every “n” iterations by setting the “iterations between snapshots” parameter to “n”.
  
  For each snapshot requested a file is produced in one of two formats:
  
  * List format which has a filename of the form “x1idaa.prn”, where “x” is the plane over
  which the snapshot has been taken, “1"is the snapshot serial number. ie. the snaps are numbered in the order which
  they appear in the input file.. “id” in an identifier specified in the “flags” object. “aa" is the time serial number ie.
  if snapshots are asked for at every 100 iterations then the first one will have “aa, the second one “ab" etc
  The file consists of a single header line followed by columns of numbers, one for each field component wanted and
  two for the coordinates of the point which has been sampled. These files can be read into Gema.
  
  * Matrix format for each snapshot a file is produced for each requested field component with a name of the form
  “x1idaa_ex” where the “ex” is the field component being sampled. The rest of the filename is tha same as for the list
  format case. The file consists of a matrix of numbers the first column and first row or which, gives the position of
  the sample points in each direction. These files can be read into MathCad or to spreadsheet programs.
  
  The format of the snapshot object is as follows:
  
  1)first: iteration number for the first snapshot
  2)repetition: number of iterations between snapshots
  3)plane: 1=x,2=y,3=z
  4-9)P1,P2: coordinates of the lower left and top right corners of the plane P1(x1,y1,z1), P2(x2,y2,z2)
  10-18)E,H,J: field components to be sampled E(Ex,Ey,Ez), H(Hx,Hy,Hz), J(Jx,Jy,Jz)
  19)power: print power? =0/1
  20)eps: create EPS (->epsilon->refractive index) snapshot? =0/1
  21)???: write an output file in “list” format (NOT IMPLEMENTED YET)(default is list format)
  22)???: write an output file in “matrix” format (NOT IMPLEMENTED YET)
  
  Mode filtered probe files (Requires a template for the first excitation object!):
  =================================================================================
  Mode filtered probe files are specified in the same way as a snapshot across the reference plane except that no field components are selected, i.e. E=H=J=power=eps=(0,0,0).
  In addition, the "repetition" parameter takes the role which the "step" parameter does on normal probes.
  
  The output will have the same form as a probe file and will consist of the inner product at each time step of the field distribution across the reference plane with the template specified for the first excitation object.
  This template will normally be the wanted mode of the guiding structure and, thus, the output of this probe will be the amplitude of just this mode.

  The effect of this is that the amplitude of the mode of interest is sampled across the whole waveguide cross-section.
  If a normal field probe had been used, then the unwanted effects of other modes would cause inaccuracies in the final result.
  '''
  def __init__(self,
    name = None,
    first = None,
    repetition = None,
    plane = None,
    P1 = None,
    P2 = None,
    E = None,
    H = None,
    J = None,
    power = None,
    eps = None,
    layer = None,
    group = None):

    if name is None: name = 'time_snapshot'
    if first is None: first = 1 # crashes if = 0
    if repetition is None: repetition = 524200
    if plane is None: plane = 1 #1,2,3 for x,y,z
    if P1 is None: P1 = [0,0,0]
    if P2 is None: P2 = [0,1,1]
    if E is None: E = [1,1,1]
    if H is None: H = [1,1,1]
    if J is None: J = [0,0,0]
    if power is None: power = 0
    if eps is None: eps = 0
    if layer is None: layer = 'time_snapshot'
    if group is None: group = 'time_snapshot'
  
    self.name = name
    self.layer = layer
    self.group = group
    self.first = first
    self.repetition = repetition
    self.plane = plane
    self.P1 = P1
    self.P2 = P2
    self.E = E
    self.H = H
    self.J = J
    self.power = power
    self.eps = eps
    
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'first = ' + str(self.first) + '\n' +\
    'repetition = ' + str(self.repetition) + '\n' +\
    'plane = ' + str(self.plane) + '\n' +\
    'P1 = ' + str(self.P1) + '\n' +\
    'P2 = ' + str(self.P2) + '\n' +\
    'E = ' + str(self.E) + '\n' +\
    'H = ' + str(self.H) + '\n' +\
    'J = ' + str(self.J) + '\n' +\
    'power = ' + str(self.power) + '\n' +\
    'eps = ' + str(self.eps)
    return ret
    
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    idx = 0
    if entry.name:
      self.name = entry.name
    self.first = float(entry.data[idx]); idx = idx+1
    self.repetition = float(entry.data[idx]); idx = idx+1
    self.plane = int(float(entry.data[idx])); idx = idx+1
    self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.power = float(entry.data[idx]); idx = idx+1
    if(len(entry.data)>idx): self.eps = int(float(entry.data[idx])); idx = idx+1
    return(0)
    
  def write_entry(self, FILE):
    self.P1, self.P2 = fixLowerUpper(self.P1, self.P2)
  
    def snapshot(plane,P1,P2):
      plane_ID, plane_name = planeNumberName(plane)
    
      FILE.write('SNAPSHOT **name='+self.name+'\n')
      FILE.write('{\n')
  
      FILE.write("%d **FIRST\n" % self.first)
      FILE.write("%d **REPETITION\n" % self.repetition)
      FILE.write("%d **PLANE %s\n" % (plane_ID, plane_name))
      FILE.write("%E **X1\n" % P1[0])
      FILE.write("%E **Y1\n" % P1[1])
      FILE.write("%E **Z1\n" % P1[2])
      FILE.write("%E **X2\n" % P2[0])
      FILE.write("%E **Y2\n" % P2[1])
      FILE.write("%E **Z2\n" % P2[2])
      FILE.write("%d **EX\n" % self.E[0])
      FILE.write("%d **EY\n" % self.E[1])
      FILE.write("%d **EZ\n" % self.E[2])
      FILE.write("%d **HX\n" % self.H[0])
      FILE.write("%d **HY\n" % self.H[1])
      FILE.write("%d **HZ\n" % self.H[2])
      FILE.write("%d **JX\n" % self.J[0])
      FILE.write("%d **JY\n" % self.J[1])
      FILE.write("%d **JZ\n" % self.J[2])
      FILE.write("%d **POW\n" % self.power)
      FILE.write("%d **EPS\n" % self.eps)
      FILE.write('}\n')
  
      FILE.write('\n')
  
    plane_ID, plane_name = planeNumberName(self.plane)
    if self.P1[plane_ID-1] == self.P2[plane_ID-1]:
      snapshot(plane_ID,self.P1,self.P2)
    else:
      snapshot(1,[self.P1[0],self.P1[1],self.P1[2]],[self.P1[0],self.P2[1],self.P2[2]])
      snapshot(1,[self.P2[0],self.P1[1],self.P1[2]],[self.P2[0],self.P2[1],self.P2[2]])
      snapshot(2,[self.P1[0],self.P1[1],self.P1[2]],[self.P2[0],self.P1[1],self.P2[2]])
      snapshot(2,[self.P1[0],self.P2[1],self.P1[2]],[self.P2[0],self.P2[1],self.P2[2]])
      snapshot(3,[self.P1[0],self.P1[1],self.P1[2]],[self.P2[0],self.P2[1],self.P1[2]])
      snapshot(3,[self.P1[0],self.P1[1],self.P2[2]],[self.P2[0],self.P2[1],self.P2[2]])
      
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.P1[0],self.P2[0]])
    objy = numpy.sort([self.P1[1],self.P2[1]])
    objz = numpy.sort([self.P1[2],self.P2[2]])
    eps = 1
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz
  
class ModeFilteredProbe(Time_snapshot):
  def __init__(self,
      name = None,
      first = None,
      repetition = None,
      plane = None,
      P1 = None,
      P2 = None,
      layer = None,
      group = None):

    if name is None: name = 'mode_filtered_probe'
    if first is None: first = 1 # crashes if = 0
    if repetition is None: repetition = 10
    if plane is None: plane = 1 #1,2,3 for x,y,z
    if P1 is None: P1 = [0,0,0]
    if P2 is None: P2 = [0,1,1]
    if layer is None: layer = 'mode_filtered_probe'
    if group is None: group = 'mode_filtered_probe'
    
    Time_snapshot.__init__(self, name = name, first = first, repetition = repetition, plane = plane, P1 = P1, P2 = P2, layer = layer, group = group)
    self.E = [0,0,0]
    self.H = [0,0,0]
    self.J = [0,0,0]
    self.power = 0
    self.eps = 0

class EpsilonSnapshot(Time_snapshot):
  def __init__(self,
      name = None,
      first = None,
      repetition = None,
      plane = None,
      P1 = None,
      P2 = None,
      layer = None,
      group = None):

    if name is None: name = 'epsilon_snapshot'
    if first is None: first = 1 # crashes if = 0
    if repetition is None: repetition = 1
    if plane is None: plane = 1 #1,2,3 for x,y,z
    if P1 is None: P1 = [0,0,0]
    if P2 is None: P2 = [0,1,1]
    if layer is None: layer = 'epsilon_snapshot'
    if group is None: group = 'epsilon_snapshot'
    
    Time_snapshot.__init__(self, name = name, first = first, repetition = repetition, plane = plane, P1 = P1, P2 = P2, layer = layer, group = group)
    self.E = [0,0,0]
    self.H = [0,0,0]
    self.J = [0,0,0]
    self.power = 0
    self.eps = 1
  
class Frequency_snapshot(object):
  '''
  The format of a frequency snapshot object is:
  
  1)first: iteration number for the first snapshot
  2)repetition: number of iterations between snapshots
  3)interpolate:
  If set to 1 : the H field samples are interpolated to give the value at the plane of the E field nodes
  If set to 2 : as above but the field values are multiplied by the area of the cell on the plane and interpolated
  to the centre of the square in the plane of the E field nodes..
  If set to 3 : as above but the order of the field components in the output file is changed so that for the x,y
  and z planes the order is (yzx), (zxy) and (xyz) respectively instead of always being (xyz)
  If set to 4 : as for 2 except that all 3 coordinates are given for each point
  4)real_dft: Set this if it is not required to write the imaginary component to file
  5)mod_only: Write only the modulus to file
  6)mod_all: Write the modulus AND the real and imaginary parts to file
  7)plane: 0=all, 1=x, 2=y, 3=z
  8-13)P1,P2: coordinates of the lower left and top right corners of the plane P1(x1,y1,z1), P2(x2,y2,z2)
  14)frequency_vector: frequency (in MHz! ). Will create a frequency snapshot for each frequency in the list/vector
  15)starting_sample: iteration number at which to start the running fourier transforms
  16-24)E,H,J: field components to be sampled E(Ex,Ey,Ez), H(Hx,Hy,Hz), J(Jx,Jy,Jz)
  
  The output file is of the same format as the snapshot “list format” and the naming is the same except that the time serial number starts at “00" instead of “aa”.
  '''
  # TODO: Change frequency_vector to frequency_vector_Mhz?
  def __init__(self,
    name = None,
    first = None,
    repetition = None,
    interpolate = None,
    real_dft = None,
    mod_only = None,
    mod_all = None,
    plane = None,
    P1 = None,
    P2 = None,
    frequency_vector = None,
    starting_sample = None,
    E = None,
    H = None,
    J = None,
    layer = None,
    group = None):

    if name is None: name = 'frequency_snapshot'
    if first is None: first = 1 # crashes if = 0
    if repetition is None: repetition = 524200
    if interpolate is None: interpolate = 1
    if real_dft is None: real_dft = 0
    if mod_only is None: mod_only = 0
    if mod_all is None: mod_all = 1
    if plane is None: plane = 1 #1,2,3 for x,y,z
    if P1 is None: P1 = [0,0,0]
    if P2 is None: P2 = [0,1,1]
    if frequency_vector is None: frequency_vector = [0]
    if starting_sample is None: starting_sample = 0
    if E is None: E = [1,1,1]
    if H is None: H = [1,1,1]
    if J is None: J = [0,0,0]
    if layer is None: layer = 'frequency_snapshot'
    if group is None: group = 'frequency_snapshot'
    
    self.name = name
    self.layer = layer
    self.group = group
    self.first = first
    self.repetition = repetition
    self.interpolate = interpolate
    self.real_dft = real_dft
    self.mod_only = mod_only
    self.mod_all = mod_all
    self.plane = plane
    self.P1 = P1
    self.P2 = P2
    self.frequency_vector = frequency_vector
    self.starting_sample = starting_sample
    self.E = E
    self.H = H
    self.J = J
  
  def getLambda(self):
    return get_c0()/numpy.array(self.frequency_vector)
  
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'first = ' + str(self.first) + '\n' +\
    'repetition = ' + str(self.repetition) + '\n' +\
    'interpolate = ' + str(self.interpolate) + '\n' +\
    'real_dft = ' + str(self.real_dft) + '\n' +\
    'mod_only = ' + str(self.mod_only) + '\n' +\
    'mod_all = ' + str(self.mod_all) + '\n' +\
    'plane = ' + str(self.plane) + '\n' +\
    'P1 = ' + str(self.P1) + '\n' +\
    'P2 = ' + str(self.P2) + '\n' +\
    'frequency = ' + str(self.frequency_vector) + '\n' +\
    'starting_sample = ' + str(self.starting_sample) + '\n' +\
    'E = ' + str(self.E) + '\n' +\
    'H = ' + str(self.H) + '\n' +\
    'J = ' + str(self.J)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    idx = 0
    self.first = float(entry.data[idx]); idx = idx+1
    self.repetition = float(entry.data[idx]); idx = idx+1
    self.interpolate = float(entry.data[idx]); idx = idx+1
    self.real_dft = float(entry.data[idx]); idx = idx+1
    self.mod_only = float(entry.data[idx]); idx = idx+1
    self.mod_all = float(entry.data[idx]); idx = idx+1
    self.plane = int(float(entry.data[idx])); idx = idx+1
    self.P1 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.P2 = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.frequency_vector = [float(entry.data[idx])]; idx = idx+1
    self.starting_sample = float(entry.data[idx]); idx = idx+1
    self.E = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.H = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    self.J = float_array([entry.data[idx], entry.data[idx+1], entry.data[idx+2]]); idx = idx+3
    return(0)
  def write_entry(self, FILE):
    self.P1, self.P2 = fixLowerUpper(self.P1, self.P2)
  
    def snapshot(name,plane,P1,P2, frequency):
      plane_ID, plane_name = planeNumberName(plane)
      FILE.write('FREQUENCY_SNAPSHOT **name='+name+'\n')
      FILE.write('{\n')
      FILE.write("%d **FIRST\n" % self.first)
      FILE.write("%d **REPETITION\n" % self.repetition)
      FILE.write("%d **interpolate?\n" % self.interpolate)
      FILE.write("%d **REAL DFT\n" % self.real_dft)
      FILE.write("%d **MOD ONLY\n" % self.mod_only)
      FILE.write("%d **MOD ALL\n" % self.mod_all)
      FILE.write("%d **PLANE %s\n" % (plane_ID, plane_name))
      FILE.write("%E **X1\n" % P1[0])
      FILE.write("%E **Y1\n" % P1[1])
      FILE.write("%E **Z1\n" % P1[2])
      FILE.write("%E **X2\n" % P2[0])
      FILE.write("%E **Y2\n" % P2[1])
      FILE.write("%E **Z2\n" % P2[2])
      FILE.write("%E **FREQUENCY (MHz)\n" % frequency)
      FILE.write("%d **STARTING SAMPLE\n" % self.starting_sample)
      FILE.write("%d **EX\n" % self.E[0])
      FILE.write("%d **EY\n" % self.E[1])
      FILE.write("%d **EZ\n" % self.E[2])
      FILE.write("%d **HX\n" % self.H[0])
      FILE.write("%d **HY\n" % self.H[1])
      FILE.write("%d **HZ\n" % self.H[2])
      FILE.write("%d **JX\n" % self.J[0])
      FILE.write("%d **JY\n" % self.J[1])
      FILE.write("%d **JZ\n" % self.J[2])
      FILE.write('}\n')
      FILE.write('\n')
  
    plane_ID, plane_name = planeNumberName(self.plane)
    for i in range(len(self.frequency_vector)):
      if self.P1[plane_ID-1] == self.P2[plane_ID-1]:
        snapshot(self.name, plane_ID,self.P1,self.P2,self.frequency_vector[i])
      else:
        snapshot(self.name + ' X-', 1,[self.P1[0],self.P1[1],self.P1[2]],[self.P1[0],self.P2[1],self.P2[2]],self.frequency_vector[i])
        snapshot(self.name + ' X+', 1,[self.P2[0],self.P1[1],self.P1[2]],[self.P2[0],self.P2[1],self.P2[2]],self.frequency_vector[i])
        snapshot(self.name + ' Y-', 2,[self.P1[0],self.P1[1],self.P1[2]],[self.P2[0],self.P1[1],self.P2[2]],self.frequency_vector[i])
        snapshot(self.name + ' Y+', 2,[self.P1[0],self.P2[1],self.P1[2]],[self.P2[0],self.P2[1],self.P2[2]],self.frequency_vector[i])
        snapshot(self.name + ' Z-', 3,[self.P1[0],self.P1[1],self.P1[2]],[self.P2[0],self.P2[1],self.P1[2]],self.frequency_vector[i])
        snapshot(self.name + ' Z+', 3,[self.P1[0],self.P1[1],self.P2[2]],[self.P2[0],self.P2[1],self.P2[2]],self.frequency_vector[i])

  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.P1[0],self.P2[0]])
    objy = numpy.sort([self.P1[1],self.P2[1]])
    objz = numpy.sort([self.P1[2],self.P2[2]])
    eps = 1
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz

class Probe(object):
  '''
  The format of the probe object is as follows:
  
  1-3)position: Coordinates of the probe position(x,y,z)
  4)step: Samples may be taken at every time step, by setting the parameter “step” equal to 1, or after every n timesteps by setting “step” to the value “n”.
  5-13)E,H,J: Field components to be sampled: E(Ex,Ey,Ez), H(Hx,Hy,Hz), J(Jx,Jy,Jz)
  '''
  def __init__(self,
    position = [0,0,0],
    name = 'probe',
    step = 10,
    E = [1,1,1],
    H = [1,1,1],
    J = [0,0,0],
    power = 0,
    layer = 'probe',
    group = 'probe'):
        
    self.name = name
    self.layer = layer
    self.group = group
    self.position = position
    self.step = step
    self.E = E
    self.H = H
    self.J = J
    self.power = power
  
  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'position = ' + str(self.position) + '\n' +\
    'step = ' + str(self.step) + '\n' +\
    'E = ' + str(self.E) + '\n' +\
    'H = ' + str(self.H) + '\n' +\
    'J = ' + str(self.J) + '\n' +\
    'power = ' + str(self.power)
    return ret
  def read_entry(self,entry):
    if entry.name:
      self.name = entry.name
    self.position = float_array([entry.data[0],entry.data[1],entry.data[2]])
    self.step = float(entry.data[3])
    self.E = float_array([entry.data[4],entry.data[5],entry.data[6]])
    self.H = float_array([entry.data[7],entry.data[8],entry.data[9]])
    self.J = float_array([entry.data[10],entry.data[11],entry.data[12]])
    self.power = float(entry.data[13])
  def write_entry(self, FILE):
    FILE.write('PROBE **name='+self.name+'\n')
    FILE.write('{\n')
    FILE.write("%E **X\n" % self.position[0])
    FILE.write("%E **Y\n" % self.position[1])
    FILE.write("%E **Z\n" % self.position[2])
    FILE.write("%d **STEP\n" % self.step)
    FILE.write("%d **EX\n" % self.E[0])
    FILE.write("%d **EY\n" % self.E[1])
    FILE.write("%d **EZ\n" % self.E[2])
    FILE.write("%d **HX\n" % self.H[0])
    FILE.write("%d **HY\n" % self.H[1])
    FILE.write("%d **HZ\n" % self.H[2])
    FILE.write("%d **JX\n" % self.J[0])
    FILE.write("%d **JY\n" % self.J[1])
    FILE.write("%d **JZ\n" % self.J[2])
    FILE.write("%d **POW\n" % self.power)
    FILE.write('}\n')
    FILE.write('\n')

  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([0,self.position[0]])
    objy = numpy.sort([0,self.position[1]])
    objz = numpy.sort([0,self.position[2]])
    eps = 1
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,eps])
    epsy = numpy.vstack([epsy,eps])
    epsz = numpy.vstack([epsz,eps])
    return xvec,yvec,zvec,epsx,epsy,epsz

class Entry(object):
  def __init__(self):
    self.name = 'default_entry'
    self.layer = 'default_layer'
    self.scene = 'default_scene'
    self.group = 'default_group'
    self.Type = ''
    self.data = []

# TODO: add addSnapshot, addProbe, etc functions to BFDTDobject to make adding stuff easier (should copy value from last similar)
# TODO: beware of the multiple snapshot lists! reduce duplicate info and add set/get functions
# TODO: implement "orientation" thingie from triangular_prism.py to easily exchange axes.
class BFDTDobject(object):
  def __init__(self):
    # mandatory objects
    self.mesh = MeshObject()
    self.flag = Flag()
    self.boundaries = Boundaries()
    self.box = Box()
    
    # geometry objects
    self.geometry_object_list = []
    self.sphere_list = []
    self.block_list = []
    self.distorted_list = []
    self.cylinder_list = []
    self.global_rotation_list = []
    
    # excitation objects
    self.excitation_list = []
    
    # measurement objects
    self.measurement_object_list = [] # TODO: make sure fully unused + not necessary and remove? use subclasses, etc...
    self.snapshot_list = []
    self.time_snapshot_list = []
    self.frequency_snapshot_list = []
    self.probe_list = []

    # excitation template list
    self.excitation_template_list = []
    self.mesh_object_list = []

    # special
    self.fileList = []
    
    
    # excitation object meshes
    self.fitMeshToExcitations = True
    self.fitMeshToProbes = False
    self.fitMeshToSnapshots = False
    
    self.verboseMeshing = False
    
    self.verbosity = 1
    
  def __str__(self):
      ret = '--->snapshot_list\n'
      for i in range(len(self.snapshot_list)):
          ret += '-->snapshot '+str(i)+':\n'
          ret += self.snapshot_list[i].__str__()+'\n'

      ret += '--->time_snapshot_list\n'
      for i in range(len(self.time_snapshot_list)):
          ret += '-->time_snapshot '+str(i)+':\n'
          ret += self.time_snapshot_list[i].__str__()+'\n'

      ret += '--->frequency_snapshot_list\n'
      for i in range(len(self.frequency_snapshot_list)):
          ret += '-->frequency_snapshot '+str(i)+':\n'
          ret += self.frequency_snapshot_list[i].__str__()+'\n'

      ret += '--->excitation_list\n'
      for i in range(len(self.excitation_list)):
          ret += '-->excitation '+str(i)+':\n'
          ret += self.excitation_list[i].__str__()+'\n'
      
      ret += '--->delta_X_vector\n'+self.mesh.getXmeshDelta().__str__()+'\n'+\
      '--->delta_Y_vector\n'+self.mesh.getYmeshDelta().__str__()+'\n'+\
      '--->delta_Z_vector\n'+self.mesh.getZmeshDelta().__str__()+'\n'+\
      '--->flag\n'+self.flag.__str__()+'\n'+\
      '--->boundaries\n'+self.boundaries.__str__()+'\n'+\
      '--->box\n'+self.box.__str__()+'\n'
      
      ret += '--->probe_list\n'
      for i in range(len(self.probe_list)):
          ret += '-->probe '+str(i)+':\n'
          ret += self.probe_list[i].__str__()+'\n'

      ret += '--->sphere_list\n'
      for i in range(len(self.sphere_list)):
          ret += '-->sphere '+str(i)+':\n'
          ret += self.sphere_list[i].__str__()+'\n'
      
      ret += '--->block_list\n'
      for i in range(len(self.block_list)):
          ret += '-->block '+str(i)+':\n'
          ret += self.block_list[i].__str__()+'\n'

      ret += '--->distorted_list\n'
      for i in range(len(self.distorted_list)):
          ret += '-->distorted '+str(i)+':\n'
          ret += self.distorted_list[i].__str__()+'\n'

      ret += '--->cylinder_list\n'
      for i in range(len(self.cylinder_list)):
          ret += '-->cylinder '+str(i)+':\n'
          ret += self.cylinder_list[i].__str__()+'\n'

      ret += '--->global_rotation_list\n'
      for i in range(len(self.global_rotation_list)):
          # ret += '\n'
          ret += '-->rotation '+str(i)+':\n'
          ret += self.global_rotation_list[i].__str__()+'\n'

      ret += '--->geometry_object_list\n'
      for i in range(len(self.geometry_object_list)):
          ret += '-->geometry_object '+str(i)+':\n'
          ret += self.geometry_object_list[i].__str__()+'\n'
          
      return ret
  
  def getNcells(self):
    return self.mesh.getNcells()

  def addBoxFrequencySnapshots(self):
    L = [self.box.lower[0], self.box.lower[1], self.box.lower[2]]
    U = [self.box.upper[0], self.box.upper[1], self.box.upper[2]]
    F = Frequency_snapshot(name='Box frequency snapshot', P1=L, P2=U)
    self.snapshot_list.append(F)
    return F
  
  def addFrequencySnapshot(self, plane, position):
    if not isinstance(position,int) and not isinstance(position,float):
      print('ERROR: position argument is not int or float, but is '+str(type(position)))
      sys.exit(1)
    vec, alpha = getVecAlphaDirectionFromVar(plane)
    if alpha == 'x':
      name='X frequency snapshot'
      L = [position, self.box.lower[1], self.box.lower[2]]
      U = [position, self.box.upper[1], self.box.upper[2]]
    elif alpha == 'y':
      name='Y frequency snapshot'
      L = [self.box.lower[0], position, self.box.lower[2]]
      U = [self.box.upper[0], position, self.box.upper[2]]
    elif alpha == 'z':
      name='Z frequency snapshot'
      L = [self.box.lower[0], self.box.lower[1], position]
      U = [self.box.upper[0], self.box.upper[1], position]
    else:
      print(('ERROR: Invalid plane : ',plane))
      sys.exit(1)
    F = Frequency_snapshot(name=name, plane=plane, P1=L, P2=U)
    self.snapshot_list.append(F)
    return F
  
  def addTimeSnapshot(self, plane, position):
    if not isinstance(position,int) and not isinstance(position,float):
      print('ERROR: position argument is not int or float, but is '+str(type(position)))
      sys.exit(1)      
    vec, alpha = getVecAlphaDirectionFromVar(plane)
    if alpha == 'x':
      name='X Time snapshot'
      L = [position, self.box.lower[1], self.box.lower[2]]
      U = [position, self.box.upper[1], self.box.upper[2]]
    elif alpha == 'y':
      name='Y Time snapshot'
      L = [self.box.lower[0], position, self.box.lower[2]]
      U = [self.box.upper[0], position, self.box.upper[2]]
    elif alpha == 'z':
      name='Z Time snapshot'
      L = [self.box.lower[0], self.box.lower[1], position]
      U = [self.box.upper[0], self.box.upper[1], position]
    else:
      print(('ERROR: Invalid plane : ',plane))
      sys.exit(1)
    F = Time_snapshot(name=name, plane=plane, P1=L, P2=U)
    self.snapshot_list.append(F)
    return F

  def addModeFilteredProbe(self, plane, position):
    if not isinstance(position,int) and not isinstance(position,float):
      print('ERROR: position argument is not int or float, but is '+str(type(position)))
      sys.exit(1)      
    # TODO: use x,y,z or vectors wherever possible instead of 1,2,3/0,1,2 to avoid confusion
    # TODO: support multiple types for position argument (int/float or array)
    vec, alpha = getVecAlphaDirectionFromVar(plane)
    if alpha == 'x':
      name='X mode filtered probe'
      L = [position, self.box.lower[1], self.box.lower[2]]
      U = [position, self.box.upper[1], self.box.upper[2]]
      plane = 1
    elif alpha == 'y':
      name='Y mode filtered probe'
      L = [self.box.lower[0], position, self.box.lower[2]]
      U = [self.box.upper[0], position, self.box.upper[2]]
      plane = 2
    elif alpha == 'z':
      name='Z mode filtered probe'
      L = [self.box.lower[0], self.box.lower[1], position]
      U = [self.box.upper[0], self.box.upper[1], position]
      plane = 3
    else:
      print(('ERROR: Invalid plane : ',plane))
      sys.exit(1)
    F = ModeFilteredProbe(name=name, plane=plane, P1=L, P2=U)
    self.snapshot_list.append(F)
    return F

  def addEpsilonSnapshot(self, plane, position):
    if not isinstance(position,int) and not isinstance(position,float):
      print('ERROR: position argument is not int or float, but is '+str(type(position)))
      sys.exit(1)
    if isinstance(plane,int) or isinstance(plane,float):
      if plane == 1:
        plane = 'x'
      elif plane == 2:
        plane = 'y'
      elif plane == 3:
        plane = 'z'
      print('WARNING: Interpreting plane as being '+str(plane))
      
    # TODO: use x,y,z or vectors wherever possible instead of 1,2,3/0,1,2 to avoid confusion
    # TODO: support multiple types for position argument (int/float or array)
    vec, alpha = getVecAlphaDirectionFromVar(plane)
    if alpha == 'x':
      name='X epsilon snapshot'
      L = [position, self.box.lower[1], self.box.lower[2]]
      U = [position, self.box.upper[1], self.box.upper[2]]
      plane = 1
    elif alpha == 'y':
      name='Y epsilon snapshot'
      L = [self.box.lower[0], position, self.box.lower[2]]
      U = [self.box.upper[0], position, self.box.upper[2]]
      plane = 2
    elif alpha == 'z':
      name='Z epsilon snapshot'
      L = [self.box.lower[0], self.box.lower[1], position]
      U = [self.box.upper[0], self.box.upper[1], position]
      plane = 3
    else:
      print(('ERROR: Invalid plane : ',plane))
      sys.exit(1)
    F = EpsilonSnapshot(name=name, plane=plane, P1=L, P2=U)
    self.snapshot_list.append(F)
    return F

  def clearTimeSnapshots(self):
    self.snapshot_list = [ s for s in self.snapshot_list if ( not isinstance(s,Time_snapshot) or isinstance(s,EpsilonSnapshot) or isinstance(s,ModeFilteredProbe) ) ]
    self.time_snapshot_list[:] = []

  def clearFrequencySnapshots(self):
    self.snapshot_list = [ s for s in self.snapshot_list if not isinstance(s,Frequency_snapshot) ]
    self.frequency_snapshot_list[:] = []

  def clearEpsilonSnapshots(self):
    self.snapshot_list = [ s for s in self.snapshot_list if not isinstance(s,EpsilonSnapshot) ]

  def clearModeFilteredProbes(self):
    self.snapshot_list = [ s for s in self.snapshot_list if not isinstance(s,ModeFilteredProbe) ]

  def clearAllSnapshots(self):
    self.snapshot_list[:] = []
    self.time_snapshot_list[:] = []
    self.frequency_snapshot_list[:] = []

  def clearProbes(self):
    self.probe_list[:] = []

  def getEpsilonSnapshots(self):
    for i in range(len(self.snapshot_list)):
      s = self.snapshot_list[i]
    # TODO: To be continued...
      #if 
    epsilon_snapshot_list = [ s for s in self.snapshot_list if isinstance(s,EpsilonSnapshot) ]


  def clearMesh():
    self.mesh = MeshObject()

  def read_input_file(self,filename):
      ''' read GEO or INP file '''
      if self.verbosity>0: print('Processing ' + filename)
      box_read = False
      xmesh_read = False
      
      # open file
      input = open(filename)
      # read the whole file as one string
      fulltext = input.read()
      # close file
      input.close()
  
      # print fulltext
  
      # remove comments
      # TODO: Add more generic system for functional comments (to add layer, scene and group for example)
      pattern_stripcomments = re.compile("\*\*(?!name=).*\n")
      cleantext = pattern_stripcomments.sub("\n", fulltext)
      #print(cleantext)
  
      # pattern_objects = re.compile("^(?<Type>\w+).*?\{(?<data>[^\{\}]*?)\}")
      #pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<name>(?<=\*\*name=)[^{}]*)?{(?P<data>[^{}]*)}",re.DOTALL)
      pattern_objects = re.compile("(?P<Type>\w+)\s*(?P<nameblob>[^{}]+)?{(?P<data>[^{}]*)}",re.DOTALL)
      objects = [m.groupdict() for m in pattern_objects.finditer(cleantext)]
    
      entries = []
      # process objects
      for i in range(len(objects)):
          Type = objects[i]['Type']
          name = ''
          if 'nameblob' in objects[i].keys():
            #print objects[i]['nameblob']
            if objects[i]['nameblob']:
              #print 'OK'
              pattern_nameblob = re.compile("\*\*name=(.*)")
              m = pattern_nameblob.match(objects[i]['nameblob'])
              if m:
                name = m.group(1).strip()
            #else:
              #print 'NOT OK'
              #name = ''
          #else:
            #print 'NO NAME'
            #name = ''
          data = objects[i]['data']
          
          # convert Type to upper case and strip it
          Type = Type.upper().strip()
          # split data by spaces and new lines
          data = re.split('\s+',data)
          # remove empty lines from data
          #data = filter(None, data)
          data = list(filter(None, data))
          #print('data = '+str(data))
          
          entry = Entry()
          entry.Type = Type
          entry.name = name
          entry.data = data
          entries.append(entry)
          
          # mandatory objects
          if entry.Type == 'XMESH':
              self.mesh.setXmeshDelta(float_array(entry.data))
              xmesh_read = True
          elif entry.Type == 'YMESH':
              self.mesh.setYmeshDelta(float_array(entry.data))
          elif entry.Type == 'ZMESH':
              self.mesh.setZmeshDelta(float_array(entry.data))
          elif entry.Type == 'FLAG':
              self.flag.read_entry(entry)
          elif entry.Type == 'BOUNDARY':
              self.boundaries.read_entry(entry)
          elif entry.Type == 'BOX':
              self.box.read_entry(entry)
              box_read = True
                  
          # geometry objects
          elif entry.Type == 'SPHERE':
              sphere = Sphere()
              sphere.read_entry(entry)
              self.sphere_list.append(sphere)
              self.geometry_object_list.append(sphere)
          elif entry.Type == 'BLOCK':
              block = Block()
              block.read_entry(entry)
              self.block_list.append(block)
              self.geometry_object_list.append(block)
          elif entry.Type == 'DISTORTED':
              distorted = Distorted()
              distorted.read_entry(entry)
              self.distorted_list.append(distorted)
              self.geometry_object_list.append(distorted)
          elif entry.Type == 'CYLINDER':
              cylinder = Cylinder()
              cylinder.read_entry(entry)
              self.cylinder_list.append(cylinder)
              self.geometry_object_list.append(cylinder)
          elif entry.Type == 'ROTATION':
              rotation = Rotation()
              rotation.read_entry(entry)
              self.global_rotation_list.append(rotation)
              self.geometry_object_list[-1].rotation_list.append(rotation)
          
          # excitation objects
          elif entry.Type == 'EXCITATION':
              current_excitation = Excitation()
              current_excitation.read_entry(entry)
              self.excitation_list.append(current_excitation)
          
          # measurement objects
          elif entry.Type == 'FREQUENCY_SNAPSHOT':
              frequency_snapshot = Frequency_snapshot()
              frequency_snapshot.read_entry(entry)
              self.frequency_snapshot_list.append(frequency_snapshot)
              self.snapshot_list.append(frequency_snapshot)
          elif entry.Type == 'SNAPSHOT':
              time_snapshot = Time_snapshot()
              time_snapshot.read_entry(entry)
              self.time_snapshot_list.append(time_snapshot)
              self.snapshot_list.append(time_snapshot)
          elif entry.Type == 'PROBE':
              probe = Probe()
              probe.read_entry(entry)
              self.probe_list.append(probe)
  
          else:
              print('Unknown Type: ', entry.Type)

      return [ xmesh_read, box_read ]

  def read_inputs(self,filename):
      ''' read .in file '''
      if self.verbosity>0: print('->Processing .in file : ', filename)
      
      box_read = False
      xmesh_read = False
      
      f = open(filename, 'r')
      for line in f:
          if line.strip(): # only process line if it is not empty
            if self.verbosity>0: print(('os.path.dirname(filename): ', os.path.dirname(filename))) # directory of .in file
            if self.verbosity>0: print(('line.strip()=', line.strip())) # remove any \n or similar
            self.fileList.append(line.strip())
            # this is done so that you don't have to be in the directory containing the .geo/.inp files
            #subfile = os.path.join(os.path.dirname(filename),os.path.basename(line.strip())) # converts absolute paths to relative
            subfile = os.path.join(os.path.dirname(filename),line.strip()) # uses absolute paths if given
            if self.verbosity>0: print(('subfile: ', subfile))
            if (not xmesh_read): # as long as the mesh hasn't been read, .inp is assumed as the default extension
                subfile_ext = addExtension(subfile,'inp')
            else:
                subfile_ext = addExtension(subfile,'geo')
                if not os.path.isfile(subfile_ext):
                  subfile_ext = addExtension(subfile,'inp')
            [ xmesh_read_loc, box_read_loc ] = self.read_input_file(subfile_ext)
            if xmesh_read_loc:
                xmesh_read = True
            if box_read_loc:
                box_read = True
      f.close()
      if (not xmesh_read):
          print('WARNING: mesh not found')
      if (not box_read):
          print('WARNING: box not found')

  def writeMesh(self,FILE):
    ''' writes mesh to FILE '''
    # mesh X
    FILE.write('XMESH **name='+self.mesh.name+'\n')
    FILE.write('{\n')
    for i in range(len(self.mesh.getXmeshDelta())):
      FILE.write("%E\n" % self.mesh.getXmeshDelta()[i])
    FILE.write('}\n')
    FILE.write('\n')
  
    # mesh Y
    FILE.write('YMESH **name='+self.mesh.name+'\n')
    FILE.write('{\n')
    for i in range(len(self.mesh.getYmeshDelta())):
      FILE.write("%E\n" % self.mesh.getYmeshDelta()[i])
    FILE.write('}\n')
    FILE.write('\n')
  
    # mesh Z
    FILE.write('ZMESH **name='+self.mesh.name+'\n')
    FILE.write('{\n')
    for i in range(len(self.mesh.getZmeshDelta())):
      FILE.write("%E\n" % self.mesh.getZmeshDelta()[i])
    FILE.write('}\n')
    FILE.write('\n')
  
  def writeDatFiles(self,directory):
    '''Generate template .dat file for a plane excitation'''
    for obj in self.excitation_template_list:
      obj.writeDatFile(directory+os.sep+obj.fileName,self.mesh)
    return

  def writeGeoFile(self,fileName):
    ''' Generate .geo file '''
    # open file
    with open(fileName, 'w') as out:
  
      # write header
      out.write('**GEOMETRY FILE\n')
      out.write('\n')

      # write geometry objects
      #print('len(self.geometry_object_list) = '+len(self.geometry_object_list))
      for obj in self.geometry_object_list:
        #print obj.name
        #print obj.__class__.__name__
        obj.write_entry(out)

      #write box
      self.box.write_entry(out)
      
      # write footer
      out.write('end\n'); #end the file
    
      # close file
      out.close()

    return

  def writeInpFile(self,fileName):
    ''' Generate .inp file '''
    
    # make sure there is at least one excitation. Otherwise Bristol FDTD will crash.
    if len(self.excitation_list)==0:
      print('WARNING: No excitation specified. Adding default excitation.')
      self.excitation_list.append(Excitation())
    
    # open file
    with open(fileName, 'w') as out:
  
      for obj in self.excitation_list:
        #obj.directory = os.path.dirname(fileName)
        obj.mesh = self.mesh
        obj.write_entry(out)
      #print(self.boundaries)
      self.boundaries.write_entry(out)
      self.flag.write_entry(out)
      self.writeMesh(out)
      
      for obj in self.snapshot_list:
        obj.write_entry(out)
      for obj in self.probe_list:
        obj.write_entry(out)
      
      #write footer
      out.write('end\n') #end the file
      #close file
      out.close()
    return
        
  def writeFileList(self,fileName,fileList=None):
    ''' Generate .in file '''
    # leaving it external at the moment since it might be practical to use it without having to create a Bfdtd object
    #if self.fileList is None:
      #self.fileList = [fileBaseName+'.inp',fileBaseName+'.geo']
    if fileList is None:
      fileList = self.fileList
    print('fileName = '+fileName)
    #print('fileList = '+str(fileList))
    GEOin(fileName,fileList)
    return
    
  def writeCondorScript(self, fileName, BASENAME=None):
    ''' Generate fileName.cmd file for Condor using BASENAME.in, BASENAME.geo, BASENAME.inp '''
    # leaving it external at the moment since it might be practical to use it without having to create a Bfdtd object
    if BASENAME is None:
      BASENAME = os.path.splitext(os.path.basename(fileName))[0]
    GEOcommand(fileName, BASENAME)
    return
    
  def writeShellScript(self, fileName, BASENAME=None, EXE='fdtd', WORKDIR='$JOBDIR', WALLTIME=12):
    ''' Generate .sh file '''
    if BASENAME is None:
      BASENAME = os.path.splitext(os.path.basename(fileName))[0]
    GEOshellscript(fileName, BASENAME, EXE, WORKDIR, WALLTIME)
    #probe_col = 0
    #if self.excitation.E == [1,0,0]:
      #probe_col = 2
    #elif self.excitation.E == [0,1,0]:
      #probe_col = 3
    #elif self.excitation.E == [0,0,1]:
      #probe_col = 4
    #else:
      #print('ERROR : Unknown Excitation type')
      #sys.exit(-1)
    #GEOshellscript_advanced(fileName, BASENAME, probe_col, EXE, WORKDIR, WALLTIME)
    return
    
  def writeAll(self, newDirName, fileBaseName=None):
    ''' Generate .in,.inp,.geo,.cmd,.sh files in directory newDirName (it will be created if it doesn't exist)'''
    newDirName = os.path.expanduser(newDirName).rstrip('/') # replace ~ or similar and remove any trailing '/'
    
    #use_makedirs=False
    if not os.path.isdir(newDirName):
      os.makedirs(newDirName)
      #if use_makedirs:
        #os.makedirs(newDirName)
      #else:
        #os.mkdir(newDirName)

    if fileBaseName is None:
      fileBaseName = os.path.basename(os.path.abspath(newDirName))
    
    #print('fileBaseName = '+fileBaseName)
    
    geoFileName = newDirName+os.sep+fileBaseName+'.geo'
    inpFileName = newDirName+os.sep+fileBaseName+'.inp'
    inFileName = newDirName+os.sep+fileBaseName+'.in'
    cmdFileName = newDirName+os.sep+fileBaseName+'.cmd'
    shFileName = newDirName+os.sep+fileBaseName+'.sh'

    if not self.fileList:
      self.fileList = [fileBaseName+'.inp',fileBaseName+'.geo']
    
    self.writeGeoFile(geoFileName)
    self.writeInpFile(inpFileName)
    self.writeFileList(inFileName,self.fileList)
    self.writeDatFiles(newDirName)
    #self.writeCondorScript(cmdFileName)
    #self.writeShellScript(shFileName)
  
  def fitBox(self, vec6):
    ''' Changes the limits of the box to fit the geometry. Moves all other things as necessary to have box min be [0,0,0] (necessary?). 
    TODO: finish this function '''
    print('fitBox not working yet')
  
  def calculateMeshingParameters(self, minimum_mesh_delta_vector3):
    ''' returns parameters that can be used for meshing:
    -Section_MaXDeltaVector_X
    -Section_ThicknessVector_X
    -Section_MaXDeltaVector_Y
    -Section_ThicknessVector_Y
    -Section_MaXDeltaVector_Z
    -Section_ThicknessVector_Z
    '''

    simMinX = self.box.lower[0]
    simMinY = self.box.lower[1]
    simMinZ = self.box.lower[2]
    simMaXX = self.box.upper[0]
    simMaXY = self.box.upper[1]
    simMaXZ = self.box.upper[2]

    # Xvec, Yvec, Zvec are arrays of size (N,2) containing a list of (lower,upper) pairs corresponding to the meshing subdomains defined by the various geometrical objects.
    # epsX, epsY, epsZ are arrays of size (N,1) containing a list of epsilon values corresponding to the meshing subdomains defined by the various geometrical objects.
    # The (lower,upper) pairs from Xvec,Yvec,Zvec are associated with the corresponding epsilon values from epsX,epsY,epsZ to determine an appropriate mesh in the X,Y,Z directions respectively.

    # box mesh
    Xvec = numpy.array([[simMinX,simMaXX]])
    Yvec = numpy.array([[simMinY,simMaXY]])
    Zvec = numpy.array([[simMinZ,simMaXZ]])
    
    epsX = numpy.array([[1]])
    epsY = numpy.array([[1]])
    epsZ = numpy.array([[1]])

    # geometry object meshes
    for obj in self.geometry_object_list:
      if self.verboseMeshing:
        print(obj.name)
        print((Xvec,Yvec,Zvec,epsX,epsY,epsZ))
      Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)
      if self.verboseMeshing:
        print((Xvec,Yvec,Zvec,epsX,epsY,epsZ))

    # mesh object meshes
    for obj in self.mesh_object_list:
      Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

    # excitation object meshes
    if self.fitMeshToExcitations:
      for obj in self.excitation_list:
        Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

    # probe object meshes
    if self.fitMeshToProbes:
      for obj in self.probe_list:
        Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)

    # snapshot object meshes
    if self.fitMeshToSnapshots:
      for obj in self.snapshot_list:
        Xvec,Yvec,Zvec,epsX,epsY,epsZ = obj.getMeshingParameters(Xvec,Yvec,Zvec,epsX,epsY,epsZ)
      
    # postprocess the meshes
    Xvec[Xvec<simMinX] = simMinX
    Xvec[Xvec>simMaXX] = simMaXX
    Yvec[Yvec<simMinY] = simMinY
    Yvec[Yvec>simMaXY] = simMaXY
    Zvec[Zvec<simMinZ] = simMinZ
    Zvec[Zvec>simMaXZ] = simMaXZ

    ##
    VX = numpy.unique(numpy.sort(numpy.vstack([Xvec[:,0],Xvec[:,1]])))
    MX = numpy.zeros((Xvec.shape[0],len(VX)))

    for m in range(Xvec.shape[0]):
      indmin = numpy.nonzero(VX==Xvec[m,0])[0][0]
      indmaX = numpy.nonzero(VX==Xvec[m,1])[0][0]
      eps = epsX[m,0]
      vv = numpy.zeros(len(VX))
      vv[indmin:indmaX] = eps
      MX[m,:] = vv
  
    thicknessVX = numpy.diff(VX)
    epsVX = MX[:,0:MX.shape[1]-1]
    epsVX = epsVX.max(0)

    ##
    VY = numpy.unique(numpy.sort(numpy.vstack([Yvec[:,0],Yvec[:,1]])))
    MY = numpy.zeros((Yvec.shape[0],len(VY)))

    for m in range(Yvec.shape[0]):
      indmin = numpy.nonzero(VY==Yvec[m,0])[0][0]
      indmax = numpy.nonzero(VY==Yvec[m,1])[0][0]
      eps = epsY[m,0]
      vv = numpy.zeros(len(VY))
      vv[indmin:indmax] = eps
      MY[m,:] = vv
  
    thicknessVY = numpy.diff(VY)
    epsVY = MY[:,0:MY.shape[1]-1]
    epsVY = epsVY.max(0)

    ##
    VZ = numpy.unique(numpy.sort(numpy.vstack([Zvec[:,0],Zvec[:,1]])))
    MZ = numpy.zeros((Zvec.shape[0],len(VZ)))

    for m in range(Zvec.shape[0]):
      indmin = numpy.nonzero(VZ==Zvec[m,0])[0][0]
      indmax = numpy.nonzero(VZ==Zvec[m,1])[0][0]
      eps = epsZ[m,0]
      vv = numpy.zeros(len(VZ))
      vv[indmin:indmax] = eps
      MZ[m,:] = vv
  
    thicknessVZ = numpy.diff(VZ)
    epsVZ = MZ[:,0:MZ.shape[1]-1]
    epsVZ = epsVZ.max(0)
        
    meshing_parameters = MeshingParameters()
    meshing_parameters.maxPermittivityVector_X = []
    meshing_parameters.thicknessVector_X = []
    meshing_parameters.maxPermittivityVector_Y = []
    meshing_parameters.thicknessVector_Y = []
    meshing_parameters.maxPermittivityVector_Z = []
    meshing_parameters.thicknessVector_Z = []
    
    # TODO: use (thickness, epsilon) tuples so that filter() and similar functions can be used. Also prevents errors if lists have different lengths.
    # ex: t = filter(lambda x: x>=1, t)
    # filter out parts smaller than minimum_mesh_delta_vector3[i]
    for idx in range(len(thicknessVX)):
      if thicknessVX[idx] >= minimum_mesh_delta_vector3[0]:
        meshing_parameters.maxPermittivityVector_X.append(epsVX[idx])
        meshing_parameters.thicknessVector_X.append(thicknessVX[idx])
    for idx in range(len(thicknessVY)):
      if thicknessVY[idx] >= minimum_mesh_delta_vector3[1]:
        meshing_parameters.maxPermittivityVector_Y.append(epsVY[idx])
        meshing_parameters.thicknessVector_Y.append(thicknessVY[idx])
    for idx in range(len(thicknessVZ)):
      if thicknessVZ[idx] >= minimum_mesh_delta_vector3[2]:
        meshing_parameters.maxPermittivityVector_Z.append(epsVZ[idx])
        meshing_parameters.thicknessVector_Z.append(thicknessVZ[idx])
    
    return meshing_parameters
    
  def autoMeshGeometryWithMaxNumberOfCells(self, Lambda, MAXCELLS = 1e7):
    a = 10
    self.autoMeshGeometry(Lambda/a)
    print(self.getNcells()<MAXCELLS)
    while(self.getNcells()<MAXCELLS):
      print(a)
      a = a+1
      self.autoMeshGeometry(Lambda/a)
    while(self.getNcells()>MAXCELLS and a>1):
      a = a-1
      self.autoMeshGeometry(Lambda/a)
    return(a)
    
  def autoMeshGeometry(self,meshing_factor, minimum_mesh_delta_vector3 = [1e-3,1e-3,1e-3]):
    meshing_parameters = self.calculateMeshingParameters(minimum_mesh_delta_vector3)
    if self.verboseMeshing: print(meshing_parameters)
    delta_X_vector, local_delta_X_vector = subGridMultiLayer(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_X), meshing_parameters.thicknessVector_X)
    delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Y), meshing_parameters.thicknessVector_Y)
    delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(meshing_factor*1./numpy.sqrt(meshing_parameters.maxPermittivityVector_Z), meshing_parameters.thicknessVector_Z)
    self.mesh.setXmeshDelta(delta_X_vector)
    self.mesh.setYmeshDelta(delta_Y_vector)
    self.mesh.setZmeshDelta(delta_Z_vector)
  
  def rotate(self, axis_point, axis_direction, angle_degrees):
    for obj in self.geometry_object_list:
      self.rotation_list.append(Rotation(axis_point = axis_point, axis_direction = axis_direction, angle_degrees = angle_degrees))
    return
    
  def applyTransformationMatrix(self, M):
    # TODO
    return

    
class MeshBox(Geometry_object):
  def __init__(self,
    name = None,
    layer = None,
    group = None,
    lower = None,
    upper = None,
    delta_max = None):

    if name is None: name = 'mesh_box'
    if layer is None: layer = 'mesh_box'
    if group is None: group = 'mesh_box'
    if lower is None: lower = [0,0,0]
    if upper is None: upper = [1,1,1]
    if delta_max is None: permittivity3D = [1e-3,1e-3,1e-3]
    
    Geometry_object.__init__(self)
    self.name = name
    self.layer = layer
    self.group = group
    self.lower = lower
    self.upper = upper
    self.delta_max = delta_max

  def __str__(self):
    ret  = 'name = '+self.name+'\n'
    ret += 'lower = '+str(self.lower)+'\n'
    ret += 'upper = '+str(self.upper)+'\n'
    ret += 'delta_max = '+str(self.delta_max)+'\n'
    ret += Geometry_object.__str__(self)
    return ret

  def getCentro(self):
    return [ 0.5*(self.lower[0]+self.upper[0]), 0.5*(self.lower[1]+self.upper[1]), 0.5*(self.lower[2]+self.upper[2]) ]
    
  def getMeshingParameters(self,xvec,yvec,zvec,epsx,epsy,epsz):
    objx = numpy.sort([self.lower[0],self.upper[0]])
    objy = numpy.sort([self.lower[1],self.upper[1]])
    objz = numpy.sort([self.lower[2],self.upper[2]])
    xvec = numpy.vstack([xvec,objx])
    yvec = numpy.vstack([yvec,objy])
    zvec = numpy.vstack([zvec,objz])
    epsx = numpy.vstack([epsx,self.delta_max[0]])
    epsy = numpy.vstack([epsy,self.delta_max[1]])
    epsz = numpy.vstack([epsz,self.delta_max[2]])
    return xvec,yvec,zvec,epsx,epsy,epsz
    
#==== CLASSES END ====#

def readBristolFDTD(filename, verbosity = 1):
    ''' reads .in (=>.inp+.geo), .geo or .inp '''
    if verbosity>0: print('->Processing generic file : '+filename)

    structured_entries = BFDTDobject()
    structured_entries.verbosity = verbosity
    
    extension = getExtension(filename)
    if extension == 'in':
        if verbosity>0: print('.in file detected')
        structured_entries.read_inputs(filename)
    elif extension == 'inp':
        if verbosity>0: print('.inp file detected')
        structured_entries.read_input_file(filename)
    elif extension == 'geo':
        if verbosity>0: print('.geo file detected')
        structured_entries.read_input_file(filename)
    elif extension == 'prn':
        if verbosity>0: print('.prn file detected: Not supported yet')
    else:
        if verbosity>0: print('Unknown file format: '+extension)
        sys.exit(-1)
    
    #~ print '================'
    #~ print structured_entries
    #~ print '================'
    return structured_entries

def TestWriting():
    '''
    function to test the various functions, might not create working input files, but should create the correct format
    can be used as a template to create new geometries
    '''
    # initialize object
    obj = BFDTDobject()
    # mesh
    obj.mesh.setXmeshDelta([1,2,3])
    obj.mesh.setYmeshDelta([1,2,3])
    obj.mesh.setZmeshDelta([1,2,3])
    # flag
    obj.flag.iterations = 1048000
    # boundary
    obj.boundaries.Xpos_bc = 10
    obj.boundaries.Ypos_bc = 1
    obj.boundaries.Zpos_bc = 10
    obj.boundaries.Xneg_bc = 10
    obj.boundaries.Yneg_bc = 10
    obj.boundaries.Zneg_bc = 10
    obj.boundaries.Xpos_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Ypos_param = [ 1, 1, 0 ]
    obj.boundaries.Zpos_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Xneg_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Yneg_param = [ 8, 2, 1e-3 ]
    obj.boundaries.Zneg_param = [ 8, 2, 1e-3 ]
    # box
    obj.box.lower = [0,0,0]
    obj.box.upper = [10,20,30]

    # write object to example_dir/example.***
    obj.writeAll('example_dir','example')
    
    # more code, unchanged
    with open('tmp.txt', 'w') as FILE:
      delta_X_vector = [11.25,21.25,31.25]
      delta_Y_vector = [12.25,22.25,32.25]
      delta_Z_vector = [13.25,23.25,33.25]
      COMMENT = 'example comment'
      
      #GEOmesh(FILE, COMMENT, delta_X_vector, delta_Y_vector, delta_Z_vector)
      #GEOflag(FILE, COMMENT, 70, 12.34, 24, 42, 1000, 0.755025, '_id_')
      #GEOboundary(FILE, COMMENT, 1.2, [3.4,3.4,3.4],\
                                  #5.6, [7.8,7.8,6.2],\
                                  #9.10, [11.12,1,2],\
                                  #13.14, [15.16,3,4],\
                                  #17.18, [19.20,5,6],\
                                  #21.22, [23.24,7.8,5.4])
      #GEObox(FILE, COMMENT, [1.2,3.4,5.6], [9.8,7.6,5.4])
      GEOsphere(FILE, COMMENT, [1,2,3], 9, 8, 7, 6)
      GEOblock(FILE, COMMENT, [1.1,2.2,3.3], [4.4,5.5,6.6], 600, 700)
      GEOcylinder(FILE, COMMENT, [1.2,3.4,5.6], 77, 88, 99, 100, 0.02, 47.42)
      GEOrotation(FILE, COMMENT, [1,2,3], [4,5,6], 56)
      excitation_obj = Excitation(COMMENT, 77, [1,2,3], [4,5,6], [7,8,9], [77,88,99], 69, 12.36, 45.54, 78.87, 456, 1, 22, 333, 4444)
      excitation_obj.write_entry(FILE)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'x', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'y', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'z', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, True)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'x', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'y', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOtime_snapshot(FILE, COMMENT, 1, 23, 'z', [1,2,3], [4,5,6], [7,8,9], [77,88,99], [1.23,4.56,7.89], 123, False)
      GEOfrequency_snapshot(FILE, COMMENT, 369, 852, 147, 258, 369, 987, 'x', [1,2,3], [1,2,3], [852,741,963], 147, [7,8,9],[4,5,6],[1,2,3])
      GEOprobe(FILE, COMMENT, [1,2,3], 56, [5,6,7], [5,6,7], [5,6,7], 4564654 )
      GEOcommand('tmp.bat', 'BASENAME')
      GEOin('tmp.in', ['file','list'])
      GEOshellscript('tmp.sh', 'BASENAME', '/usr/bin/superexe', '/work/todo', 999)
  
def main(argv=None):
  if argv is None:
      argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error as msg:
      raise Usage(msg)
    # main function
    # for testing
    print('----->Importing bristol FDTD geometry...')
    structured_entries = readBristolFDTD(sys.argv[1])
    print(structured_entries)
    print('...done')
    
  except Usage as err:
    print(err.msg, file=sys.stderr)
    print("for help use --help", file=sys.stderr)
    return 2

if __name__ == "__main__":
  sys.exit(main())
