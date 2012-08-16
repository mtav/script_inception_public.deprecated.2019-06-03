#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import numpy
import math
import re
import datetime

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

def getProbeColumnFromExcitation(excitation):
  print(('excitation = ',excitation))
  probe_col = 0
  if excitation == [1,0,0]:
    probe_col = 2
  elif excitation == [0,1,0]:
    probe_col = 3
  elif excitation == [0,0,1]:
    probe_col = 4
  else:
    print('ERROR in getProbeColumnFromExcitation: Unknown Excitation type')
    sys.exit(-1)
  print(('probe_col', probe_col))
  return probe_col

def symmetrifyEven(vec):
  ''' [1, 2, 3]->[1, 2, 3, 3, 2, 1] '''
  sym = vec[:]; sym.reverse()
  return vec + sym

def symmetrifyOdd(vec):
  ''' [1, 2, 3]->[1, 2, 3, 2, 1] '''
  sym = vec[:]; sym.reverse()
  return vec + sym[1:]

def symmetrifyAndSubtractOdd(vec,max):
  ''' [1, 2, 3]->[1, 2, 3, 8, 9] for max = 10
      [0, 1, 2, 3]->[0, 1, 2, 3, 4, 5, 6] for max = 6 '''
  sym = vec[:]; sym.reverse()
  sym_cut = [max-x for x in sym[1:]]
  return vec + sym_cut

def float_array(A):
    ''' convert string array to float array '''
    for i in range(len(A)):
        A[i]=float(A[i])
    return(A)
  
def int_array(A):
    ''' convert string array to int array '''
    for i in range(len(A)):
        A[i]=int(float(A[i]))
    return(A)


def is_number(s):
    ''' returns true if s can be converted to a float, otherwise false '''
    try:
        float(s)
        return True
    except ValueError:
        return False

def addExtension(filename, default_extension):
    ''' add default_extension if the file does not end in .geo or .inp '''
    
    extension = getExtension(filename)
    if extension == 'geo' or extension == 'inp':
        return filename
    else:
        return filename + '.' + default_extension

def getExtension(filename):
    ''' returns extension of filename '''
    return filename.split(".")[-1]

''' Returns ([1,0,0],'x'),etc corresponding to var(alpha or vector) '''
def getVecAlphaDirectionFromVar(var):
  S = ['x','y','z']
  V = [[1,0,0],[0,1,0],[0,0,1]]
  if var in V:
    return var, S[var.index(1)]
  elif var.lower() in S:
    return V[S.index(var.lower())],var.lower()
  else:
    print('unknown direction: '+str(var))
    sys.exit(-1)
  
''' Returns numindex(1,2,3) and char('X','Y','Z') corresponding  to var(num or alpha index) '''
def planeNumberName(var):
  S=['X','Y','Z']
  if var in [1,2,3]:
    return var, S[var-1]
  elif var.upper() in S:
    return S.index(var.upper())+1,var.upper()
  else:
    print('unknown plane: '+str(var))
    sys.exit(-1)

# based on functions from http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def findNearest(a, a0):
    ''' Element in nd array `a` closest to the scalar value `a0` 
    returns (idx, a.flat[idx]) = (index of closest value, closest value)'''
    idx = numpy.abs(a - a0).argmin()
    return (idx, a.flat[idx])

def addDoubleQuotesIfMissing(orig):
  
  # simple solution
  orig_quoted = '"'+str(orig).strip('"').strip('\'')+'"'

  ## Complex solution as seen on: http://stackoverflow.com/questions/3584005/how-to-properly-add-quotes-to-a-string-using-python
  #Q = '"'
  #re_quoted_items = re.compile(r'" \s* [^"\s] [^"]* \"', re.VERBOSE)

  ## The orig string w/o the internally quoted items.
  #woqi = re_quoted_items.sub('', orig)

  #if len(orig) == 0:
    #orig_quoted = Q + orig + Q
  #elif len(woqi) > 0 and not (woqi[0] == Q and woqi[-1] == Q):
    #orig_quoted = Q + orig + Q    
  #else:
    #orig_quoted = orig

  return orig_quoted

# FIB distance estimation functions. Might be used in FIB picture postprocessing program eventually. Or in Gimp through a plugin...
# TODO: At the moment those formulas are only for distances in the Y (vertical) direction of the picture. Need to add support for any sort of line on the picture.
# Functions could be tested against FIB measurement tool. Method: Project (X,Y) points along Z axis onto arbitrary plane and corresponding normal.

def FIBdistanceHorizontal(tilt_deg, magnification, distance_on_picture_pxl, angle_to_horizontal_deg = 90, horizontal_width_of_picture_pxl = 1024, HFW_mum = 304000):
  '''
  Returns the horizontal distance in mum based on the visible distance in pixels on the picture.
  Warning: formula for angled segments hasn't been fully verified yet.
  '''
  W_mum = HFW_mum/float(magnification); # Width of the horizontal scan (mum). (HFW = Horizontal Field Width)
  resolution = W_mum/horizontal_width_of_picture_pxl; # size of each pixel (mum/pxl).
  lx_visible_pxl = distance_on_picture_pxl*numpy.cos(numpy.deg2rad(angle_to_horizontal_deg))
  ly_visible_pxl = distance_on_picture_pxl*numpy.sin(numpy.deg2rad(angle_to_horizontal_deg))
  Lx_sample_pxl = lx_visible_pxl
  Ly_sample_pxl = ly_visible_pxl/numpy.cos(numpy.deg2rad(tilt_deg))
  L_sample_pxl = numpy.sqrt(pow(Lx_sample_pxl,2)+pow(Ly_sample_pxl,2))
  L_sample_mum = L_sample_pxl*resolution
  return L_sample_mum

