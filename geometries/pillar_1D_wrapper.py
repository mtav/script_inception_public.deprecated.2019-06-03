#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geometries.pillar_1D import *

def cylinder(DSTDIR, bottomN, topN, excitationType):
  P = pillar_1D()
  print('======== cylinder START ============')
  P.DSTDIR = DSTDIR
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  
  P.HOLE_TYPE = 'cylinder'
  P.setRadiusPillarYZ(0.200,0.300)# 0.150/2.0
  P.print_podium = False;
  P.thickness_X_bottomSquare = 0;
  
  P.d_holes_mum = 0.220; #mum
  P.setRadiusHole(0.28*P.d_holes_mum,P.radius_Y_pillar_mum,0.28*P.d_holes_mum)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  
  P.setDistanceBetweenDefectCentersInCavity(2*P.d_holes_mum) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = 0.5*P.getLambda()/(15*P.n_Diamond)
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(2*delta_diamond,2*delta_diamond,2*delta_diamond)
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(0,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.delta_X_bottomSquare = delta_diamond
  P.thickness_X_topBoxOffset = 0

  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 5*2*P.radius_Y_pillar_mum;
  P.Zmax = 5*2*P.radius_Z_pillar_mum;
  
  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()

  P.write()
  
def square_holes(DSTDIR, bottomN, topN, excitationType):
  P = pillar_1D()
  print('======== square_holes START ============')
  P.DSTDIR = DSTDIR
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  
  P.HOLE_TYPE = 'square_holes'
  
  P.setRadiusPillarYZ(0.200,1)
  P.print_podium = True
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  
  P.setRadiusHole((P.getLambda()/(4*P.n_Air))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum - (P.d_holes_mum-2*P.radius_X_hole))
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.setDistanceBetweenDefectCentersInCavity(P.getLambda()/P.n_Diamond + 2*P.radius_X_hole) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Diamond)
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.delta_X_bottomSquare = delta_diamond
  P.thickness_X_topBoxOffset = 1
  
  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  #dumpObj(P)
  #P.verbose = True

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()

  P.write()

def rectangular_holes(DSTDIR, bottomN, topN, excitationType):
  P = pillar_1D()
  print('======== rectangular_holes START ============')
  P.DSTDIR = DSTDIR
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  
  P.HOLE_TYPE = 'rectangular_holes'
  P.setRadiusPillarYZ(0.200,1)
  P.print_podium = True
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  
  P.setRadiusHole((P.getLambda()/(4*P.n_Air))/2, P.radius_Y_pillar_mum, P.radius_Z_pillar_mum - (P.d_holes_mum-2*P.radius_X_hole))
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.setDistanceBetweenDefectCentersInCavity(P.getLambda()/P.n_Diamond + 2*P.radius_X_hole) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Diamond)
  P.delta_X_bottomSquare = delta_diamond
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)

  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  P.thickness_X_topBoxOffset = 1

  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()

  P.write()

def rectangular_yagi(DSTDIR, bottomN, topN, excitationType):
  P = pillar_1D()
  print('======== rectangular_yagi START ============')
  P.DSTDIR = DSTDIR
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  
  P.HOLE_TYPE = 'rectangular_yagi'
  P.setRadiusPillarYZ(0.200,0.5)
  P.print_podium = True
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  P.setRadiusHole((P.getLambda()/(4*P.n_Air))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum - 0.100)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  
  P.setDistanceBetweenDefectCentersInCavity(P.getLambda()/P.n_Diamond + 2*P.radius_X_hole) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Diamond);
  P.delta_X_bottomSquare = delta_diamond
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  P.thickness_X_topBoxOffset = 1
  
  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()

  P.write()

def triangular_yagi(DSTDIR, bottomN, topN, excitationType):
  P = pillar_1D()
  print('======== triangular_yagi START ============')
  P.DSTDIR = DSTDIR
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]
  
  P.HOLE_TYPE = 'triangular_yagi'
  P.setRadiusPillarYZ(0.200,0.5)
  P.print_podium = True
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  P.setRadiusHole((P.getLambda()/(4*P.n_Air))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum - 0.100)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  
  P.setDistanceBetweenDefectCentersInCavity(P.getLambda()/P.n_Diamond + 2*P.radius_X_hole) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Diamond);
  P.setDeltaHole(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)

  P.delta_X_bottomSquare = delta_diamond
  P.thickness_X_topBoxOffset = 1

  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()

  P.write()

