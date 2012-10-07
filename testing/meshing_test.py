#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import re
import os
import numpy

from bfdtd.meshobject import *
from bfdtd.meshingparameters import MeshingParameters
#import bfdtd.bfdtd_parser as bfdtd

MeshParamsList = []

mesh = MeshParams()
mesh.setExtension(0, 4)
mesh.setDeltaMax(0.25)
MeshParamsList.append(mesh)

mesh = MeshParams()
mesh.setExtension(0.5, 1.5)
mesh.setDeltaMax(0.20)
MeshParamsList.append(mesh)

mesh = MeshParams()
mesh.setExtension(3.25, 4.25)
mesh.setDeltaMax(0.10)
MeshParamsList.append(mesh)

mesh = MeshParams()
mesh.setExtension(2, 3.25)
mesh.setDeltaMax(0.15)
MeshParamsList.append(mesh)

merged = mergeMeshingParameters(MeshParamsList)

for idx in range(len(MeshParamsList)):
  print('== mesh %d =='%idx)
  print(MeshParamsList[idx])

print('== merged ==')
print(merged)
