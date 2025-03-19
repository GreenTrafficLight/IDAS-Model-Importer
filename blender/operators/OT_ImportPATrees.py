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

class IDAS_OT_ImportPATrees(Operator, ImportHelper):
    bl_idname = "idas.import_pa_trees"
    bl_label = "Import IDAS Trees"

    tree_folder_path: bpy.props.StringProperty(
        name="Folder Path",
        description="Select the folder containing trees",
        subtype='DIR_PATH'
    )

    def execute(self, context):        
        return {'FINISHED'}

