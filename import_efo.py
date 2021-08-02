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

def build_hierarchy(efo, texture_dir):

    for skeletonSignature in efo._sSceneDatabase.skeleton.keys():

        skeleton = efo._sSceneDatabase.skeleton[skeletonSignature]

        #bpy.ops.object.empty_add(type='PLAIN_AXES')
        #skeleton_empty = bpy.context.active_object
        #skeleton_empty.empty_display_size = 0.1
        #skeleton_empty.name = skeleton.sSkeletonInfoName

        bpy.ops.object.add(type="ARMATURE")
        ob = bpy.context.object
        ob.rotation_euler = ( radians(90), 0, 0 )
        ob.name = skeleton.sSkeletonName
        
        amt = ob.data
        amt.name = skeleton.sSkeletonName

        
        """
        for boneSignature in skeleton.bone:

            if bone.vertexBlendTarget == -1:

                pass
        """
        empty_list = []

        for boneSignature in skeleton.bone:

            bone = efo._sSceneDatabase.bone[boneSignature]

            #if bone.vertexBlendTarget == 0:

            bpy.ops.object.empty_add(type='PLAIN_AXES', location=bone.translation, scale=bone.scale)
            empty = bpy.context.active_object
            empty.empty_display_size = 0
            empty.name = bone.sBoneName
            
            if bone.rotation != 0:
                empty.rotation_euler = bone.rotation

            if bone.parentIndex == -1:
                #bone_empty.rotation_euler = ( radians(90), 0, 0 )
                empty.parent = ob
                
            if bone.parentName != "":
                
                empty.parent = empty_list[bone.parentIndex]

            if bone.shapeHeader != 0:
                
                shapeHeader = efo._sSceneDatabase.shapeHeader[bone.shapeHeader]

                for shapeSignature in shapeHeader.shape:

                    shape = efo._sSceneDatabase.shape[shapeSignature]

                    build_mesh(efo._sSceneDatabase, shape,  empty, texture_dir)

            empty_list.append(empty)
            """
            elif bone.vertexBlendTarget == -1:

                bpy.context.view_layer.objects.active = ob
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                obArm = bpy.context.active_object #get the armature object
                ebs = obArm.data.edit_bones
                eb = ebs.new(bone.sBoneName)
                eb.head = (0, 1, 1) # if the head and tail are the same, the bone is deleted
                eb.tail = (0, 1, 2)    # upon returning to object mode
                bpy.ops.object.mode_set(mode='OBJECT')

                if bone.parentName != "":
                
                    eb.parent = bone_empty_list[bone.parentIndex]

                bone_empty_list.append(ebs)
            """


 
def build_mesh(sSceneDatabase, shape, shapeHeader, texture_dir):
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

    if "texCoordsLayer1" in vertexArray.array.array:
        uv_layer1 = bm.loops.layers.uv.new()
    if "texCoordsLayer2" in vertexArray.array.array:
        uv_layer2 = bm.loops.layers.uv.new()

    # Set vertices
    for j in range(primitiveList.startNumber, primitiveList.endNumber + 1):
        vertex = bm.verts.new(vertexArray.array.array["positions"][j]) # array.array TO CHANGE
        if "normals" in vertexArray.array.array:
                vertex.normal = vertexArray.array.array["normals"][j]
                normals.append(vertexArray.array.array["normals"][j])
        vertex.index = j

        vertexList[j] = vertex 
    
    # Set faces
    for j in range(len(faces)):
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

    # Set uv
    for f in bm.faces:
        if "texCoordsLayer1" in vertexArray.array.array:
            for l in f.loops:
                l[uv_layer1].uv = [vertexArray.array.array["texCoordsLayer1"][l.vert.index][0], 1 - vertexArray.array.array["texCoordsLayer1"][l.vert.index][1]]
        if "texCoordsLayer2" in vertexArray.array.array:
            for l in f.loops:
                l[uv_layer2].uv = [vertexArray.array.array["texCoordsLayer1"][l.vert.index][0], 1 - vertexArray.array.array["texCoordsLayer1"][l.vert.index][1]]

    # Set colors
    if "colors" in vertexArray.array.array:
        color_layer = bm.loops.layers.color.new("Color")
        for f in bm.faces:
            for l in f.loops:
                l[color_layer] = vertexArray.array.array["colors"][l.vert.index]

    bm.to_mesh(mesh)
    bm.free()

    # Set normals
    mesh.use_auto_smooth = True

    if normals != []:
        mesh.normals_split_custom_set_from_vertices(normals)

    material = get_materials(sSceneDatabase, shape, texture_dir)

    mesh.materials.append(material)


def get_materials(sSceneDatabase, shape, texture_dir):

    state = sSceneDatabase.state[shape.state]
    
    material = bpy.data.materials.get(state.sStateName)
    if not material:
        material = bpy.data.materials.new(state.sStateName)

    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    bsdf =  material.node_tree.nodes["Principled BSDF"]

    if state.texture != []:
        texture = sSceneDatabase.texture[state.texture[0]]
        textureImage = sSceneDatabase.textureImage[texture.textureImage]

        texture_file = f"{texture_dir}{texture.fileName}"

        if os.path.isfile(texture_file):
            texture_image = nodes.new(type='ShaderNodeTexImage')
            texture_image.image = bpy.data.images.load(texture_file)

            material.node_tree.links.new(bsdf.inputs['Base Color'], texture_image.outputs['Color'])


    """
    for userParameter in state.userParameter:
        print(userParameter.name)

        if userParameter.name == "teaSA_color":
            pass
        elif userParameter.name == "teaSA_fresnel":
            node = nodes.new('ShaderNodeFresnel')
    """

    return material


def extract_textures(efo, texture_dir):

    for textureImageSignature, textureImage in efo._sSceneDatabase.textureImage.items():
        if textureImageSignature > 0 and not os.path.isfile(texture_dir + textureImage.fileName):
            f = open(texture_dir + textureImage.fileName, "wb")
            f.write(textureImage.file)
            f.close()




            
def main(filepath, clear_scene):
    if clear_scene == True:
        clearScene()
    efo = EFO(filepath)
    efoName = filepath.split("\\")[-1]

    head = os.path.split(filepath)[0]
    tail = os.path.split(filepath)[1]
    
    texture = head + "\\" + "texture.efo"
    if os.path.exists(texture):
        texture_efo = EFO(texture)
        texture_dir = filepath.replace(efoName, "textures\\")
        if not os.path.exists(texture_dir):
            os.mkdir(texture_dir)
        extract_textures(texture_efo, texture_dir)
    else:
        texture_dir = head + "\\" + efoName[:-4] + "_" + "textures\\"
        if not os.path.exists(texture_dir):
            os.mkdir(texture_dir)
        extract_textures(efo, texture_dir)

    build_hierarchy(efo, texture_dir)
    return {'FINISHED'}

if __name__ == '__main__':
    main()
