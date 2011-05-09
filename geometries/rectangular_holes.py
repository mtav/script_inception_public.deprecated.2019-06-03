#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geometries.pillar_1D import *
from geometries.pillar_1D_wrapper import *

def main(argv=None):
  usagestr = "usage: %prog [-d destdir] [-i iterations] [ -b Nbottom ] [ -t Ntop ] [ -e excitationTypeStr ] [ -f FrequencyList ]"
  parser = OptionParser(usage=usagestr)
  
  parser.add_option("-d", "--destdir", action="store", type="string", dest="destdir", default=os.getenv('TESTDIR'), help="destination directory")
  parser.add_option("-i", type="int", dest="iterations", default=65400+524200+524200, help="number of iterations")
  parser.add_option("-b", type="int", dest="N_bottom", default=9, help="number of holes at the bottom")
  parser.add_option("-t", type="int", dest="N_top", default=7, help="number of holes at the top")
  parser.add_option("-e", type="string", dest="excitationTypeStr", default='Zm1', help="excitationType: Ym1,Ym2,Zm1,Zm2")
  parser.add_option("-f", type="string", dest="FrequencyList", default='', help="frequency of the frequency snapshots: ex: \"100.1,150.2,200.3,250.4\"")
  
  (options, args) = parser.parse_args()
  
  print 'destdir = ',options.destdir
  print 'iterations = ',options.iterations
  print 'N_bottom = ',options.N_bottom
  print 'N_top = ',options.N_top
  print 'excitationTypeStr = ',options.excitationTypeStr
  print 'FrequencyList = ',options.FrequencyList
  
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
    rectangular_holes(options.destdir,options.N_bottom,options.N_top,excitationType,options.iterations,freq_snapshots)
  else:
    print('options.destdir = ' + options.destdir + ' is not a directory')

if __name__ == "__main__":
  sys.exit(main())
