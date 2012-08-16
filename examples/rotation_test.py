#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import *
import time
import sys
import os
import numpy
from GWL.GWL_parser import *
  
def main():
  box = GWLobject()
  #box.addZblock(P1=[0,0,0], P2=[1,2,3], LineNumber_Horizontal=10, LineDistance_Horizontal=0.2, LineNumber_Vertical=10, LineDistance_Vertical=0.2, BottomToTop = False)
  #box.addZblock(P1=[0,0,0], P2=[1,2,3], LineNumber_X=10, LineDistance_X=0.2, LineNumber_Y=10, LineDistance_Y=0.2)

  box.clear()
  box.addXblock(P1=[0,0,0], P2=[1,2,3])
  box.write_GWL('X.gwl')

  box.clear()
  box.addYblock(P1=[0,0,0], P2=[1,2,3])
  box.write_GWL('Y.gwl')

  box.clear()
  box.addZblock(P1=[0,0,0], P2=[1,2,3])
  box.write_GWL('Z.gwl')

  #box.rotate(axis_point=[0,0,0], axis_direction=[1,0,0], angle_degrees=0)

if __name__ == "__main__":
  main()
