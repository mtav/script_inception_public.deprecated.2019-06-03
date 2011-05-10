#!/usr/bin/env python

import bfdtd.bfdtd_parser

toto= bfdtd.bfdtd_parser.readBristolFDTD('rectangular_holes.bottomN_30.topN_15.excitationType_Zm1.in')

for i in range(len(toto.frequency_snapshot_list)):
  print i, toto.frequency_snapshot_list[i].name, toto.frequency_snapshot_list[i].plane
