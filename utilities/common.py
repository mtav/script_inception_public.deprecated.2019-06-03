#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def fixLowerUpper(L,U):
  real_L = [0,0,0]
  real_U = [0,0,0]
  for i in range(3):
    real_L[i] = min(L[i],U[i])
    real_U[i] = max(L[i],U[i])
  return real_L, real_U
