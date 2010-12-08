#!BPY

"""
Name: 'MEEP (*.ctl)'
Blender: 249
Group: 'Import'
Tooltip: 'Import from MEEP'
"""

print 'Importing MEEP file'

import pyscheme.parser
import pyscheme.parser
import pyscheme.scheme
import pyscheme.expressions
import sys
from glob import glob

def parseFile(filename):
	print "Processing "+filename;
	FILE = open(filename,'r');
	str = FILE.read();
	FILE.close();
	program = pyscheme.parser.parse('('+str+')')
	print program

if len(sys.argv)>4:
    # for i in range(len(sys.argv)- 4):
        # print 'Importing ', sys.argv[4+i];
        # importMEEP(sys.argv[4+i]);
    for arg in sys.argv[4:]:
        filelist = glob(arg);
        for file in filelist:
            parseFile(file);
        # filelist = glob('*.ctl');
        # print "============"
        # print filelist
        # print "============"
        # parseFile(arg);
else:
    print 'No arguments given'
