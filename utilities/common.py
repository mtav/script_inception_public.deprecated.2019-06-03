#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import numpy
import math

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def fixLowerUpper(L,U):
  real_L = [0,0,0]
  real_U = [0,0,0]
  for i in range(3):
    real_L[i] = min(L[i],U[i])
    real_U[i] = max(L[i],U[i])
  return real_L, real_U

def LimitsToThickness(limits):
  return [ limits[i+1]-limits[i] for i in range(len(limits)-1) ]

#def getUnitaryDirection()
#E = subtract(excitation.P2,excitation.P1)
#E = list(E/linalg.norm(E))

def Unit(vec):
  ''' return unit vector parallel to vec. '''
  tot = numpy.linalg.norm(vec)
  if tot > 0.0:
    return vec/tot
  else:
    return vec

  #tot = Mag2(vec)
  #if tot > 0.0:
    #return vec*(1.0/math.sqrt(tot))
  #else:
    #return vec

def Mag2(vec):
  return vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2]

def Mag(vec):
  ''' return the magnitude (rho in spherical coordinate system) '''
  return math.sqrt(Mag2(vec))
