#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import fnmatch
import os
import string
from optparse import OptionParser
import glob
import re
from subprocess import call

title='test'
width1=0.9
width2=1
texfile='/tmp/tmp.tex'
picture1='/tmp/resonance.png'
picture_list=['/tmp/FS.png','/tmp/FS.png']

with open(texfile, 'w') as f:
  f.write('\documentclass{beamer}\n')
  f.write('\usetheme{Copenhagen}\n')
  f.write('\n')
  f.write('\usepackage{grffile}\n')
  f.write('\n')
  f.write('\\begin{document}\n')
  f.write('\n')
  f.write('\\begin{frame}{'+title+'}\\begin{center}\includegraphics[width='+str(width1)+' \\textwidth]{'+picture1+'}\end{center}\end{frame}\n')
  for pic in picture_list:
    f.write('\\begin{frame}{'+title+'}\\begin{center}\includegraphics[width='+str(width2)+' \\textwidth]{'+pic+'}\end{center}\end{frame}\n')
  f.write('\n')
  f.write('\end{document}\n')

cmd=['cat', texfile]
print cmd
call(cmd)

cmd=['pdflatex','-output-directory', os.path.dirname(texfile), texfile]
print cmd
call(cmd)
