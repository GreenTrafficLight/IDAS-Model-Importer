import bpy

from bpy.types import Panel

class IDAS_PT_ImportPAGallery(Panel):
    bl_idname = "IDAS_PT_ImportPAGallery"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    bl_category = "IDAS Importer"
    bl_label = "Gallery label"

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is Gallery")
