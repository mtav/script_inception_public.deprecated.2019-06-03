#!/usr/bin/env python
# -*- coding: utf-8 -*-

# generate grid of woodpiles

from GWL.GWL_parser import *

Lambda_list = [0.780,1.550]
wh_list = [(0.2,0.25),(0.3/sqrt(2.0),0.7/sqrt(2.0))]
a_over_Lambda_list = [0.9199,0.8333]

for Lambda in Lambda_list:
  for a_over_Lambda in a_over_Lambda_list:
    a = a_over_Lambda*Lambda
    woodpile_obj = Woodpile()
    GWL_obj = woodpile_obj.getGWL()
    GWL_obj.interLayerDistance = a/4.0
    GWL_obj.interRodDistance = a/sqrt(2.0)
    GWL_obj.write_GWL('woodpile.Lambda_'+str(Lambda)+'.a_'+a+'.gwl')
  
