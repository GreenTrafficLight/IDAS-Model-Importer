import bpy

from .blender.operators.OT_ImportEFO import *
from .blender.operators.OT_ImportPATrees import *

from .blender.panels.PT_ImportPATrees import *
from .blender.panels.PT_ImportPAGallery import *

bl_info = {
	"name": "Import Initial D Arcade Stage (5 to Zero) Models format (.efo)",
	"description": "Import Initial D Arcade Stage Model",
	"author": "GreenTrafficLight",
	"version": (2, 0),
	"blender": (4, 2, 0),
	"location": "File > Import > Initial D Arcade Stage Importer (.efo)",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

classes = [
    IDAS_OT_ImportEFO,
    IDAS_OT_ImportPATrees,
    IDAS_PT_ImportPATrees,
    IDAS_PT_ImportPAGallery
]

def menu_func_import(self, context):
    self.layout.operator(IDAS_OT_ImportEFO.bl_idname, text="Initial D Arcade Stage Model (.efo)")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
