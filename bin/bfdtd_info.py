#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script to quickly get various info from bfdtd related files

import bfdtd.bfdtd_parser as bfdtd
import argparse
import sys

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
  
