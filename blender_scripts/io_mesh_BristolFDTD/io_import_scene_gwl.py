# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    'name': 'Import GWL Format (.gwl)',
    'author': 'mtav',
    'version': (0, 0, 1),
    'blender': (2, 5, 8),
    'location': 'File > Import > GWL (.gwl)',
    'description': 'Import files in the GWL format (.gwl)',
    'warning': 'Under construction! Visit github for details.',
    'wiki_url': '',
    'tracker_url': '',
    'support': 'UNOFFICIAL',
    'category': 'Import-Export',
    }

import os
import codecs
import math
from math import sin, cos, radians
import bpy
from mathutils import Vector, Matrix

from blender_scripts.GWL_import import *

class IMPORT_GWL(bpy.types.Operator):
    '''Import from GWL file format (.gwl)'''
    bl_idname = "import_scene.gwl"
    bl_description = 'Import from GWL file format (.gwl)'
    bl_label = "Import GWL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'UNDO'}

    filepath = StringProperty(subtype='FILE_PATH')
         
    def execute(self, context):
        print('Importing: ' + self.filepath)
        importGWL(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    self.layout.operator(IMPORT_GWL.bl_idname, text="GWL (.gwl)")

def register():
    print('registering '+str(__name__))
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_func)


if __name__ == "__main__":
    register()


