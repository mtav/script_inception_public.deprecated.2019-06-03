#!/usr/bin/env python

import bfdtd.bfdtd_parser
import sys

FDTDobj = bfdtd.bfdtd_parser.readBristolFDTD(sys.argv[1])

for i in range(len(FDTDobj.frequency_snapshot_list)):
  plane = FDTDobj.frequency_snapshot_list[i].plane
  print 'i+1=', i+1, 'name=', FDTDobj.frequency_snapshot_list[i].name, 'plane=', plane, 'f=', FDTDobj.frequency_snapshot_list[i].frequency, 'pos=', FDTDobj.frequency_snapshot_list[i].P1[plane-1]
