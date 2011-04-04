#!/usr/bin/env python

import sys
import getopt

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    print "main called"
    if argv is None:
  print "none"
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    print "calling main"
    sys.exit(main())
