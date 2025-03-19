import bpy

from bpy.types import Operator
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        CollectionProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        )

from ..utils.ImportEFO import import_efo

class IDAS_OT_ImportEFO(Operator, ImportHelper):
    bl_idname = "import_scene.import_efo"
    bl_label = "Import IDAS model"

    filename_ext = ".efo"
    filter_glob: StringProperty(default="*.efo", options={'HIDDEN'}, maxlen=255,)

    # Selected files
    files: CollectionProperty(type=bpy.types.PropertyGroup)

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

    def execute(self, context):
        import_efo(self.filepath, self.files, self.clear_scene, self.import_textures)
        
        return {'FINISHED'}

