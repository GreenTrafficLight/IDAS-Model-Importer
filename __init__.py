bl_info = {
	"name": "Import Initial D Arcade Stage (5 to Zero) Models format (.efo)",
	"description": "Import Initial D Arcade Stage Model",
	"author": "GreenTrafficLight",
	"version": (1, 1),
	"blender": (2, 80, 0),
	"location": "File > Import > Initial D Arcade Stage Importer (.efo)",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"support": "COMMUNITY",
	"category": "Import-Export"}

import bpy
import os

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportEFO(Operator, ImportHelper):
    """Load a EFO model file"""
    bl_idname = "import_scene.efo_data"
    bl_label = "Import EFO Data"

    filename_ext = ".efo"
    filter_glob: StringProperty(default="*.efo", options={'HIDDEN'}, maxlen=255,)

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    clear_scene: BoolProperty(
        name="Clear scene",
        description="Example Tooltip",
        default=False,
    )

    import_textures: BoolProperty(
        name="Import textures",
        description="Example Tooltip",
        default=True,
    )

    def execute(self, context):
        from . import  import_efo
        import_efo.main(self.filepath, self.clear_scene)
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportEFO.bl_idname, text="Initial D Arcade Stage Model (.efo)")


def register():
    bpy.utils.register_class(ImportEFO)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportEFO)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
