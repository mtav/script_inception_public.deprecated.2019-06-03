#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script to quickly get various info from bfdtd related files
# TODO: Integrate some of those functions into the BFDTD class?
# TODO: Add something to create epsilon snapshots from a geometry? based on existing mode volume frequency snapshots?

import bfdtd.bfdtd_parser as bfdtd
from utilities.common import *
from utilities.brisFDTD_ID_info import *
from constants.constants import *
import argparse
import sys
import re
import os

from bin.harminv import getFrequencies

def printNcells(infile,verbosity):
  sim = bfdtd.readBristolFDTD(infile,verbosity)
  print(sim.getNcells())
  return

def printExcitation(infile, id_list, verbosity=0):
  sim = bfdtd.readBristolFDTD(infile,verbosity)
  if id_list is None:
    id_list = range(len(sim.excitation_list))
  for i in id_list:
    print('=== excitation '+str(i)+' ===')
    print(sim.excitation_list[i])
  return

def printAll(infile,verbosity):
  sim = bfdtd.readBristolFDTD(infile,verbosity)
  print(sim)
  return

def printExcitationDirection(infile, id_list, verbosity=0):
  sim = bfdtd.readBristolFDTD(infile,verbosity)
  if id_list is None:
    id_list = range(len(sim.excitation_list))
  for i in id_list:
    print('=== excitation '+str(i)+' ===')
    print(sim.excitation_list[i].E)
  return

def printFormattedString(FORMAT):
  return

def rotate(infile, outfile, axis_point, axis_direction, angle_degrees):
  sim = bfdtd.readBristolFDTD(infile)
  sim.rotate(axis_point, axis_direction, angle_degrees)
  sim.writeGeoFile(outfile)

def automeshWithMeshingFactor(infile, outfile, meshing_factor):
  sim = bfdtd.readBristolFDTD(infile)
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(outfile)

# TODO: finish this in a nice usable way
def automeshWithMaxCells(infile, outfile, meshing_factor, MAXCELLS, Lambda, a):
  sim = bfdtd.readBristolFDTD(infile)
  sim.autoMeshGeometry(meshing_factor)
  sim.writeInpFile(outfile)

  sim = bfdtd.readBristolFDTD(infile)
  sim.autoMeshGeometry(Lambda/a)
  while(sim.getNcells()>MAXCELLS and a>1):
    a = a-1
    sim.autoMeshGeometry(Lambda/a)
  sim.writeInpFile(outfile)