def triangular_yagi_voxel(DSTDIR, bottomN, topN, excitationType):
  P = pillar_1D()
  print('======== triangular_yagi_voxel START ============')
  P.DSTDIR = DSTDIR
  P.ITERATIONS = 32000
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = [get_c0()/0.637, get_c0()/0.637-1, get_c0()/0.637+1]

  P.Nvoxels = 10;
  
  P.HOLE_TYPE = 'triangular_yagi_voxel'
  P.setRadiusPillarYZ(0.200,0.5)
  P.print_podium = True
  P.print_pillar = True
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Diamond)+P.getLambda()/(4*P.n_Air);#mum
  
  P.setRadiusHole((P.getLambda()/(4*P.n_Air))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum - 3*P.radius_X_hole)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.setDistanceBetweenDefectCentersInCavity(P.getLambda()/P.n_Diamond + 2*P.radius_X_hole) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Diamond);
  #print '=====> delta = ', (2*P.radius_X_hole)/(2*P.Nvoxels+1)
  P.setDeltaHole((2*P.radius_X_hole)/(2*P.Nvoxels+1), delta_diamond, (P.radius_Z_pillar_mum - P.radius_Z_hole)/(P.Nvoxels+1))
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air),P.getLambda()/(4*P.n_Air))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,4*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.delta_X_bottomSquare = delta_diamond
  P.thickness_X_topBoxOffset = 1

  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  #dumpObj(P)
  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()

  P.write()

def test(DSTDIR,bottomN,topN):
  P = pillar_1D()
  P.DSTDIR = DSTDIR
  P.bottom_N = bottomN
  P.top_N = topN
  for i in range(4):
    P.setExcitationType(i)
    P.HOLE_TYPE = 'cylinder'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()
    P.write()
    P.HOLE_TYPE = 'square_holes'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()
    P.write()
    P.HOLE_TYPE = 'rectangular_holes'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()
    P.write()
    P.HOLE_TYPE = 'rectangular_yagi'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()
    P.write()
    P.HOLE_TYPE = 'triangular_yagi'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()
    P.write()
    P.HOLE_TYPE = 'triangular_yagi_voxel'
    P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType()
    P.write()

def test2(DSTDIR):
  P = pillar_1D()
  P.DSTDIR = DSTDIR
  print('======== default START ============')
  P.write()
  
  for i in range(4):
    cylinder(DSTDIR,12,12,i)
    cylinder(DSTDIR,20,10,i)
    square_holes(DSTDIR,6,3,i)
    square_holes(DSTDIR,20,10,i)
    rectangular_holes(DSTDIR,6,3,i)
    rectangular_holes(DSTDIR,6,4,i)
    rectangular_holes(DSTDIR,7,4,i)
    rectangular_holes(DSTDIR,7,5,i)
    rectangular_holes(DSTDIR,8,6,i)
    rectangular_yagi(DSTDIR,20,10,i)
    triangular_yagi(DSTDIR,20,10,i)
    triangular_yagi_voxel(DSTDIR,20,10,i)

def mission1(DSTDIR,excitationType):
  rectangular_holes(DSTDIR,6,3,excitationType)
  rectangular_holes(DSTDIR,6,4,excitationType)
  rectangular_holes(DSTDIR,7,4,excitationType)
  rectangular_holes(DSTDIR,7,5,excitationType)
  rectangular_holes(DSTDIR,8,6,excitationType)

def mission2(DSTDIR,excitationType):
  rectangular_yagi(DSTDIR,20,10,excitationType)

def mission3(DSTDIR,excitationType):
  cylinder(DSTDIR,12,12,excitationType)
  cylinder(DSTDIR,20,10,excitationType)

def mission4(DSTDIR,excitationType):
  triangular_yagi(DSTDIR,20,10,excitationType)
  triangular_yagi_voxel(DSTDIR,20,10,excitationType)

def main(argv=None):
  if argv is None:
      argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error, msg:
      raise Usage(msg)
    # main function
    #test(os.getenv('TESTDIR')+os.sep+'meshtest',20,10)
    #test2(os.getenv('TESTDIR'))
    excitationType = 1
    mission1(os.getenv('DATADIR')+os.sep+'mission1',excitationType)
    mission2(os.getenv('DATADIR')+os.sep+'mission2',excitationType)
    mission3(os.getenv('DATADIR')+os.sep+'mission3',excitationType)
    mission4(os.getenv('DATADIR')+os.sep+'mission4',excitationType)
    
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
