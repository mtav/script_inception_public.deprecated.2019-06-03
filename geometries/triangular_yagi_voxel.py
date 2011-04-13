from geometries.pillar_1D import *

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
  
  P.d_holes_mum = P.getLambda()/(4*P.n_Substrate)+P.getLambda()/(4*P.n_Defect);#mum
  
  P.setRadiusHole((P.getLambda()/(4*P.n_Defect))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum - 3*P.radius_X_hole)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  P.setDistanceBetweenDefectCentersInCavity(P.getLambda()/P.n_Substrate + 2*P.radius_X_hole) #mum
  # P.setDistanceBetweenDefectPairsInCavity(P.getDistanceBetweenDefectCentersInCavity() - P.d_holes_mum) # mum
  delta_diamond = P.getLambda()/(10*P.n_Substrate);
  #print '=====> delta = ', (2*P.radius_X_hole)/(2*P.Nvoxels+1)
  P.setDeltaHole((2*P.radius_X_hole)/(2*P.Nvoxels+1), delta_diamond, (P.radius_Z_pillar_mum - P.radius_Z_hole)/(P.Nvoxels+1))
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,12*delta_diamond)
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