def FIBdistanceVertical(tilt_deg, magnification, distance_on_picture_pxl, horizontal_width_of_picture_pxl = 1024, HFW_mum = 304000):
  '''
  Returns the vertical distance in mum based on the visible distance in pixels on the picture. 
  Warning: Always assumes a vertical pixel distance measurement (because it's the only thing making sense assuming an orthographic projection)
  '''
  W_mum = HFW_mum/float(magnification); # Width of the horizontal scan (mum). (HFW = Horizontal Field Width)
  resolution = W_mum/horizontal_width_of_picture_pxl; # size of each pixel (mum/pxl).
  L_sample_mum = (distance_on_picture_pxl*resolution)/numpy.sin(numpy.deg2rad(tilt_deg))
  return L_sample_mum

# time utility functions from http://stackoverflow.com/questions/7065761/how-to-substract-two-datetime-time-values-in-django-template-and-how-to-format-a
def difft(start,end):
    ''' returns the difference in seconds between two datetime.time objects '''
    a,b,c,d = start.hour, start.minute, start.second, start.microsecond
    w,x,y,z = end.hour, end.minute, end.second, end.microsecond
    delt = (w-a)*60*60 + (x-b)*60 + (y-c) + (z-d)/pow(10,6)
    return delt + 24*60*60 if delt<0 else delt

def difft_string(start,end):
    ''' prints the difference between two datetime.time objects in a nice format '''
    delt = difft(start,end)

    hh,rem = divmod(delt,60*60)
    hh = int(hh)
    mm,rem = divmod(rem,60)
    mm = int(mm)
    ss = int(rem)
    ms = (rem - ss)*pow(10,6)
    ms = int(ms)

    SS = '%sh %smn %ss %sms'
    return SS % (hh,mm,ss,ms)
    
def todatetime(time):
    ''' converts a datetime.time object to a datetime.datetime object using the current date '''
    return datetime.datetime.today().replace(hour=time.hour, minute=time.minute, second=time.second, 
                                             microsecond=time.microsecond, tzinfo=time.tzinfo)

def timestodelta(starttime, endtime):
    ''' returns the difference in seconds between two datetime.time objects '''
    return todatetime(endtime) - todatetime(starttime)

# TODO: Start splitting up all those utilities into different files?
def rotation_matrix3(axis,theta):
  '''
  Returns a rotation matrix of size 4 to rotate something around vector v by angle theta
  Usage:
    v = np.array([3,5,0])
    axis = np.array([4,4,1])
    theta = 1.2 
    print(np.dot(rotation_matrix(axis,theta),v))
  source: http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector
  TODO: Replace with some existing complete geometry module???
  '''
  axis = axis/np.sqrt(np.dot(axis,axis))
  a = np.cos(theta/2)
  b,c,d = -axis*np.sin(theta/2)
  return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                   [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                   [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

def rotation_matrix4(axis,theta):
  '''
  Returns a rotation matrix of size 4 to rotate something around vector v by angle theta
  Usage:
    v = np.array([3,5,0])
    axis = np.array([4,4,1])
    theta = 1.2 
    print(np.dot(rotation_matrix(axis,theta),v))
  source: http://stackoverflow.com/questions/6802577/python-rotation-of-3d-vector
  TODO: Replace with some existing complete geometry module???
  '''
  axis = axis/np.sqrt(np.dot(axis,axis))
  a = np.cos(theta/2)
  b,c,d = -axis*np.sin(theta/2)
  return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c), 0],
                   [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b), 0],
                   [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c, 0],
                   [0,0,0,1]])

def Angle(p, q):
   ''' return the angle w.r.t. another 3-vector '''
   ptot2 = numpy.dot(p,p)*numpy.dot(q,q)
   if ptot2 <= 0:
      return 0.0
   else:
      arg = numpy.dot(p,q)/numpy.sqrt(ptot2)
      if arg >  1.0: arg =  1.0
      if arg < -1.0: arg = -1.0
      return numpy.arccos(arg)

def Orthogonal(u):
  '''
  get vector v orthogonal to u
  ex: v = Orthogonal(u)
  '''
  if u[0] < 0.0:
    xx = -u[0]
  else:
    xx = u[0]
  if u[1] < 0.0:
    yy = -u[1]
  else:
    yy = u[1]
  if u[2] < 0.0:
    zz = -u[2]
  else:
    zz = u[2]
  if (xx < yy):
    if xx < zz:
      return numpy.array([0,u[2],-u[1]])
    else:
      return numpy.array([u[1],-u[0],0])
  else:
    if yy < zz:
      return numpy.array([-u[2],0,u[0]])
    else:
      return numpy.array([u[1],-u[0],0])
