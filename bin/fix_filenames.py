#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import fnmatch
import os
import string
import argparse
from utilities.brisFDTD_ID_info import numID_to_alphaID, alphaID_to_numID

# TODO: add support for the full range of char IDs (;,<, etc)
def main():
  # command-line option handling  
  parser = argparse.ArgumentParser(description = 'rename .prn files produced by BFDTD to NTFS compatible names (as well as human readable)')
  
  parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose: print names of files successfully renamed.")
  parser.add_argument("-n", "--no-act", action="store_true", dest="no_act", default=False, help="No Action: show what files would have been renamed.")
  parser.add_argument("-f", "--force", action="store_true", dest="force", default=False, help="Force: overwrite existing files.")
  parser.add_argument("-d", "--directory", action="append", dest="directory", help="rename all .prn files in this directory recursively. Multiple directories can be specified with -d DIR1 -d DIR2")
  parser.add_argument('files', action="store", nargs='*', help='input files (.prn)')

  arguments = parser.parse_args()
  
  print('---------')
  print(arguments)
  print('---------')

  src = arguments.files

  # add .prn files in specified directories recursively
  if arguments.directory:
    for directory in arguments.directory:
      matches = []
      for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.prn'):
          matches.append(os.path.join(root, filename))
      
      src.extend(matches)
  
  dst = len(src)*[0]
  
  for i in range(len(src)):
    numID, snap_plane, probe_ident, snap_time_number, fixed_filename = alphaID_to_numID(src[i])
    dst[i] = fixed_filename
    if dst[i]:
      if arguments.verbose:
        print(src[i]+' -> '+dst[i])
      if os.path.isfile(src[i]):
        if (not os.path.isfile(dst[i])) or arguments.force:
          if (not arguments.no_act):
            os.rename(src[i], dst[i])
        else:
          print('WARNING: Skipping '+src[i]+' -> '+dst[i]+' : destination file exists', file=sys.stderr)
      else:
        print('WARNING: Skipping '+src[i]+' -> '+dst[i]+' : source file does not exist', file=sys.stderr)
    else:
      print('WARNING: ' + src[i] + ' could not be converted', file=sys.stderr)

  # left in for reference
  #for filename in fnmatch.filter(filenames, '*:*.prn'):
    #dst.append(os.path.join(root, string.replace(filename,':','10')))
  #for filename in fnmatch.filter(filenames, 'p??id.prn'):
    #dst.append(os.path.join(root, string.replace(filename,'p','p0',1)))

if __name__ == "__main__":
    sys.exit(main())
