import bpy

class TreePathImporterProperties(bpy.types.PropertyGroup):
    tree_path_file: bpy.props.StringProperty(
        name="Tree Path File",
        subtype='FILE_PATH'
    )

    tree_model_file: bpy.props.StringProperty(
        name="Tree Model File",
        subtype='FILE_PATH'
    )

    tree_lod : bpy.props.EnumProperty(
        name="Tree LOD",
        description="Choose which lod to import for the trees",
        items=(
            ('OPT_A', "LOD A", "Import trees from LOD A"),
            ('OPT_B', "LOD B", "Import trees from LOD B"),
            ('OPT_C', "LOD C", "Import trees from LOD C"),
        ),
        default='OPT_A',
    )

    import_textures: bpy.props.BoolProperty(
        name="Import Textures",
        description="Import textures of the trees",
        default=False
    )
    
class IDAS_PT_TreePath_Importer(bpy.types.Panel):
    bl_label = "Tree Path Importer"
    bl_idname = "IDAS_PT_TreePath_importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        props = context.scene.tree_path_importer_properties
        
        layout.label(text="Tree Path file")
        layout.prop(props, "tree_path_file", text="")

        layout.label(text="Tree Model file")
        layout.prop(props, "tree_model_file", text="")

        layout.label(text="Tree LOD")
        layout.prop(props, "tree_lod", text= "")

        layout.prop(props, "import_textures")

        layout.separator() 

        # Button that calls the operator
        row = layout.row()
        row.enabled = bool(props.tree_path_file and props.tree_model_file)
        row.operator("import_idas.treepathimport_operator", text="Import")