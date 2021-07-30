import bpy
import struct
import bmesh
import numpy as np
import os

from math import *
from mathutils import *
from .efo import *
from .utils import *
from .blender_functions import *
from io import BytesIO

def build(efo):

    """
    for shapeHeaderSignature in efo._sSceneDatabase.shapeHeader.keys():

        shapeHeader = efo._sSceneDatabase.shapeHeader[shapeHeaderSignature]

        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty = bpy.context.active_object
        empty.empty_display_size = 0.1
        empty.name = shapeHeader.sShapeHeaderName

        for shapeSignature in shapeHeader.shape:

            shape = efo._sSceneDatabase.shape[shapeSignature]


            construct_mesh(efo._sSceneDatabase, shape,  empty)

            
            get_materials(efo._sSceneDatabase, shape)

            pass
    """

    for skeletonSignature in efo._sSceneDatabase.skeleton.keys():

        skeleton = efo._sSceneDatabase.skeleton[skeletonSignature]

        #bpy.ops.object.empty_add(type='PLAIN_AXES')
        #skeleton_empty = bpy.context.active_object
        #skeleton_empty.empty_display_size = 0.1
        #skeleton_empty.name = skeleton.sSkeletonInfoName

        bone_empty_list = []

        for boneSignature in skeleton.bone:

                bone = efo._sSceneDatabase.bone[boneSignature]

                bpy.ops.object.empty_add(type='PLAIN_AXES')
                bone_empty = bpy.context.active_object
                bone_empty.empty_display_size = 0
                bone_empty.location = bone.translation
                
                if bone.parentIndex == -1:
                    bone_empty.rotation_euler = ( radians(90), 0, 0 )
                
                bone_empty.name = bone.sBoneName
                
                if bone.parentName != "":
                    bone_empty.parent = bone_empty_list[bone.parentIndex]

                if bone.shapeHeader != 0:
                    
                    shapeHeader = efo._sSceneDatabase.shapeHeader[bone.shapeHeader]

                    for shapeSignature in shapeHeader.shape:

                        shape = efo._sSceneDatabase.shape[shapeSignature]

                        construct_mesh(efo._sSceneDatabase, shape,  bone_empty)

                bone_empty_list.append(bone_empty)
                
 
def construct_mesh(sSceneDatabase, shape, shapeHeader):
    mesh = bpy.data.meshes.new(shape.sShapeName)
    obj = bpy.data.objects.new(shape.sShapeName, mesh)

    if bpy.app.version >= (2, 80, 0):
        shapeHeader.users_collection[0].objects.link(obj)
    else:
        shapeHeader.users_collection[0].objects.link(obj)

    obj.parent = shapeHeader

    displayList = sSceneDatabase.displayList[shape.displayList]

    geometry = sSceneDatabase.geometry[displayList.geometry]
    
    primitiveList = sSceneDatabase.primitiveList[displayList.primitiveList[0]] # TEST

    vertexArray = sSceneDatabase.vertexArray[geometry.vertexArray]

    if displayList.displayListRef != 0:
        faces = np.frombuffer(sSceneDatabase.displayList[displayList.displayListRef].index[4:], dtype=np.ushort).tolist()[primitiveList.indexStart:]
    else:
        faces = np.frombuffer(displayList.index[4:], dtype=np.ushort).tolist()[primitiveList.indexStart:]
    
    faces = faces[:primitiveList.indexNumber]
    faces = StripToTriangle(faces)
    
    bm = bmesh.new()
    bm.from_mesh(mesh)

    vertexList = {}
    facesList = []
    normals = []

    # Set vertices
    for j in range(primitiveList.startNumber, primitiveList.endNumber + 1):
        vertex = bm.verts.new(vertexArray.array.array["positions"][j]) # array.array TO CHANGE
        if "normals" in vertexArray.array.array:
                vertex.normal = vertexArray.array.array["normals"][j]
                normals.append(vertexArray.array.array["normals"][j])
        vertex.index = j

        vertexList[j] = vertex 
    
    # Set faces
    for j in range(primitiveList.indexNumber):
        try:
            face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
            face.smooth = True
            facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
        except:
            pass
            #print(shape.sShapeName)
    """
    
    # Set faces
    for j in range(len(faces)):
        try:
            face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
            face.smooth = True
        except:
            for Face in facesList:
                if {vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]} == set(Face[1]):
                    face = Face[0].copy(verts=False, edges=False)
                    face.smooth = True
                    break
        facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
    """

    bm.to_mesh(mesh)
    bm.free()

    # Set normals
    mesh.use_auto_smooth = True

    if normals != []:
        mesh.normals_split_custom_set_from_vertices(normals)

    material = get_materials(sSceneDatabase, shape)

    mesh.materials.append(material)


def get_materials(sSceneDatabase, shape):

    state = sSceneDatabase.state[shape.state]
    
    material = bpy.data.materials.get(state.sStateName)
    if not material:
        material = bpy.data.materials.new(state.sStateName)
    
    
    material.use_nodes = True
    nodes = material.node_tree.nodes

    #texture = sSceneDatabase.texture[state.texture[0]]
    #textureImage = sSceneDatabase.textureImage[texture.textureImage]


    """
    for userParameter in state.userParameter:
        print(userParameter.name)

        if userParameter.name == "teaSA_color":
            pass
        elif userParameter.name == "teaSA_fresnel":
            node = nodes.new('ShaderNodeFresnel')
    """

    return material




            
def main(filepath, clear_scene, import_character):
    if clear_scene == True:
        clearScene()
    efo = EFO(filepath)
    #buildModel(efo, import_character)
    build(efo)
    return {'FINISHED'}

if __name__ == '__main__':
    main()
