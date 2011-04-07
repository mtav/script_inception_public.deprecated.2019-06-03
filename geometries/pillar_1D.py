#!/usr/bin/env python
# -*- coding: utf-8 -*-

#~ import sys
#~ import os
#~ import getopt
#~ from utilities.getuserdir import *
from bristolFDTD_generator_functions import *
from constants import *
from meshing.subGridMultiLayer import *

class pillar_1D:
  '''creates a 1D pillar with different kinds of irregularities'''
  def __init__(self):
    self.BASENAME = 'pillar_1D'
    self.DSTDIR = getuserdir()

    self.verbose = False

    self.print_mesh = True
    self.print_holes = True
    self.print_holes_top = True
    self.print_holes_bottom = True
    self.print_pillar = True
    self.print_podium = True
    self.print_snaphots = True
    self.print_freqsnap = True
    self.print_timesnap = True
    self.print_epssnap = True
    self.print_excitation = True
    self.print_probes = True
    
    self.ITERATIONS = 32000
    self.HOLE_TYPE = 'rectangular_holes'
    self.pillar_radius_mum = 1
    self.setLambda(0.637)

    self.SNAPSHOTS_FREQUENCY = []
    self.excitation_type = 1
    self.h_bottom_square = 0.5 # mum #bottom square thickness

    #self.getLambda() = get_c0()/self.EXCITATION_FREQUENCY

    # refractive indices
    self.n_Diamond = 2.4; #no unit
    self.n_Air = 1; #no unit
    self.n_bottom_square = self.n_Diamond; #3.5214; #no unit
    # distance between holes
    #self.d_holes_mum = 0.220; #mum
    self.d_holes_mum = self.getLambda()/(4*self.n_Diamond)+self.getLambda()/(4*self.n_Air);#mum
    # hole radius
    #self.hole_radius_X = 0.28*self.d_holes_mum; #mum
    self.hole_radius_X = (self.getLambda()/(4*self.n_Air))/2;#mum
    #print self.pillar_radius_mum
    #print self.d_holes_mum
    #print self.hole_radius_X
    self.hole_radius_Z = self.pillar_radius_mum - (self.d_holes_mum-2*self.hole_radius_X); #mum

    # number of holes on bottom
    self.bottom_N = 6; #no unit
    # number of holes on top
    self.top_N = 3; #no unit
    # distance between 2 holes around cavity
    #self.d_holes_cavity = 2*self.d_holes_mum; #mum
    self.d_holes_cavity = self.getLambda()/self.n_Diamond + 2*self.hole_radius_X;#mum
    self.Lcav = self.d_holes_cavity - self.d_holes_mum; # mum
    # self.d_holes_cavity = self.Lcav + self.d_holes_mum
    # top box offset
    self.top_box_offset=1; #mum
  
    # self.ITERATIONS = 261600; #no unit
    # self.ITERATIONS = 32000; #no unit
    # self.ITERATIONS = 10; #no unit
  
    # self.ITERATIONS=1048400
    self.FIRST=65400
    self.REPETITION=524200
    self.WALLTIME=360
  
    self.TIMESTEP=0.9; #mus
    self.TIME_CONSTANT=4.000000E-09; #mus
    self.AMPLITUDE=1.000000E+01; #V/mum???
    self.TIME_OFFSET=2.700000E-08; #mus

    # max mesh intervals
    #self.delta_diamond = 0.5*self.getLambda()/(15*self.n_Diamond)
    self.delta_diamond = self.getLambda()/(10*self.n_Diamond);
    self.delta_hole = self.delta_diamond
    #self.delta_outside = 2*self.delta_diamond
    self.delta_outside = self.getLambda()/(4*self.n_Air)
    self.delta_center = self.delta_diamond
    self.delta_boundary = self.delta_diamond

    # center area where excitation takes place (for meshing)
    self.center_radius = 2*self.delta_center
  
    # buffers (area outside pillar where mesh is fine)
    self.X_buffer = 32*self.delta_diamond; #mum
    self.Y_buffer = 4*self.delta_diamond; #mum
    self.Z_buffer = 4*self.delta_diamond; #mum
  
    # dimension and position parameters
    #self.getPillarHeight() = (self.bottom_N+self.top_N)*self.d_holes_mum + self.Lcav
    
    self.Xmax = self.h_bottom_square + self.getPillarHeight() + self.X_buffer + self.top_box_offset; #mum
    #self.Ymax = 5*2*self.pillar_radius_mum;
    #self.Ymax = 2*(self.pillar_radius_mum + self.Y_buffer + 4*self.delta_outside); #mum
    self.Ymax = 2*(self.pillar_radius_mum + 4*self.delta_diamond + 4*self.delta_outside); #mum
    self.Zmax = self.Ymax; #mum

  def getPillarHeight(self):
    return (self.bottom_N+self.top_N)*self.d_holes_mum + self.Lcav

  def getLambda(self):
    return get_c0()/self.EXCITATION_FREQUENCY

  def setLambda(self,Lambda_mum):
    self.EXCITATION_FREQUENCY = get_c0()/Lambda_mum


  def getPillarCenterX(self):
    return self.h_bottom_square + self.bottom_N*self.d_holes_mum + self.Lcav/2
    
  def getPillarCenterY(self):
    return self.Ymax/2
    
  def getPillarCenterZ(self):
    return self.Zmax/2

  def write(self):
    self.mesh()
    self.writeIN();
    self.writeSH();
    self.writeCMD();
    self.writeGEO();
    self.writeINP();
  def mesh(self):
    
    if not os.path.isdir(self.DSTDIR):
      print('error: self.DSTDIR = '+self.DSTDIR+'is not a directory')
      return('error')
       
    if not os.path.isdir(self.DSTDIR+os.sep+self.BASENAME):
      os.mkdir(self.DSTDIR+os.sep+self.BASENAME)
    
    #print >>sys.stderr, 'self.hole_radius_X',self.hole_radius_X
    #print >>sys.stderr, 'self.hole_radius_Z',self.hole_radius_Z
    #print >>sys.stderr, 'self.d_holes_mum',self.d_holes_mum
    #print >>sys.stderr, 'self.pillar_radius_mum',self.pillar_radius_mum
    
    if self.hole_radius_Z<=0:
      if self.HOLE_TYPE == 'rectangular_holes':
        print >>sys.stderr, 'FATAL ERROR: negative self.hole_radius_Z = ',self.hole_radius_Z
        sys.exit(-1)
      #else:
        #print >>sys.stderr, 'WARNING: negative self.hole_radius_Z = ',self.hole_radius_Z

    if self.pillar_radius_mum<self.hole_radius_X:
      print >>sys.stderr, 'ERROR: self.pillar_radius_mum = '+str(self.pillar_radius_mum)+' < self.hole_radius_X = '+str(self.hole_radius_X)
      sys.exit(-1)      

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # additional calculations
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    # meshing parameters
    thicknessVector_X = [ ]
    max_delta_Vector_X = [ ]
    mesh_factor=1
    for i in range(self.bottom_N):
      thicknessVector_X += [ self.d_holes_mum/2 - self.hole_radius_X, 2*self.hole_radius_X, self.d_holes_mum/2 - self.hole_radius_X ]
      max_delta_Vector_X += [ mesh_factor*self.delta_diamond, mesh_factor*self.delta_hole, mesh_factor*self.delta_diamond ]
    thicknessVector_X += [ self.Lcav/2-self.center_radius, 2*self.center_radius, self.Lcav/2-self.center_radius ]
    max_delta_Vector_X += [ mesh_factor*self.delta_diamond, mesh_factor*self.delta_center, mesh_factor*self.delta_diamond ]
    for i in range(self.top_N):
      thicknessVector_X += [ self.d_holes_mum/2 - self.hole_radius_X, 2*self.hole_radius_X, self.d_holes_mum/2 - self.hole_radius_X ]
      max_delta_Vector_X += [ mesh_factor*self.delta_diamond, mesh_factor*self.delta_hole, mesh_factor*self.delta_diamond ]
  
    delta_min = min(max_delta_Vector_X)
  
    if self.HOLE_TYPE == 'cylinder':
      thicknessVector_Y_1 = [ self.Ymax/2-self.pillar_radius_mum-self.Y_buffer, self.Y_buffer, self.pillar_radius_mum-self.center_radius, self.center_radius ]
    elif self.HOLE_TYPE == 'square_holes':
      thicknessVector_Y_1 = [ self.Ymax/2-self.pillar_radius_mum-self.Y_buffer, self.Y_buffer, self.pillar_radius_mum-self.center_radius, self.center_radius ]
    elif self.HOLE_TYPE == 'rectangular_holes':
      thicknessVector_Y_1 = [ self.Ymax/2-self.pillar_radius_mum-self.Y_buffer, self.Y_buffer, self.pillar_radius_mum-self.center_radius, self.center_radius ]
    else:
      print >>sys.stderr, "ERROR: Unknown self.HOLE_TYPE "+self.HOLE_TYPE
  
    thicknessVector_Y_2 = thicknessVector_Y_1[:]; thicknessVector_Y_2.reverse()
    thicknessVector_Y = thicknessVector_Y_1 + thicknessVector_Y_2
    
    max_delta_Vector_Y_1 = [ self.delta_outside, self.delta_boundary, self.delta_hole, self.delta_center ]
    max_delta_Vector_Y_2 = max_delta_Vector_Y_1[:]; max_delta_Vector_Y_2.reverse();
    max_delta_Vector_Y = max_delta_Vector_Y_1 + max_delta_Vector_Y_2
  
    #print 'thicknessVector_Y = ', thicknessVector_Y
    #print 'max_delta_Vector_Y = ', max_delta_Vector_Y
  
    thicknessVector_Z = [ self.Zmax/2.0-self.pillar_radius_mum-self.Z_buffer,
    self.Z_buffer,
    self.pillar_radius_mum-self.hole_radius_Z,
    self.hole_radius_Z-self.center_radius,
    self.center_radius ]
    max_delta_Vector_Z = [ self.delta_outside, self.delta_boundary, self.delta_diamond, self.delta_diamond, self.delta_center ]
    
    #Mesh_ThicknessVector, Section_FinalDeltaVector = subGridMultiLayer([1,2,3,4,5],[5,4,3,2,1])
    #print('Mesh_ThicknessVector = '+str(Mesh_ThicknessVector))
    #print('Section_FinalDeltaVector = '+str(Section_FinalDeltaVector))
    
    #print('max_delta_Vector_X = '+str(max_delta_Vector_X))
    #print('thicknessVector_X = '+str(thicknessVector_X))
    #subGridMultiLayer(max_delta_Vector_X,thicknessVector_X)
    #print('============')
    
    #print max_delta_Vector_X; print thicknessVector_X
    #print max_delta_Vector_Y; print thicknessVector_Y
    #print max_delta_Vector_Z; print thicknessVector_Z
    
    delta_X_vector, local_delta_X_vector = subGridMultiLayer(max_delta_Vector_X,thicknessVector_X)
    delta_Y_vector, local_delta_Y_vector = subGridMultiLayer(max_delta_Vector_Y,thicknessVector_Y)
    delta_Z_vector, local_delta_Z_vector = subGridMultiLayer(max_delta_Vector_Z,thicknessVector_Z)
  
    # for the frequency snapshots
    
    Xplanes = [ 0,
    self.bottom_N/2*self.d_holes_mum,
    self.getPillarCenterX()-self.delta_center,
    self.getPillarCenterX(),
    self.getPillarCenterX()+self.delta_center,
    self.bottom_N*self.d_holes_mum + self.Lcav + self.top_N/2*self.d_holes_mum,
    self.getPillarHeight() ]
    
    Yplanes = [ 0,
    self.Ymax/2-self.pillar_radius_mum-self.Y_buffer,
    self.Ymax/2-self.pillar_radius_mum,
    self.Ymax/2-self.hole_radius_X,
    self.Ymax/2-2*self.delta_center,
    self.Ymax/2-self.delta_center,
    self.Ymax/2,
    self.Ymax/2+self.delta_center,
    self.Ymax/2+2*self.delta_center,
    self.Ymax/2+self.hole_radius_X,
    self.Ymax/2+self.pillar_radius_mum,
    self.Ymax/2+self.pillar_radius_mum+self.Y_buffer,
    self.Ymax ]
  
    Zplanes = [ 0,
    self.Zmax/2-self.pillar_radius_mum-self.Z_buffer,
    self.Zmax/2-self.pillar_radius_mum,
    self.Zmax/2-2*self.delta_center,
    self.Zmax/2-self.delta_center,
    self.Zmax/2 ]
    
    # for probes
    probes_X_vector = Xplanes[1:len(Xplanes)-1]
    probes_Y_vector = Yplanes[1:8]
    probes_Z_vector = Zplanes[1:4]
    
    probes_X_vector_center = Xplanes[2:5]
    probes_Y_vector_center = [Yplanes[5],Yplanes[7]]

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Files to generate:
    # .in
    # .sh
    # .cmd
    # .geo
    # .inp
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def writeIN(self):
    # .in file
    in_filename = self.DSTDIR+os.sep+self.BASENAME+os.sep+self.BASENAME+'.in'
    if self.verbose:
      print('Writing IN file '+in_filename+' ...')
    GEOin(in_filename, [ self.BASENAME+'.inp', self.BASENAME+'.geo' ])
    if self.verbose:
      print('...done')
    return(in_filename)
    
  def writeSH(self):
    # .sh file
    #TODO: improve this
    # WORKDIR = ['$HOME/loncar_structure','/',self.BASENAME]
    sh_filename = self.DSTDIR+os.sep+self.BASENAME+os.sep+self.BASENAME+'.sh';
    if self.verbose:
      print('Writing shellscript '+sh_filename+' ...')
    GEOshellscript(sh_filename, self.BASENAME, '$HOME/bin/fdtd', '$JOBDIR', self.WALLTIME)
    if self.verbose:
      print('...done')
    return(sh_filename)

  def writeCMD(self):
    # .cmd file
    cmd_filename = self.DSTDIR+os.sep+self.BASENAME+os.sep+self.BASENAME+'.cmd'
    if self.verbose:
      print('Writing CMD file '+cmd_filename+' ...')
    GEOcommand(cmd_filename, self.BASENAME)
    if self.verbose:
      print('...done')
    return(cmd_filename)
  
  def writeGEO(self):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # .geo file
    geo_filename = self.DSTDIR+os.sep+self.BASENAME+os.sep+self.BASENAME+'.geo'
    if self.verbose:
      print('Writing GEO file '+geo_filename+' ...')
  
    # open file
    with open(geo_filename, 'w') as out:
  
      # write header
      out.write('**GEOMETRY FILE\n')
      out.write('\n')
    
      # initialize current y
      X_current=0
      
      if self.print_podium:
        # create bottom block
        L = [ 0, 0, 0 ]
        U = [ X_current + self.h_bottom_square, self.Ymax, self.Zmax ]
        GEOblock(out, L, U, pow(self.n_bottom_square,2), 0)
  
      X_current = X_current + self.h_bottom_square;
      
      if self.print_pillar:
        # create main pillar
        L = [ X_current, self.Ymax/2 - self.pillar_radius_mum, self.Zmax/2 - self.pillar_radius_mum ]
        U = [ X_current + self.getPillarHeight(), self.Ymax/2 + self.pillar_radius_mum, self.Zmax/2 + self.pillar_radius_mum ]
        GEOblock(out, L, U, pow(self.n_Diamond,2), 0)
    
      X_current = X_current + self.d_holes_mum/2
    
      if self.print_holes:
          # hole settings
          permittivity = pow(self.n_Air,2)
          conductivity = 0
          
          # create bottom holes
          for i in range(self.bottom_N):
            if self.print_holes_bottom:
              centre = [ X_current, self.Ymax/2, self.Zmax/2 ]
              if self.HOLE_TYPE == 'cylinder':
                GEOcylinder(out, centre, 0, self.hole_radius_X, 2*self.pillar_radius_mum, permittivity, conductivity, 0)
              elif self.HOLE_TYPE == 'square_holes':
                lower = [ X_current - self.hole_radius_X, self.Ymax/2 - self.pillar_radius_mum, self.Zmax/2 - self.hole_radius_X]
                upper = [ X_current + self.hole_radius_X, self.Ymax/2 + self.pillar_radius_mum, self.Zmax/2 + self.hole_radius_X]
                GEOblock(out, lower, upper, permittivity, conductivity)
              elif self.HOLE_TYPE == 'rectangular_holes':
                lower = [ X_current - self.hole_radius_X, self.Ymax/2 - self.pillar_radius_mum, self.Zmax/2 - self.hole_radius_Z]
                upper = [ X_current + self.hole_radius_X, self.Ymax/2 + self.pillar_radius_mum, self.Zmax/2 + self.hole_radius_Z]
                GEOblock(out, lower, upper, permittivity, conductivity)
              else:
                print >>sys.stderr, "ERROR: Unknown self.HOLE_TYPE "+self.HOLE_TYPE
            X_current = X_current + self.d_holes_mum
    
          X_current = X_current - self.d_holes_mum + self.d_holes_cavity
    
          # create top holes
          for i in range(self.top_N):
            if self.print_holes_top:
              centre = [ X_current, self.Ymax/2, self.Zmax/2 ]
              if self.HOLE_TYPE == 'cylinder':
                GEOcylinder(out, centre, 0, self.hole_radius_X, 2*self.pillar_radius_mum, permittivity, conductivity, 0)
              elif self.HOLE_TYPE == 'square_holes':
                lower = [ X_current - self.hole_radius_X, self.Ymax/2 - self.pillar_radius_mum, self.Zmax/2 - self.hole_radius_X]
                upper = [ X_current + self.hole_radius_X, self.Ymax/2 + self.pillar_radius_mum, self.Zmax/2 + self.hole_radius_X]
                GEOblock(out, lower, upper, permittivity, conductivity)
              elif self.HOLE_TYPE == 'rectangular_holes':
                lower = [ X_current - self.hole_radius_X, self.Ymax/2 - self.pillar_radius_mum, self.Zmax/2 - self.hole_radius_Z]
                upper = [ X_current + self.hole_radius_X, self.Ymax/2 + self.pillar_radius_mum, self.Zmax/2 + self.hole_radius_Z]
                GEOblock(out, lower, upper, permittivity, conductivity)
              else:
                print >>sys.stderr, "ERROR: Unknown self.HOLE_TYPE "+self.HOLE_TYPE
            X_current = X_current + self.d_holes_mum
          
      #write box
      L = [ 0, 0, 0 ]
      U = [ self.Xmax, self.Zmax, self.Ymax/2 ]
      GEObox(out, L, U)
    
      #write footer
      out.write('end\n'); #end the file
    
      #close file
      out.close()
      if self.verbose:
        print('...done')
        
      return(geo_filename)

  def writeINP(self):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # .inp file
    inp_filename = self.DSTDIR+os.sep+self.BASENAME+os.sep+self.BASENAME+'.inp'
    if self.verbose:
      print('Writing INP file '+inp_filename+' ...')
  
    # open file
    with open(inp_filename, 'w') as out:
  
      if self.print_excitation:
        P_Xm = [ self.getPillarCenterX()-2*self.delta_center, self.getPillarCenterY(), self.getPillarCenterZ() ]
        P_Xp = [ self.getPillarCenterX()+2*self.delta_center, self.getPillarCenterY(), self.getPillarCenterZ() ]
        P_Ym1 = [ self.getPillarCenterX(), self.getPillarCenterY()-1*self.delta_center, self.getPillarCenterZ() ]
        P_Yp1 = [ self.getPillarCenterX(), self.getPillarCenterY()+1*self.delta_center, self.getPillarCenterZ() ]
        P_Ym2 = [ self.getPillarCenterX(), self.getPillarCenterY()-2*self.delta_center, self.getPillarCenterZ() ]
        P_Yp2 = [ self.getPillarCenterX(), self.getPillarCenterY()+2*self.delta_center, self.getPillarCenterZ() ]
        P_Zm1 = [ self.getPillarCenterX(), self.getPillarCenterY(), self.getPillarCenterZ()-1*self.delta_center ]
        P_Zp1 = [ self.getPillarCenterX(), self.getPillarCenterY(), self.getPillarCenterZ()+1*self.delta_center ]
        P_Zm2 = [ self.getPillarCenterX(), self.getPillarCenterY(), self.getPillarCenterZ()-2*self.delta_center ]
        P_Zp2 = [ self.getPillarCenterX(), self.getPillarCenterY(), self.getPillarCenterZ()+2*self.delta_center ]
        P_center = [ self.getPillarCenterX(), self.getPillarCenterY(), self.getPillarCenterZ() ]
        Ey = [ 0, 1, 0 ]
        Ez = [ 0, 0, 1 ]
        H = [ 0, 0, 0 ]
        type = 10
    
        if self.excitation_type == 1:
          GEOexcitation(out, 7, P_Ym1, P_center, Ey, H, type, self.TIME_CONSTANT, self.AMPLITUDE, self.TIME_OFFSET, self.EXCITATION_FREQUENCY, 0, 0, 0, 0)
        elif  self.excitation_type == 2:
          GEOexcitation(out, 7, P_Zm1, P_center, Ez, H, type, self.TIME_CONSTANT, self.AMPLITUDE, self.TIME_OFFSET, self.EXCITATION_FREQUENCY, 0, 0, 0, 0)
        elif  self.excitation_type == 3:
          GEOexcitation(out, 7, P_Ym2, P_center, Ey, H, type, self.TIME_CONSTANT, self.AMPLITUDE, self.TIME_OFFSET, self.EXCITATION_FREQUENCY, 0, 0, 0, 0)
        elif  self.excitation_type == 4:
          GEOexcitation(out, 7, P_Zm2, P_center, Ez, H, type, self.TIME_CONSTANT, self.AMPLITUDE, self.TIME_OFFSET, self.EXCITATION_FREQUENCY, 0, 0, 0, 0)
        else:
          error('invalid direction')
    
      Xpos_bc = 2; Xpos_param = [1,1,0]
      Ypos_bc = 2; Ypos_param = [1,1,0]
      Zpos_bc = 1; Zpos_param = [1,1,0]
      Xneg_bc = 2; Xneg_param = [1,1,0]
      Yneg_bc = 2; Yneg_param = [1,1,0]
      Zneg_bc = 2; Zneg_param = [1,1,0]
      GEOboundary(out, Xpos_bc, Xpos_param, Ypos_bc, Ypos_param, Zpos_bc, Zpos_param, Xneg_bc, Xneg_param, Yneg_bc, Yneg_param, Zneg_bc, Zneg_param)
      
      iteration_method = 5
      propagation_constant = 0
      flag_1 = 0
      flag_2 = 0
      id_character = 'id'
      GEOflag(out, iteration_method, propagation_constant, flag_1, flag_2, self.ITERATIONS, self.TIMESTEP, id_character)
    
      if self.print_mesh:
        GEOmesh(out, delta_X_vector, delta_Y_vector, delta_Z_vector)
          
      # frequency snapshots
      first = self.FIRST
      repetition = self.REPETITION
      interpolate = 1
      real_dft = 0
      mod_only = 0
      mod_all = 1
      starting_sample = 0
      E=[1,1,1]
      H=[1,1,1]
      J=[0,0,0]
      power = 0
      
      if self.print_snaphots == 1:
        #for iY in range(len(Yplanes)):
          #plane = 2
          #P1 = [0, Yplanes[iY], 0]
          #P2 = [self.Xmax, Yplanes[iY], self.Ymax/2]
          #GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
          #GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0)
        #for iX in range(len(Xplanes)):
          #plane = 1
          #P1 = [Xplanes[iX], 0, 0]
          #P2 = [Xplanes[iX], self.Zmax, self.Ymax/2]
          #GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
          #GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0)
        #for iZ in range(len(Zplanes)):
          #plane = 3
          #P1 = [0, 0, Zplanes[iZ]]
          #P2 = [self.Xmax, self.Zmax, Zplanes[iZ]]
          #GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
          #GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0)
    
        plane = 1
        P1 = [self.getPillarCenterX(), 0, 0]
        P2 = [self.getPillarCenterX(), self.Zmax, self.Ymax/2]
        GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
        GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0)
    
        plane = 2
        P1 = [0, self.Zmax/2, 0]
        P2 = [self.Xmax, self.Zmax/2, self.Ymax/2]
        GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
        GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0)
    
        plane = 3
        P1 = [0, 0, self.Ymax/2-2*self.delta_center]
        P2 = [self.Xmax, self.Zmax, self.Ymax/2-2*self.delta_center]
        GEOfrequency_snapshot(out, first, repetition, interpolate, real_dft, mod_only, mod_all, plane, P1, P2, self.SNAPSHOTS_FREQUENCY, starting_sample, E, H, J)
        GEOtime_snapshot(out, first, repetition, plane, P1, P2, E, H, J, power,0)
    
      if self.print_probes:
        # probes
        step=10
        E=[1,1,1]
        H=[1,1,1]
        J=[0,0,0]
        power = 0
        for iX in range(len(probes_X_vector)):
          # XZ probes
          for iZ in range(len(probes_Z_vector)):
            GEOprobe(out, [probes_X_vector[iX], Yplanes[5], probes_Z_vector[iZ]], step, E, H, J, power )
          # XY probes
          for iY in range(len(probes_Y_vector)):
            GEOprobe(out, [probes_X_vector[iX], probes_Y_vector[iY], Zplanes[4]], step, E, H, J, power )
        
        # XY center probes
        for iX in range(len(probes_X_vector_center)):
          for iY in range(len(probes_Y_vector_center)):
            GEOprobe(out, [probes_X_vector_center[iX], probes_Y_vector_center[iY], Zplanes[3]], step, E, H, J, power )
      
      #write footer
      out.write('end\n'); #end the file
    
      #close file
      out.close()
      if self.verbose:
        print('...done')
    
    return(inp_filename)

