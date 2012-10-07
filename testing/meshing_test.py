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

mesh1 = MeshParams()
mesh1.setExtension(2,10)
mesh1.setDeltaMax(1)

mesh2 = MeshParams()
mesh2.setExtension(5,7)
mesh2.setDeltaMax(0.5)

merged = mergeMeshingParameters([mesh1,mesh2])

print('== mesh1 ==')
print(mesh1)
print('== mesh2 ==')
print(mesh2)
print('== merged ==')
print(merged)
