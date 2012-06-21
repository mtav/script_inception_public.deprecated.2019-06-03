#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import fnmatch
import os
import string
from optparse import OptionParser

# TODO: add support for the full range of char IDs (;,<, etc)
def main(argv=None):
  usagestr = "usage: %prog [ -v ] [ -n ] [ -f ] [ directory ]"
        #[-v, --verbose]
       #[-n, --no-act]
       #[-f, --force]
       
  parser = OptionParser(usage=usagestr)
  
  parser.add_option("-v", "--verbose", action="store_true", dest="verbose",default=False, help="Verbose: print names of files successfully renamed.")
  parser.add_option("-n", "--no-act", action="store_true", dest="no_act",default=False, help="No Action: show what files would have been renamed.")
  parser.add_option("-f", "--force", action="store_true", dest="force",default=False, help="Force: overwrite existing files.")
  #parser.add_option("-q", action="store_false", dest="verbose")
  #parser.add_option("-q", action="store_false", dest="verbose")

  
  #parser.add_option("-d", "--destdir", action="store", type="string", dest="destdir", default=os.getenv('DATADIR'), help="destination directory")
  #parser.add_option("-i", type="int", dest="iterations", default=65400+524200+524200, help="number of iterations")
  
  (options, args) = parser.parse_args()
  if len(args) != 1:
    parser.error("incorrect number of arguments")
      
  #print options.verbose
  #print options.no_act
  #print options.force

  #print args
  
  # main code
  
  #find . -name "*.prn" 
  #-exec rename ":" "10" {} \;
  matches = []
  dst = []
  for root, dirnames, filenames in os.walk(args[0]):
    for filename in fnmatch.filter(filenames, '*:*.prn'):
      matches.append(os.path.join(root, filename))
      dst.append(os.path.join(root, string.replace(filename,':','10')))
  for i in range(len(matches)):
    if (not options.no_act):
      os.rename(matches[i], dst[i])
    if options.verbose:
      print matches[i]+' -> '+dst[i]
    #print matches[i]+' -> '+dst[i]

  #find . -name "p??id.prn" 
  #-exec rename "p" "p0" {} \;
  matches = []
  dst = []
  for root, dirnames, filenames in os.walk(args[0]):
    for filename in fnmatch.filter(filenames, 'p??id.prn'):
      matches.append(os.path.join(root, filename))
      dst.append(os.path.join(root, string.replace(filename,'p','p0',1)))
  for i in range(len(matches)):
    if (not options.no_act):
      os.rename(matches[i], dst[i])
    if options.verbose:
      print matches[i]+' -> '+dst[i]
    #print matches[i]+' -> '+dst[i]

if __name__ == "__main__":
    sys.exit(main())