def cylinder():
  P = pillar_1D()
  print('======== cylinder START ============')
  P.DSTDIR = os.getenv('TESTDIR')
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  P.excitation_type = 1
  
  P.HOLE_TYPE = 'cylinder'
  P.BASENAME = P.HOLE_TYPE
  P.pillar_radius_mum = 0.150/2.0
  P.print_podium = False;
  P.h_bottom_square = 0;
  
  P.d_holes_mum = 0.220; #mum
  P.hole_radius_X = 0.28*P.d_holes_mum; #mum
  P.hole_radius_Z = P.hole_radius_X
  P.bottom_N = 12; #no unit
  P.top_N = 12; #no unit
  P.d_holes_cavity = 2*P.d_holes_mum; #mum
  P.Lcav = P.d_holes_cavity - P.d_holes_mum; # mum
  P.delta_diamond = 0.5*P.getLambda()/(15*P.n_Diamond)
  P.delta_hole = P.delta_diamond
  P.delta_outside = 2*P.delta_diamond
  P.delta_center = P.delta_diamond
  P.delta_boundary = P.delta_diamond
  P.X_buffer = 0; #mum
  P.Y_buffer = 4*P.delta_diamond; #mum
  P.Z_buffer = 4*P.delta_diamond; #mum
  P.top_box_offset = 0
  P.Xmax = P.h_bottom_square + P.getPillarHeight() + P.X_buffer + P.top_box_offset; #mum
  P.Ymax = 5*2*P.pillar_radius_mum;
  P.Zmax = P.Ymax; #mum
  P.center_radius = 2*P.delta_center
  
  print(P.write())
  
