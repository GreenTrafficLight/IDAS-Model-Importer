import bpy

from ...Formats.EFO.efoFile import *
from ...Formats.pa8 import *

from ..utils.ImportEFO import *

class IDAS_OT_TreePath_Import(bpy.types.Operator):
        bl_idname = "import_idas.treepathimport_operator"
        bl_label = "Import Tree Path"

        def execute(self, context):   
            props = context.scene.tree_path_importer_properties

            treeModel = EFO(props.tree_model_file)
            treeName = props.tree_model_file.split("\\")[-1]
            
            if props.import_textures:
                treeNameHead = os.path.split(props.tree_model_file)[0]
                common_texture_dir = treeNameHead + "\\" + treeName[:-4] + "_" + "textures\\"

            build_hierarchy(treeModel, common_texture_dir, os.path.splitext(treeName)[0])

            treePath = PA(props.tree_path_file)

            return {'FINISHED'}