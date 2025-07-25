import bpy

from ...Formats.EFO.efoFile import *

class IDAS_OT_TreePath_Import(bpy.types.Operator):
        bl_idname = "import_idas.treepathimport_operator"
        bl_label = "Import Tree Path"

        def execute(self, context):   
            props = context.scene.tree_path_importer_properties

            treeModel = EFO(props.tree_model_file)

            return {'FINISHED'}