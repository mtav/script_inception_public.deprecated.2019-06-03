#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script to quickly get various info from bfdtd related files

import bfdtd.bfdtd_parser as bfdtd
from utilities.common import *
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

def main():
  
  # command-line option handling
  parser = argparse.ArgumentParser(description = 'get info about bfdtd related files')
  parser.add_argument('-N','--ncells', action="store_true", dest='print_Ncells', default=False, help='print the number of cells')
  parser.add_argument('-E','--excitation', action="store_true", dest='print_Excitation', default=False, help='print out excitations')
  parser.add_argument('-A','--all', action="store_true", dest='print_all', default=False, help='print out all information')
  parser.add_argument('-D','--printExcitationDirection', action="store_true", dest='print_ExcitationDirection', default=False, help='print out excitation directions')
  parser.add_argument('-f','--format', action="store_true", dest='format', default=False, help='Use FORMAT as the format string that controls the output.')
  parser.add_argument('-r','--rotate', action="store_true", dest='rotate', default=False, help='Rotate the geometry.')
  parser.add_argument('-m','--mesh', action="store_true", dest='mesh', default=False, help='Automatically mesh the geometry.')
  parser.add_argument('-o','--out', action="store", dest="outfile", default='.', help='output file or directory')
  parser.add_argument('-b','--basename', action="store", dest="basename", default='sim', help='output basename')
  parser.add_argument('--id', action="store", metavar='ID', dest="id_list", nargs='+', type=int, help='ID(s) of the object(s) you want to print out.')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument('infile', action="store", help='input file (.geo, .inp or .in)')

#axis_point
#axis_direction
#angle_degrees

  arguments = parser.parse_args()
  
  if arguments.verbosity>0:
    print('---------')
    print(arguments)
    print('---------')
  
  if arguments.print_all: printAll(arguments.infile,arguments.verbosity)
  if arguments.print_Ncells: printNcells(arguments.infile,arguments.verbosity)
  if arguments.print_Excitation: printExcitation(arguments.infile, arguments.id_list, arguments.verbosity)
  if arguments.print_ExcitationDirection: printExcitationDirection(arguments.infile, arguments.id_list, arguments.verbosity)
  
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
  
