#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import fnmatch
import os
import string
import argparse
from utilities.brisFDTD_ID_info import alphaID_to_numID

# TODO: Add option to fix only NTFS/FAT32 incompatible filenames or create/look for script to make filenames NTFS/FAT32 compatible
# ex: recode, convmv, detox
# cf: http://ubuntuforums.org/showthread.php?t=1479470
# cf: http://techtots.blogspot.co.uk/2010/01/removing-invalidencoded-characters-from.html
# convmv -r --notest -f windows-1255 -t UTF-8 *

# Note: On bluecrystal, you can use (old rename binary):
#find . -name "*.prn" -exec rename ":" "10" {} \;
#find . -name "p??id.prn" -exec rename "p" "p0" {} \;
#rename : 10 *.prn
#rename p p0 p??id.prn

def main():
  # command-line option handling  
  parser = argparse.ArgumentParser(description = 'rename .prn files produced by BFDTD to NTFS compatible names (as well as human readable)')
  
  parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose: print names of files successfully renamed.")
  parser.add_argument("-n", "--no-act", action="store_true", dest="no_act", default=False, help="No Action: show what files would have been renamed.")
  parser.add_argument("-f", "--force", action="store_true", dest="force", default=False, help="Force: overwrite existing files.")
  parser.add_argument("-d", "--directory", action="append", dest="directory", help="rename all .prn files in this directory recursively. Multiple directories can be specified with -d DIR1 -d DIR2")
  parser.add_argument('files', action="store", nargs='*', help='input files (.prn)')
  parser.add_argument("--id", action="store", dest="probe_ident", default=None, help="specify a probe identifier")
  parser.add_argument("--type", action="store", dest="expected_object_type", choices=['fsnap','tsnap','mfprobe','probe'], default=None, help="specify the type of .prn file")

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
    numID, snap_plane, probe_ident, snap_time_number, fixed_filename, object_type = alphaID_to_numID(src[i], arguments.expected_object_type, arguments.probe_ident)
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