def square_holes():
  P = pillar_1D()
  print('======== square_holes START ============')
  P.DSTDIR = os.getenv('TESTDIR')
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  P.excitation_type = 1
  
  P.HOLE_TYPE = 'square_holes'
  P.BASENAME = P.HOLE_TYPE
  P.pillar_radius_mum = 1
  P.print_podium = True
  P.h_bottom_square = 0.5 # mum #bottom square thickness
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  P.hole_radius_X = (P.getLambda()/(4*P.n_Air))/2;#mum
  P.hole_radius_Z = P.pillar_radius_mum - (P.d_holes_mum-2*P.hole_radius_X); #mum
  P.bottom_N = 6; #no unit
  P.top_N = 3; #no unit
  P.d_holes_cavity = P.getLambda()/P.n_Diamond + 2*P.hole_radius_X;#mum
  P.Lcav = P.d_holes_cavity - P.d_holes_mum; # mum
  P.delta_diamond = P.getLambda()/(10*P.n_Diamond);
  P.delta_hole = P.delta_diamond
  P.delta_outside = P.getLambda()/(4*P.n_Air)
  P.delta_center = P.delta_diamond
  P.delta_boundary = P.delta_diamond
  P.X_buffer = 32*P.delta_diamond; #mum
  P.Y_buffer = 4*P.delta_diamond; #mum
  P.Z_buffer = 4*P.delta_diamond; #mum
  P.top_box_offset = 1
  P.Xmax = P.h_bottom_square + P.getPillarHeight() + P.X_buffer + P.top_box_offset; #mum
  P.Ymax = 2*(P.pillar_radius_mum + 4*P.delta_diamond + 4*P.delta_outside); #mum
  P.Zmax = P.Ymax; #mum
  P.center_radius = 2*P.delta_center

  print(P.write())

