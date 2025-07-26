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

from ...Utilities import *
from ..utils.ImportEFO import *

class IDAS_OT_EFO_Import(Operator, ImportHelper):
    """Load a EFO model file"""
    bl_idname = "import_scene.efo_data"
    bl_label = "Import EFO Data"

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
        importEFO(self.filepath, self.files, self.clear_scene, self.import_textures)
        
        return {'FINISHED'}
    
def importEFO(filepath, files, clear_scene, import_textures):
    
    if clear_scene == True:
        clearScene()

    folder = (os.path.dirname(filepath))

    for i, j in enumerate(files):

        path_to_file = (os.path.join(folder, j.name))

        efo = EFO(path_to_file)
        efoName = path_to_file.split("\\")[-1]

        head = os.path.split(path_to_file)[0]

        if import_textures:

            texture = head + "\\" + "texture.efo"
            if os.path.exists(texture):

                texture_efo = EFO(texture)
                texture_dir = path_to_file.replace(efoName, "textures\\")
                texture_efo.extract_textures(texture_efo, texture_dir)
                texture_efo.extract_textures(efo, texture_dir)

            else:
                
                texture_dir = head + "\\" + efoName[:-4] + "_" + "textures\\"
                texture_efo.extract_textures(efo, texture_dir)
        
        else :

            texture_dir = ""

        build_hierarchy(efo, texture_dir, os.path.splitext(efoName)[0])

    return {'FINISHED'}