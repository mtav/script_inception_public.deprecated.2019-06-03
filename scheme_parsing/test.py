#!/usr/bin/env python

import pyscheme.parser
import pyscheme.parser
import pyscheme.scheme
import pyscheme.expressions
import sys

def parseFile(filename):
	print "Processing "+filename;
	FILE = open(filename,'r');
	str = FILE.read();
	FILE.close();
	program = pyscheme.parser.parse('('+str+')')
	print program


for arg in sys.argv[1:]: 
	parseFile(arg);
