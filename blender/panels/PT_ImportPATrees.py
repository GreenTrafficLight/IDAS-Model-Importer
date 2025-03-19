import bpy

from bpy.types import Panel

class IDAS_PT_ImportPATrees(Panel):
    bl_idname = "IDAS_PT_ImportPATrees"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    bl_category = "IDAS Importer"
    bl_label = "Trees"

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is Trees")
        
        # Add the operator button to the panel
        op = layout.operator("idas.import_pa_trees", text="Browse Folder")
        
        # Show the selected folder path as a label
        if op.tree_folder_path:
            layout.label(text=f"Selected Folder: {op.tree_folder_path}")
        else:
            layout.label(text="No folder selected.")

