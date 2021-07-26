import bpy

def clearScene():
    for object in bpy.context.scene.objects:
        bpy.data.objects.remove(object, do_unlink=True)

    for material in bpy.data.materials:
        bpy.data.materials.remove(material)