def copyBFDTD(src,dst):
  ''' Copy src to dst '''
  src = src.rstrip(os.sep)
  dst = dst.rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    FDTDobj = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    FDTDobj = bfdtd.readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
  
  FDTDobj.writeAll(dst,fileBaseName)
  bfdtd.GEOshellscript(dst+os.sep+fileBaseName+'.sh', fileBaseName,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

def resonance_run(src, dst, freqListFile):
  ''' Copy src to dst with added frequency snapshots from freqListFile '''
  src = os.path.abspath(src).rstrip(os.sep)
  dst = os.path.abspath(dst).rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    FDTDobj = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    FDTDobj = bfdtd.readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
  
  freq_snapshots = getFrequencies(freqListFile)
  for obj in FDTDobj.frequency_snapshot_list:
    obj.frequency_vector = freq_snapshots
  
  FDTDobj.writeAll(dst,fileBaseName)
  FDTDobj.writeShellScript(dst+os.path.sep+fileBaseName+'.sh')

def efficiency_run(src, dst):
  ''' Copy src to dst while removing the geometry '''
  src = os.path.abspath(src).rstrip(os.sep)
  dst = os.path.abspath(dst).rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    FDTDobj = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    FDTDobj = bfdtd.readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
    
  FDTDobj.geometry_object_list[:] = []
  FDTDobj.writeAll(dst,fileBaseName)

def fixSnapshots(infile, newbasename):
  '''
  -read infile
  -remove any time snapshots
  -set frequency snapshots to first=3200, repetition=32000
  -move snapshots 1 grid away from excitation.P1
  -write to ./fixedSnapshots/newbasename
  '''
  sim = bfdtd.readBristolFDTD(infile)
  sim.fileList = []
  sim.clearTimeSnapshots()
  for s in sim.snapshot_list:
    s.first = 3200
    s.repetition = 32000

  refP = sim.excitation_list[0].P1

  (idxX,valX)=findNearest(sim.mesh.getXmesh(),refP[0])
  (idxY,valY)=findNearest(sim.mesh.getYmesh(),refP[1])
  (idxZ,valZ)=findNearest(sim.mesh.getZmesh(),refP[2])

  sim.snapshot_list[0].P1[0]=sim.snapshot_list[0].P2[0]=sim.mesh.getXmesh()[idxX-1]
  sim.snapshot_list[1].P1[1]=sim.snapshot_list[1].P2[1]=sim.mesh.getYmesh()[idxY-1]
  sim.snapshot_list[2].P1[2]=sim.snapshot_list[2].P2[2]=sim.mesh.getZmesh()[idxZ-1]

  sim.writeAll('./fixedSnapshots',newbasename)

def rerun_with_new_excitation(src, dst, excitation_wavelength_nm, excitation_time_constant):
  ''' Copy src to dst, only changing excitation_wavelength_nm and excitation_time_constant'''
  src = os.path.abspath(src).rstrip(os.sep)
  dst = os.path.abspath(dst).rstrip(os.sep)
  if os.path.isdir(src):
    print(src +' is a directory')
    FDTDobj = bfdtd.readBristolFDTD(src+os.sep+os.path.basename(src)+'.in')
    fileBaseName = os.path.basename(src)
  else:
    print(src +' is not a directory')
    FDTDobj = bfdtd.readBristolFDTD(src)
    fileBaseName = os.path.splitext(os.path.basename(src))[0]
    
  FDTDobj.excitation_list[0].time_constant = excitation_time_constant
  FDTDobj.excitation_list[0].frequency = get_c0()/(1e-3*excitation_wavelength_nm)
    
  FDTDobj.writeAll(dst,fileBaseName)
  bfdtd.GEOshellscript(dst+os.sep+fileBaseName+'.sh', fileBaseName,'$HOME/bin/fdtd', '$JOBDIR', WALLTIME = 360)

def addModeVolumeFrequencySnapshots(arguments):
  FDTDobj = bfdtd.readBristolFDTD(arguments.infile, arguments.verbosity)
  (size,res) = FDTDobj.mesh.getSizeAndResolution()
  
  if arguments.verbosity>0:
    print('res = ',res)

  if arguments.slicing_direction is None:
    # take the direction with the smallest number of snapshots to reduce number of generated .prn files
    arguments.slicing_direction = res.index(min(res))
    S = ['X','Y','Z']
    arguments.slicing_direction = S[arguments.slicing_direction]
    
  frequency_vector = []
  if arguments.freqListFile is not None:
    frequency_vector.extend(getFrequencies(arguments.freqListFile))
  if arguments.wavelength_mum is not None:
    frequency_vector.extend([get_c0()/i for i in arguments.wavelength_mum])
  if arguments.frequency_MHz is not None:
    frequency_vector.extend(arguments.frequency_MHz)
  
  if len(frequency_vector)<=0:
    print('ERROR: Great scot! You forgot to specify frequencies.', file=sys.stderr)
    sys.exit(-1)

  FDTDobj.flag.iterations = arguments.iterations
  
  NAME = 'ModeVolume'
  #print(arguments.slicing_direction)
  if arguments.slicing_direction == 'X':
    pos_list = FDTDobj.mesh.getXmesh()
    for pos in pos_list:
      e = FDTDobj.addEpsilonSnapshot('X',pos)
      e.name = NAME + '.eps'
      e.first = 1
      e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
      f = FDTDobj.addFrequencySnapshot('X',pos)
      f.name = NAME + '.freq'
      f.first = arguments.first
      f.repetition = arguments.repetition
      f.frequency_vector = frequency_vector
  elif arguments.slicing_direction == 'Y':
    pos_list = FDTDobj.mesh.getYmesh()
    for pos in pos_list:
      e = FDTDobj.addEpsilonSnapshot('Y',pos)
      e.name = NAME + '.eps'
      e.first = 1
      e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
      f = FDTDobj.addFrequencySnapshot('Y',pos)
      f.name = NAME + '.freq'
      f.first = arguments.first
      f.repetition = arguments.repetition
      f.frequency_vector = frequency_vector
  elif arguments.slicing_direction == 'Z':
    pos_list = FDTDobj.mesh.getZmesh()
    #for pos in pos_list:
    # another quick hack to reduce the number of snapshots to 101 around the center... TODO: add options for that...
    reduced_range = range(len(pos_list))
    pos_mid = int(numpy.floor(len(pos_list)/2))
    #reduced_range = pos_list[ pos_mid-50:pos_mid+50+1]
    reduced_range = pos_list[ pos_mid-25:pos_mid+25+1]
    #reduced_range = pos_list[ pos_mid-1:pos_mid+1+1]
    #reduced_range = pos_list[ pos_mid-12:pos_mid+12+1]

    # temporary hack
    #arguments.repetition = FDTDobj.flag.iterations - arguments.first
    
    full_list = []
    for pos in reduced_range:
      ##pos = pos_list[idx]
      #e = FDTDobj.addEpsilonSnapshot('Z',pos)
      #e.name = NAME + '.eps'
      #e.first = 1
      #e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
      
      ## and more quick hacks...
      #e.P1[0] = min(reduced_range)
      #e.P1[1] = min(reduced_range)
      #e.P2[0] = max(reduced_range)
      #e.P2[1] = max(reduced_range)
      
      #f = FDTDobj.addFrequencySnapshot('Z',pos)
      #f.name = NAME + '.freq'
      #f.first = arguments.first
      #f.repetition = arguments.repetition
      #f.frequency_vector = frequency_vector
      
      F = bfdtd.Frequency_snapshot()
      F.name = NAME + '.freq'
      F.plane = 'Z'
      F.P1 = [ FDTDobj.box.lower[0], FDTDobj.box.lower[1], pos]
      F.P2 = [ FDTDobj.box.upper[0], FDTDobj.box.upper[1], pos]
      F.first = arguments.first
      F.repetition = arguments.repetition
      F.frequency_vector = frequency_vector
      
      full_list.append(F)
      
      ## and more quick hacks...
      #f.P1[0] = min(reduced_range)
      #f.P1[1] = min(reduced_range)
      #f.P2[0] = max(reduced_range)
      #f.P2[1] = max(reduced_range)
      
  else:
    print('ERROR: invalid slicing direction : arguments.slicing_direction = ' + str(arguments.slicing_direction), file=sys.stderr)
    sys.exit(-1)

  list_1 = full_list[0:len(full_list)//2]
  list_2 = full_list[len(full_list)//2:len(full_list)]

  ## temporary hack to rectify excitation direction
  #P1 = numpy.array(FDTDobj.excitation_list[0].P1)
  #P2 = numpy.array(FDTDobj.excitation_list[0].P2)
  #Pdiff = P2-P1
  #Pdiff = list(Pdiff)
  #exc_dir = Pdiff.index(max(Pdiff))
  #if exc_dir == 0:
    #FDTDobj.excitation_list[0].E = [1,0,0]
  #elif exc_dir == 1:
    #FDTDobj.excitation_list[0].E = [0,1,0]
  #elif exc_dir == 2:
    #FDTDobj.excitation_list[0].E = [0,0,1]
  #else:
    #print('ERROR: wrong exc_dir = '+str(exc_dir)+' Pdiff = '+str(Pdiff), file=sys.stderr)
    #sys.exit(-1)

  # temporary hack to disable frequency snaphsots
  #FDTDobj.clearFrequencySnapshots()
  #FDTDobj.clearTimeSnapshots()

  ## Add full X,Y,Z central snapshots for reference
  #pos = FDTDobj.box.getCentro()

  #for i in [0,1,2]:
    #letter = ['X','Y','Z'][i]
    #e = FDTDobj.addEpsilonSnapshot(letter,pos[i])
    #e.name = 'central.'+letter+'.eps'
    #e.first = 1
    #e.repetition = FDTDobj.flag.iterations + 1 # So that only one epsilon snapshot is created. We don't need more.
    #f = FDTDobj.addFrequencySnapshot(letter,pos[i]);
    #f.name = 'central.'+letter+'.fsnap'
    #f.first = arguments.first
    #f.repetition = arguments.repetition
    #f.frequency_vector = frequency_vector
    
  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))
  
  # hack: remove epsilon snapshots and probes to increase speed
  FDTDobj.clearEpsilonSnapshots()
  FDTDobj.clearProbes()
  
  FDTDobj.fileList = []
  
  destdir = os.path.join(arguments.outdir,'./part_1')
  FDTDobj.snapshot_list = list_1
  FDTDobj.writeAll(destdir, arguments.basename)
  FDTDobj.writeShellScript(destdir + os.path.sep + arguments.basename + '.sh', arguments.basename, '$HOME/bin/fdtd64_2008', '$JOBDIR', WALLTIME = arguments.walltime)

  destdir = os.path.join(arguments.outdir,'./part_2')
  FDTDobj.snapshot_list = list_2
  FDTDobj.writeAll(destdir, arguments.basename)
  FDTDobj.writeShellScript(destdir + os.path.sep + arguments.basename + '.sh', arguments.basename, '$HOME/bin/fdtd64_2008', '$JOBDIR', WALLTIME = arguments.walltime)

  return

def calculateModeVolume(arguments):
  # TODO: Finish this
  # NOTE: Add way to specify snapshots, epsilon/frequency snapshot pairs
  FDTDobj = bfdtd.readBristolFDTD(arguments.infile, arguments.verbosity)

  if arguments.fsnapfiles is None:
    arguments.fsnapfiles = FDTDobj.getFrequencySnapshots()
  if arguments.esnapfiles is None:
    arguments.esnapfiles = FDTDobj.getEpsilonSnapshots()
    
  if len(arguments.fsnapfiles) != len(arguments.esnapfiles):
    print('ERROR: number of frequency snapshots and epsilon snapshots do not match', file=sys.stderr)
    sys.exit(-1)
  
  return

def addCentralXYZSnapshots(arguments):

  FDTDobj = bfdtd.readBristolFDTD(arguments.infile, arguments.verbosity)
  
  # hack: remove epsilon snapshots and probes to increase speed
  FDTDobj.clearEpsilonSnapshots()
  FDTDobj.clearProbes()
  FDTDobj.clearAllSnapshots()
  
  (size,res) = FDTDobj.mesh.getSizeAndResolution()
  
  if arguments.verbosity>0:
    print('res = ',res)
  
  frequency_vector = []
  if arguments.freqListFile is not None:
    frequency_vector.extend(getFrequencies(arguments.freqListFile))
  if arguments.wavelength_mum is not None:
    frequency_vector.extend([get_c0()/i for i in arguments.wavelength_mum])
  if arguments.frequency_MHz is not None:
    frequency_vector.extend(arguments.frequency_MHz)
  
  if len(frequency_vector)<=0:
    print('ERROR: Great scot! You forgot to specify frequencies.', file=sys.stderr)
    sys.exit(-1)

  FDTDobj.flag.iterations = arguments.iterations
  
  # hack: Make sure there will be at least one long duration snapshot at the end
  arguments.repetition = FDTDobj.flag.iterations - arguments.first
    
  # Add full X,Y,Z central snapshots
  pos = FDTDobj.box.getCentro()

  for i in [0,1,2]:
    letter = ['X','Y','Z'][i]
    f = FDTDobj.addFrequencySnapshot(letter,pos[i]);
    f.name = 'central.'+letter+'.fsnap'
    f.first = arguments.first
    f.repetition = arguments.repetition
    f.frequency_vector = frequency_vector
    
  if arguments.outdir is None:
    print('ERROR: no outdir specified', file=sys.stderr)
    sys.exit(-1)
  
  if arguments.basename is None:
    arguments.basename = os.path.basename(os.path.abspath(arguments.outdir))
  
  FDTDobj.fileList = []  
  FDTDobj.writeAll(arguments.outdir, arguments.basename)
  FDTDobj.writeShellScript(arguments.outdir + os.path.sep + arguments.basename + '.sh', arguments.basename, '$HOME/bin/fdtd64_2008', '$JOBDIR', WALLTIME = arguments.walltime)

  return
  
def clearOutputs():
  return

def main():
  
  # TODO: split options into read-only and read-write operations?
  # operations: read & print info, copy, copy with changes, write back with changes, create shellscript, create .in file, etc
  # too many operations. Needs GUI!
  
  # command-line option handling
  parser = argparse.ArgumentParser(description = 'get info about bfdtd related files')
  parser.add_argument('infile', action="store", help='input file (.geo, .inp or .in)')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')

  parser.add_argument('-o','--outfile', action="store", dest="outfile", default=None, help='output file')
  parser.add_argument('-d','--outdir', action="store", dest="outdir", default=None, help='output directory')
  parser.add_argument('-b','--basename', action="store", dest="basename", default=None, help='output basename')

  parser.add_argument('--walltime', type=int, default=360, help='walltime in hours (default: 360 hours = 15*24 hours = 15 days)')

  #group = parser.add_mutually_exclusive_group()
  #group.add_argument('--foo', action='store_true')
  #group.add_argument('--bar', action='store_false')
  
  #subparsers = parser.add_subparsers(help='functions',dest='subparser_name')
  #modevolume_parser = subparsers.add_parser('modevolume', help='Add frequency snapshots to calculate the mode volume')
  #modevolume_parser.add_argument('--slicing-direction', choices=['X','Y','Z'])

  #tmp_parser = subparsers.add_parser('lol', help='lalalala')
  #tmp_parser.add_argument('--slicing-death', choices=['Xoxo','Yoyo','Zozo'], help='lol you are LEAKING!')

  group = parser.add_argument_group('Read-only operations')
  group.add_argument('-N','--ncells', action="store_true", dest='print_Ncells', default=False, help='print the number of cells')
  group.add_argument('-E','--excitation', action="store_true", dest='print_Excitation', default=False, help='print out excitations')
  group.add_argument('-A','--all', action="store_true", dest='print_all', default=False, help='print out all information')
  group.add_argument('-D','--printExcitationDirection', action="store_true", dest='print_ExcitationDirection', default=False, help='print out excitation directions')
  group.add_argument('-f','--format', action="store_true", dest='format', default=False, help='Use FORMAT as the format string that controls the output.')
  group.add_argument('--id', action="store", metavar='ID', dest="id_list", nargs='+', type=int, help='ID(s) of the object(s) you want to print out.')
  
  group = parser.add_argument_group('Mode volume calculation')
  group.add_argument('--modevolume', help='Add frequency snapshots to calculate the mode volume', action="store_true", dest='modevolume', default=False)
  group.add_argument('--slicing-direction', choices=['X','Y','Z'], default=None, dest='slicing_direction')
  group.add_argument('--first', type=int, default=3200, help='first iteration at which to take snapshot')
  group.add_argument('--repetition', type=int, default=32000, help='step in number of iterations at which to take snapshots')
  group.add_argument('--iterations', type=int, default=67200, help='number of iterations')
  group.add_argument('--freqListFile', default=None, help='frequency list file\n\
  format:\n\
  PeakNo	Frequency(Hz)	Wavelength(nm)	QFactor\n\
  1	4.7257745e+14	634.37741293	40.4569\n\
  2	4.9540615e+14	605.14480606	90.37')

  group.add_argument('--frequency_MHz', type=float, help='frequency in MHz', action='store', metavar='f(MHz)', nargs='+')
  group.add_argument('--wavelength_mum', type=float, help='wavelength in µm', action='store', metavar='lambda(µm)', nargs='+')

  group = parser.add_argument_group('Calculate mode volume')
  group.add_argument('--calc-modevolume', help='Calculate the mode volume', action="store_true", dest='calc_modevolume', default=False)
  group.add_argument('--fsnapfiles', metavar='FSNAP', help='Frequency snapshots to use', nargs='+')
  group.add_argument('--tsnapfiles', metavar='TSNAP', help='Time snapshots to use', nargs='+')
  group.add_argument('--esnapfiles', metavar='ESNAP', help='Epsilon snapshots to use', nargs='+')
  group.add_argument('--msnapfiles', metavar='MSNAP', help='Mode filtered probes to use', nargs='+')
  group.add_argument('--probefiles', metavar='PROBE', help='Probes to use', nargs='+')
  group.add_argument('--prnfiles', metavar='PRN', help='.prn files to use', nargs='+')

  group = parser.add_argument_group('addCentralXYZSnapshots')
  group.add_argument('--addCentralXYZSnapshots', help='addCentralXYZSnapshots', action="store_true", dest='addCentralXYZSnapshots', default=False)
  

  group = parser.add_argument_group('Rotate')
  group.add_argument('-r','--rotate', action="store_true", dest='rotate', default=False, help='Rotate the geometry.')
  #axis_point
  #axis_direction
  #angle_degrees

  group = parser.add_argument_group('Meshing')
  group.add_argument('-m','--mesh', action="store_true", dest='mesh', default=False, help='Automatically mesh the geometry.')

  arguments = parser.parse_args()
  
  if arguments.verbosity>0:
    print('---------')
    print(arguments)
    print('---------')
    
  if arguments.print_all: printAll(arguments.infile,arguments.verbosity)
  if arguments.print_Ncells: printNcells(arguments.infile,arguments.verbosity)
  if arguments.print_Excitation: printExcitation(arguments.infile, arguments.id_list, arguments.verbosity)
  if arguments.print_ExcitationDirection: printExcitationDirection(arguments.infile, arguments.id_list, arguments.verbosity)

  if arguments.modevolume: addModeVolumeFrequencySnapshots(arguments)
  if arguments.calc_modevolume: calculateModeVolume(arguments)
  if arguments.addCentralXYZSnapshots: addCentralXYZSnapshots(arguments)
  
  #for infile in sys.argv[1:]:
    #print('infile = '+infile)
    #printExcitationDirection(infile, verbosity=0)
  
  #for f in arguments.infiles:
    #for line in f:
      #print(line)
    #f.close()
  
  return
  
if __name__ == "__main__":
  main()
