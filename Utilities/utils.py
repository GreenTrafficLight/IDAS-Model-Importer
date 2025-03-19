import bpy

from mathutils import *

def clear_scene():
    
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

def StripToTriangle(triangleStripList):
    faces = []
    cte = 0
    for i in range(2, len(triangleStripList)):
        if triangleStripList[i] == 65535 or triangleStripList[i - 1] == 65535 or triangleStripList[i - 2] == 65535:
            if i % 2 == 0:
                cte = -1
            else:
                cte = 0
            pass
        else:
            if (i + cte) % 2 == 0:
                a = triangleStripList[i - 2]
                b = triangleStripList[i - 1]
                c = triangleStripList[i]
            else:
                a = triangleStripList[i - 1]
                b = triangleStripList[i - 2]
                c = triangleStripList[i]

            if a != b and b != c and c != a:
                faces.append([a, b, c])
    return faces

def ConvertNormal_S10S11S11(integer, reverse=False):
    
    p1 = (integer & 0xFFC00000) >> 22
    p2 = (integer & 0x003FF800) >> 11
    p3 = (integer & 0x000007FF)

    if p1 & 0x200:
        r1 = -((0x200 - (p1 & 0x1FF))) / 0x1FF
    else:
        r1 = p1 / 0x1FF

    if p2 & 0x400:
        r2 = -((0x400 - (p2 & 0x3FF))) / 0x3FF
    else:
        r2 = p2 / 0x3FF

    if p3 & 0x400:
        r3 = -((0x400 - (p3 & 0x3FF))) / 0x3FF
    else:
        r3 = p3 / 0x3FF

    if reverse == True:
        normal = Vector((r3, r2, r1)).normalized()
    else:
        normal = Vector((r1, r2, r3)).normalized()

    return normal

def Matrix4x3To4x4(matrix):
    newMatrix = Matrix()
    newMatrix[0] = matrix[0]
    newMatrix[1] = matrix[1]
    newMatrix[2] = matrix[2]
    return newMatrix