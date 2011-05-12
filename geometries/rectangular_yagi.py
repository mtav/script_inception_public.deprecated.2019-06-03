#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geometries.pillar_1D import *
from optparse import OptionParser

def rectangular_yagi(DSTDIR, bottomN, topN, excitationType, iterations, freq_snapshots, CavityScalingFactor):
  P = pillar_1D()
  print('======== rectangular_yagi START ============')
  P.DSTDIR = DSTDIR
  P.setIterations(iterations)
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = freq_snapshots

  P.Nvoxels = 10;
  
  P.HOLE_TYPE = 'rectangular_yagi'
  
  n_Eff = 2.2
  n_Diamond = 2.4
  n_Air = 1
  
  # refractive indices
  P.n_Substrate = n_Diamond
  P.n_Defect = n_Diamond
  #P.n_Defect = n_Air
  P.n_Outside = n_Air
  P.n_bottomSquare = n_Diamond
  
  P.setRadiusPillarYZ(0.5,0.5)
  P.print_podium = True
  P.print_pillar = True
  
  P.d_holes_mum = P.getLambda()/(2*n_Eff);#mum
  radius_Z_piercer = 0.100
  P.setRadiusHole((P.getLambda()/(4*P.n_Defect))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum-radius_Z_piercer)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  
  P.setDistanceBetweenDefectBordersInCavity(CavityScalingFactor*P.getLambda()/n_Eff)
  
  delta_diamond = P.getLambda()/(10*P.n_Substrate);
  delta_defect = P.getLambda()/(10*P.n_Substrate);
  P.delta_X_bottomSquare = delta_diamond
  P.setDeltaHole(delta_defect,delta_defect,delta_defect)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,12*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  P.thickness_X_topBoxOffset = 1
  
  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  P.BASENAME = P.HOLE_TYPE+'.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType() #+'.DistanceBetweenDefectBordersInCavity_'+P.getDistanceBetweenDefectBordersInCavity()

  #P.verbose = True
  #dumpObj(P)
  P.write()
  
def rectangular_yagi_LambdaOver2Cavity(DSTDIR, bottomN, topN, excitationType, iterations, freq_snapshots, CavityScalingFactor):
  P = pillar_1D()
  print('======== rectangular_yagi_LambdaOver2Cavity START ============')
  P.DSTDIR = DSTDIR
  P.setIterations(iterations)
  P.print_holes_top = True
  P.print_holes_bottom = True
  P.setLambda(0.637)
  P.SNAPSHOTS_FREQUENCY = freq_snapshots

  P.Nvoxels = 10;
  
  P.HOLE_TYPE = 'rectangular_yagi'
  
  n_Eff = 2.2
  n_Diamond = 2.4
  n_Air = 1
  
  # refractive indices
  P.n_Substrate = n_Diamond
  P.n_Defect = n_Diamond
  #P.n_Defect = n_Air
  P.n_Outside = n_Air
  P.n_bottomSquare = n_Diamond
  
  P.setRadiusPillarYZ(0.5,0.5)
  P.print_podium = True
  P.print_pillar = True
  
  P.d_holes_mum = P.getLambda()/(2*n_Eff);#mum
  radius_Z_piercer = 0.100
  P.setRadiusHole((P.getLambda()/(4*P.n_Defect))/2,P.radius_Y_pillar_mum,P.radius_Z_pillar_mum-radius_Z_piercer)
  
  P.bottom_N = bottomN; #no unit
  P.top_N = topN; #no unit
  
  P.setDistanceBetweenDefectBordersInCavity(CavityScalingFactor*P.getLambda()/n_Eff)
  
  delta_diamond = P.getLambda()/(10*P.n_Substrate);
  delta_defect = P.getLambda()/(10*P.n_Substrate);
  P.delta_X_bottomSquare = delta_diamond
  P.setDeltaHole(delta_defect,delta_defect,delta_defect)
  P.setDeltaSubstrate(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaOutside(P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect),P.getLambda()/(4*P.n_Defect))
  P.setDeltaCenter(delta_diamond,delta_diamond,delta_diamond)
  P.setDeltaBuffer(delta_diamond,delta_diamond,delta_diamond)
  P.setThicknessBuffer(32*delta_diamond,4*delta_diamond,12*delta_diamond)
  P.setRadiusCenter(2*P.delta_X_center,2*P.delta_Y_center,2*P.delta_Z_center)
  
  P.thickness_X_bottomSquare = 0.5 # mum #bottom square thickness
  P.thickness_X_topBoxOffset = 1
  
  P.Xmax = P.thickness_X_bottomSquare + P.getPillarHeight() + P.thickness_X_buffer + P.thickness_X_topBoxOffset; #mum
  P.Ymax = 2*(P.radius_Y_pillar_mum + 4*delta_diamond + 4*P.delta_Y_outside); #mum
  P.Zmax = 2*(P.radius_Z_pillar_mum + 4*delta_diamond + 4*P.delta_Z_outside); #mum

  P.setExcitationType(excitationType)
  P.BASENAME = 'rectangular_yagi_LambdaOver2Cavity' + '.bottomN_'+str(bottomN)+'.topN_'+str(topN)+'.excitationType_'+P.getExcitationType() #+'.DistanceBetweenDefectBordersInCavity_'+P.getDistanceBetweenDefectBordersInCavity()

  #P.verbose = True
  #dumpObj(P)
  P.write()
  
