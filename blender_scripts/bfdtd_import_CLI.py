#!BPY

import Blender

print Blender.Get('scriptsdir')
Blender.Run(Blender.Get('scriptsdir')+'/layer_manager.py',1323)
