import bpy

class IDAS_PT_Gallery_Importer(bpy.types.Panel):
    bl_label = "Gallery Importer"
    bl_idname = "IDAS_PT_Gallery_Importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout        
        layout.label(text="Gallery Path file")