def rectangular_holes(bottomN,topN):
  P = pillar_1D()
  print('======== rectangular_holes START ============')
  P.DSTDIR = os.getenv('TESTDIR')
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  P.excitation_type = 1
  
  P.HOLE_TYPE = 'rectangular_holes'
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)
  P.pillar_radius_mum = 1
  P.print_podium = True
  P.h_bottom_square = 0.5 # mum #bottom square thickness
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  P.hole_radius_X = (P.getLambda()/(4*P.n_Air))/2;#mum
  P.hole_radius_Z = P.pillar_radius_mum - (P.d_holes_mum-2*P.hole_radius_X); #mum
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.d_holes_cavity = P.getLambda()/P.n_Diamond + 2*P.hole_radius_X;#mum
  P.Lcav = P.d_holes_cavity - P.d_holes_mum; # mum
  P.delta_diamond = P.getLambda()/(10*P.n_Diamond);
  P.delta_hole = P.delta_diamond
  P.delta_outside = P.getLambda()/(4*P.n_Air)
  P.delta_center = P.delta_diamond
  P.delta_boundary = P.delta_diamond
  P.X_buffer = 32*P.delta_diamond; #mum
  P.Y_buffer = 4*P.delta_diamond; #mum
  P.Z_buffer = 4*P.delta_diamond; #mum
  P.top_box_offset = 1
  P.Xmax = P.h_bottom_square + P.getPillarHeight() + P.X_buffer + P.top_box_offset; #mum
  P.Ymax = 2*(P.pillar_radius_mum + 4*P.delta_diamond + 4*P.delta_outside); #mum
  P.Zmax = P.Ymax; #mum
  P.center_radius = 2*P.delta_center

  print(P.write())

