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

def add_empty(name, parent = None, empty_location=(0.0, 0.0, 0.0), empty_rotation=(0.0, 0.0, 0.0), empty_scale=(0.0, 0.0, 0.0)):

    empty = bpy.context.scene.objects.get(name)
    if empty != None and empty.parent != parent:
        empty = None

    if empty == None:
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', location = empty_location, rotation = empty_rotation, scale = empty_scale)
        empty = bpy.context.active_object
        empty.empty_display_size = 0.1
        empty.name = name
        if parent:
            empty.parent = parent

    return empty

def delete_hierarchy(name):

    objects = bpy.context.scene.objects[name]

    def recurse(ob, parent, depth):
        if not ob.children:
            bpy.data.objects.remove(ob, do_unlink=True)
            return
        
        for child in ob.children:
            recurse(child, ob,  depth + 1)

        bpy.data.objects.remove(ob, do_unlink=True)

    recurse(objects, objects.parent, 0)