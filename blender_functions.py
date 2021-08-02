import bpy

def clearScene():
    for object in bpy.context.scene.objects:
        bpy.data.objects.remove(object, do_unlink=True)

    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

    for image in bpy.data.images:
        bpy.data.images.remove(image)