def rectangular_yagi(bottomN,topN):
  P = pillar_1D()
  print('======== rectangular_yagi START ============')
  P.DSTDIR = os.getenv('TESTDIR')
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  P.excitation_type = 1
  
  P.HOLE_TYPE = 'rectangular_holes'
  P.BASENAME = 'rectangular_yagi'+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)
  P.pillar_radius_mum = 1
  P.print_podium = True
  P.h_bottom_square = 0.5 # mum #bottom square thickness
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  P.hole_radius_X = (P.getLambda()/(4*P.n_Air))/2;#mum
  P.hole_radius_Z = P.pillar_radius_mum + (P.d_holes_mum-2*P.hole_radius_X); #mum
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.d_holes_cavity = P.getLambda()/P.n_Diamond + 2*P.hole_radius_X;#mum
  P.Lcav = P.d_holes_cavity - P.d_holes_mum; # mum
  P.delta_diamond = P.getLambda()/(10*P.n_Diamond);
  P.delta_hole = P.delta_diamond
  P.delta_outside = P.getLambda()/(4*P.n_Air)
  P.delta_center = P.delta_diamond
  P.delta_boundary = P.delta_diamond
  P.X_buffer = 32*P.delta_diamond; #mum
  P.Y_buffer = 4*P.delta_diamond; #mum
  P.Z_buffer = 4*P.delta_diamond; #mum
  P.top_box_offset = 1
  P.Xmax = P.h_bottom_square + P.getPillarHeight() + P.X_buffer + P.top_box_offset; #mum
  P.Ymax = 2*(P.pillar_radius_mum + 4*P.delta_diamond + 4*P.delta_outside); #mum
  P.Zmax = P.Ymax; #mum
  P.center_radius = 2*P.delta_center

  print(P.write())

def main(argv=None):
  if argv is None:
      argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
      raise Usage(msg)
    # main function
    #in_filename = pillar_1D('test', os.getenv('TESTDIR'), 32000, 1, 1, 'cylinder', 0.150/2.0, get_c0()/0.637, [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1],1)
    #in_filename = pillar_1D('test', os.getenv('TESTDIR'), 32000, 1, 1, 'square_holes', 0.150/2.0, get_c0()/0.637, [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1],1)
    #in_filename = pillar_1D('test', os.getenv('TESTDIR'), 32000, 1, 1, 'rectangular_holes', 0.150/2.0, get_c0()/0.637, [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1],1)
    #in_filename = pillar_1D('test', os.getenv('TESTDIR'), 32000, True, True, 'rectangular_holes', 1, get_c0()/0.637, [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1],1)

    P = pillar_1D()
    print('======== default START ============')
    print(P.write())
    cylinder()
    square_holes()
    rectangular_holes(6,3)
    rectangular_holes(6,4)
    rectangular_holes(7,4)
    rectangular_holes(7,5)
    rectangular_holes(8,6)
    rectangular_yagi(20,10)
    
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
