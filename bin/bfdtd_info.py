#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# script to quickly get various info from bfdtd related files

import bfdtd.bfdtd_parser as bfdtd
import argparse
import sys

def printNcells(infile):
  sim = bfdtd.readBristolFDTD(infile)
  print(sim.getNcells())
  return

def printExcitation(infile):
  sim = bfdtd.readBristolFDTD(infile)
  for i in range(len(sim.excitation_list)):
    print('=== excitation '+str(i)+' ===')
    print(sim.excitation_list[i])
  return

def printAll(infile):
  sim = bfdtd.readBristolFDTD(infile)
  print(sim)
  return

def printExcitationDirection(infile,verbosity):
  sim = bfdtd.readBristolFDTD(infile,verbosity)
  for i in range(len(sim.excitation_list)):
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
  
  ## command-line option handling
  #parser = argparse.ArgumentParser(description = 'get info about bfdtd related files')
  #parser.add_argument('-N','--ncells')
  #arguments = parser.parse_args()
  
  #print('---------')
  #print(arguments)
  
  for infile in sys.argv[1:]:
    print('infile = '+infile)
    printExcitationDirection(infile, verbosity=0)
  
if __name__ == "__main__":
  main()
  
