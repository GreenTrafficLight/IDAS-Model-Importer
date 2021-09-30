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

import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportEFO(Operator, ImportHelper):
    """Load a EFO model file"""
    bl_idname = "import_scene.efo_data"
    bl_label = "Import EFO Data"

    filename_ext = ".efo"
    filter_glob: StringProperty(default="*.efo", options={'HIDDEN'}, maxlen=255,)

    clear_scene: BoolProperty(
        name="Clear scene",
        description="Clear everything from the scene",
        default=False,
    )

    import_textures: BoolProperty(
        name="Import textures",
        description="Import the model with textures applied",
        default=True,
    )

    import_gallery = EnumProperty(
        name="Import gallery",
        description="Choose which gallery to import",
        items=(
            ('OPT_A', "None", "Don't import gallery"),
            
            ('OPT_B', "Dry (Summer)", "Import gallery from summer"),
            ('OPT_C', "Rain (Summer)", "Import gallery from summer and when it rain"),
            
            ('OPT_D', "Dry (Winter)", "Import gallery from winter"),
            ('OPT_E', "Rain (Winter)", "Import gallery from winter and when it rain"),
            
            ('OPT_F', "Dry (Snow)", "Import gallery from snow maps"),
            ('OPT_G', "Rain (Snow)", "Import gallery from snow maps and when it rain"),
        ),
        default='OPT_A',
    )

    import_trees = EnumProperty(
        name="Import trees",
        description="Choose which lod to import from trees",
        items=(
            ('OPT_A', "None", "Don't import trees"),
            ('OPT_B', "LOD A", "Import trees from LOD A"),
            ('OPT_C', "LOD B", "Import trees from LOD B"),
            ('OPT_D', "LOD C", "Import trees from LOD C"),
        ),
        default='OPT_A',
    )


    def execute(self, context):
        from . import  import_efo
        import_efo.main(self.filepath, self.clear_scene, self.import_textures, self.import_trees, self.import_gallery)
        return {'FINISHED'}

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