def main(argv=None):
  usagestr = "usage: %prog [-d destdir] [-i iterations] [ -b Nbottom ] [ -t Ntop ] [ -e excitationTypeStr ] [ -f FrequencyList ]"
  parser = OptionParser(usage=usagestr)
  
  parser.add_option("-d", "--destdir", action="store", type="string", dest="destdir", default=os.getenv('TESTDIR'), help="destination directory")
  parser.add_option("-i", type="int", dest="iterations", default=65400+524200+524200, help="number of iterations")
  parser.add_option("-b", type="int", dest="N_bottom", default=9, help="number of holes at the bottom")
  parser.add_option("-t", type="int", dest="N_top", default=7, help="number of holes at the top")
  parser.add_option("-e", type="string", dest="excitationTypeStr", default='Zm1', help="excitationType: Ym1,Ym2,Zm1,Zm2")
  parser.add_option("-f", type="string", dest="FrequencyList", default='', help="frequency of the frequency snapshots: ex: \"100.1,150.2,200.3,250.4\"")
  parser.add_option("-c", type="float", dest="CavityScalingFactor", default=1, help="cavity height = CavityScalingFactor*lambda/n_Eff")
  
  (options, args) = parser.parse_args()
  
  print 'destdir = ',options.destdir
  print 'iterations = ',options.iterations
  print 'N_bottom = ',options.N_bottom
  print 'N_top = ',options.N_top
  print 'excitationTypeStr = ',options.excitationTypeStr
  print 'FrequencyList = ',options.FrequencyList
  print 'CavityScalingFactor = ',options.CavityScalingFactor
  
  if len(options.FrequencyList) == 0:
    freq_snapshots = []
  else:
    #print options.FrequencyList.split(',')
    freq_snapshots = [float(x) for x in options.FrequencyList.split(',')]
  print freq_snapshots
  #sys.exit()

  excitationType = -1
  if options.excitationTypeStr == 'Ym1':
    excitationType = 0
  elif options.excitationTypeStr == 'Zm1':
    excitationType = 1
  elif options.excitationTypeStr == 'Ym2':
    excitationType = 2
  elif options.excitationTypeStr == 'Zm2':
    excitationType = 3
  print 'excitationType = ', excitationType

  if os.path.isdir(options.destdir):
    if options.CavityScalingFactor == 1:
      rectangular_yagi(options.destdir,options.N_bottom,options.N_top,excitationType,options.iterations,freq_snapshots,1)
    else:
      rectangular_yagi_LambdaOver2Cavity(options.destdir,options.N_bottom,options.N_top,excitationType,options.iterations,freq_snapshots,0.5)
  else:
    print('options.destdir = ' + options.destdir + ' is not a directory')

if __name__ == "__main__":
  sys.exit(main())
