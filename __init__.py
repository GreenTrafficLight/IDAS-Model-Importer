import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator

from .Blender.operators.OT_EFO_Import import *
from .Blender.operators.OT_TreePath_Import import *
from .Blender.panels.PT_Gallery_Importer import *
from .Blender.panels.PT_TreePath_Importer import *

bl_info = {
	"name": "Import Initial D Arcade Stage (5 to Zero) Models format (.efo)",
	"description": "Import Initial D Arcade Stage Model",
	"author": "GreenTrafficLight",
	"version": (2, 0),
	"blender": (2, 80, 0),
	"location": "File > Import > Initial D Arcade Stage Importer (.efo)",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

classes = [
    TreePathImporterProperties,
    IDAS_OT_EFO_Import,
    IDAS_OT_TreePath_Import,
    IDAS_PT_Gallery_Importer,
    IDAS_PT_TreePath_Importer,
]

def menu_func_import(self, context):
    self.layout.operator(IDAS_OT_EFO_Import.bl_idname, text="Initial D Arcade Stage Model (.efo)")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tree_path_importer_properties = bpy.props.PointerProperty(type=TreePathImporterProperties)
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)