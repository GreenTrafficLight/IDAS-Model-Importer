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
from bpy_extras import image_utils


def build_hierarchy(efo, texture_dir):

    for skeletonSignature in efo._sSceneDatabase.skeleton.keys():

        skeleton = efo._sSceneDatabase.skeleton[skeletonSignature]

        bpy.ops.object.add(type="ARMATURE")
        ob = bpy.context.object
        ob.rotation_euler = ( radians(90), 0, 0 )
        #ob.matrix_local = Matrix.Rotation(radians(90.0), 4, 'X')
        ob.name = skeleton.sSkeletonName

        # TEST
        #if "Muffler" in efo._sSceneDatabase.sSceneDatabaseName and bpy.context.scene.objects.get("Locator_Muffler"):
            #ob.matrix_local = Matrix.Rotation(radians(90.0), 4, 'X') @ bpy.context.scene.objects["Locator_Muffler"].matrix_local
        
        #if "RetracL" in efo._sSceneDatabase.sSceneDatabaseName and bpy.context.scene.objects.get("Locator_RetracL"):
            #ob.matrix_local = Matrix.Rotation(radians(90.0), 4, 'X') @ bpy.context.scene.objects["Locator_RetracL"].matrix_local

        amt = ob.data
        amt.name = skeleton.sSkeletonName

        bone_mapping = []
        
        for boneSignature in skeleton.bone:

            sBone = efo._sSceneDatabase.bone[boneSignature]
            bone_mapping.append(sBone.sBoneName)

            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bone = amt.edit_bones.new(sBone.sBoneName)

            bone.tail = (0.01 , 0.01, 0.01)
            
            quad = Quaternion((sBone.quaternion[3], sBone.quaternion[0], sBone.quaternion[1], sBone.quaternion[2]))
            mat = quad.to_matrix().to_4x4()
            mat = Matrix.Translation(sBone.translation) @ mat
            bone.matrix = mat

            if sBone.parentIndex != -1:

                parent = efo._sSceneDatabase.bone[sBone.parent]

                bone.parent = amt.edit_bones[parent.sBoneName]
                bone.matrix = amt.edit_bones[parent.sBoneName].matrix @ bone.matrix

                bone.head = bone.matrix.translation

        bones = amt.edit_bones
        for boneSignature in skeleton.bone:

            sBone = efo._sSceneDatabase.bone[boneSignature]

            bone = bones[sBone.sBoneName]

            if sBone.parentIndex != -1:

                parent = efo._sSceneDatabase.bone[sBone.parent]
                
                bone.tail = bones[parent.sBoneName].head

        bpy.ops.object.mode_set(mode='OBJECT')
  
        empty_list = []

        for boneSignature in skeleton.bone:

            bone = efo._sSceneDatabase.bone[boneSignature]

            bpy.ops.object.empty_add(type='PLAIN_AXES', location=bone.translation, scale=bone.scale)
            empty = bpy.context.active_object
            empty.empty_display_size = 0
            empty.name = bone.sBoneName

            empty.matrix_local = bone.mtxLocal
            
            if bone.rotation != 0:
                empty.rotation_euler = bone.rotation

            if bone.parentIndex == -1:
                empty.parent = ob
                
            if bone.parentName != "":
                
                empty.parent = empty_list[bone.parentIndex]

            if bone.shapeHeader != 0:
                
                shapeHeader = efo._sSceneDatabase.shapeHeader[bone.shapeHeader]

                for shapeSignature in shapeHeader.shape:

                    shape = efo._sSceneDatabase.shape[shapeSignature]

                    build_mesh(efo._sSceneDatabase, shape,  empty, texture_dir, bone_mapping, ob)

            empty_list.append(empty)


def build_mesh(sSceneDatabase, shape, shapeHeader, texture_dir, bone_mapping, armature):
    mesh = bpy.data.meshes.new(shape.sShapeName)
    obj = bpy.data.objects.new(shape.sShapeName, mesh)

    if bpy.app.version >= (2, 80, 0):
        shapeHeader.users_collection[0].objects.link(obj)
    else:
        shapeHeader.users_collection[0].objects.link(obj)

    modifier = obj.modifiers.new(armature.name, type="ARMATURE")
    modifier.object = bpy.data.objects[armature.name]

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
        vertex = bm.verts.new(vertexArray.array.array["positions"][j])
        
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
    
    """
    for i in range(primitiveList.startNumber, primitiveList.endNumber + 1):
        if "boneIndices" in vertexArray.array.array:
            for k, vg in enumerate(vertexArray.array.array["boneIndices"][i]):
                vg_name = bone_mapping[vg + 1]
                if not vg_name in obj.vertex_groups:
                    group = obj.vertex_groups.new(name=vg_name)
                else:
                    group = obj.vertex_groups[vg_name]
                weight = vertexArray.array.array["boneWeights"][i][k]
                if weight > 0.0:
                    group.add([i - primitiveList.startNumber], 1.0, 'REPLACE')
    """

    # Set normals
    mesh.use_auto_smooth = True

    if normals != []:
        mesh.normals_split_custom_set_from_vertices(normals)

    material = get_materials(sSceneDatabase, shape, texture_dir)

    mesh.materials.append(material)


def get_materials(sSceneDatabase, shape, texture_dir):

    state = sSceneDatabase.state[shape.state]
    
    material = bpy.data.materials.get(state.sStateName)

    print(state.sStateName)
    print(state.fillType)
    print(state.opacity)
    
    if not material:
        material = bpy.data.materials.new(state.sStateName)

        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        bsdf =  material.node_tree.nodes["Principled BSDF"]
        output = material.node_tree.nodes["Material Output"]

        if "teaSA_color" in state.userParameter:
            bsdf.inputs['Base Color'].default_value = (state.userParameter["teaSA_color"][0], state.userParameter["teaSA_color"][1], state.userParameter["teaSA_color"][2], 1)

        if state.texture != []:
            
            for texture in state.texture:

                sTexture = sSceneDatabase.texture[texture]

                texture_filepath = f"{texture_dir}{sTexture.fileName}"

                if os.path.isfile(texture_filepath):

                    #texture_file = bpy.data.images.load(texture_filepath)
                    texture_file = image_utils.load_image(texture_filepath, check_existing=True)

                    #print(sTexture.fileName)
                    #print(sTexture.format)
                    #print(sTexture.alphaMode)

                    if sTexture.textureType == 1: # Diffuse
                        
                        diffuseTextureImage_node = nodes.new(type='ShaderNodeTexImage')
                        diffuseTextureImage_node.image = texture_file

                        links.new(bsdf.inputs['Base Color'], diffuseTextureImage_node.outputs['Color'])
                        links.new(bsdf.inputs['Alpha'], diffuseTextureImage_node.outputs['Alpha'])

                        if "teaSA_color" in state.userParameter:

                            mixRGB_node = nodes.new(type="ShaderNodeMixRGB")
                            mixRGB_node.blend_type = 'MULTIPLY'
                            links.new(bsdf.inputs['Base Color'], mixRGB_node.outputs['Color'])
                            mixRGB_node.inputs['Color1'].default_value = (state.userParameter["teaSA_color"][0], state.userParameter["teaSA_color"][1], state.userParameter["teaSA_color"][2], 1)                    
                            mixRGB_node.inputs['Fac'].default_value = 1.0
                            links.new(mixRGB_node.inputs['Color2'], diffuseTextureImage_node.outputs['Color'])

                    elif sTexture.textureType == 3: # Normal

                        normalTextureImage_node = nodes.new("ShaderNodeTexImage")
                        normalTextureImage_node.image = texture_file
                        
                        normalMapNode = nodes.new("ShaderNodeNormalMap")
                        
                        links.new(normalMapNode.inputs[1], normalTextureImage_node.outputs[0])
                        links.new(bsdf.inputs['Normal'], normalMapNode.outputs[0])

                    elif sTexture.textureType == 5: # Specular

                        specularTextureImage_node = nodes.new("ShaderNodeTexImage")
                        specularTextureImage_node.image = texture_file
                        
                        links.new(bsdf.inputs['Specular'], specularTextureImage_node.outputs['Color'])

                    else:
                        
                        #print(sTexture.textureType)
                        pass

    # TEST
    elif material:

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        node = nodes.get("Image Texture", None)
        
        if node is None and state.texture != []:
            
            bsdf =  material.node_tree.nodes["Principled BSDF"]
            output = material.node_tree.nodes["Material Output"]

            for texture in state.texture:

                sTexture = sSceneDatabase.texture[texture]

                texture_filepath = f"{texture_dir}{sTexture.fileName}"

                if os.path.isfile(texture_filepath):

                    texture_file = image_utils.load_image(texture_filepath, check_existing=True)

                    #print(sTexture.fileName)
                    #print(sTexture.format)
                    #print(sTexture.alphaMode)

                    if sTexture.textureType == 1: # Diffuse
                        
                        diffuseTextureImage_node = nodes.new(type='ShaderNodeTexImage')
                        diffuseTextureImage_node.image = texture_file

                        links.new(bsdf.inputs['Base Color'], diffuseTextureImage_node.outputs['Color'])
                        links.new(bsdf.inputs['Alpha'], diffuseTextureImage_node.outputs['Alpha'])

                        if "teaSA_color" in state.userParameter:

                            mixRGB_node = nodes.new(type="ShaderNodeMixRGB")
                            mixRGB_node.blend_type = 'MULTIPLY'
                            links.new(bsdf.inputs['Base Color'], mixRGB_node.outputs['Color'])
                            mixRGB_node.inputs['Color1'].default_value = bsdf.inputs['Base Color'].default_value
                            mixRGB_node.inputs['Fac'].default_value = 1.0                    
                            links.new(mixRGB_node.inputs['Color2'], diffuseTextureImage_node.outputs['Color'])

                    elif sTexture.textureType == 3: # Normal
                        normalTextureImage_node = nodes.new("ShaderNodeTexImage")
                        normalTextureImage_node.image = texture_file
                        
                        normalMapNode = nodes.new("ShaderNodeNormalMap")
                        
                        links.new(normalMapNode.inputs[1], normalTextureImage_node.outputs[0])
                        links.new(bsdf.inputs['Normal'], normalMapNode.outputs[0])

                    elif sTexture.textureType == 5: # Specular
                        
                        specularTextureImage_node = nodes.new("ShaderNodeTexImage")
                        specularTextureImage_node.image = texture_file
                        
                        links.new(bsdf.inputs['Specular'], specularTextureImage_node.outputs['Color'])

                    else:
                        
                        #print(sTexture.textureType)
                        pass

    if state.fillType == 0:
        material.blend_method = 'OPAQUE'
    elif state.fillType == 1:
        material.blend_method = 'CLIP'
    elif state.fillType == 2:
        material.blend_method = 'BLEND'
    else:
        material.blend_method = 'OPAQUE'

    return material


def extract_textures(efo, texture_dir):

    for textureImageSignature, textureImage in efo._sSceneDatabase.textureImage.items():
            #if textureImageSignature > 0 and not os.path.isfile(texture_dir + textureImage.fileName):
            if textureImageSignature > 0 and textureImage.fileName != None and not os.path.isfile(texture_dir + textureImage.fileName):
                if not os.path.exists(texture_dir):
                    os.mkdir(texture_dir)
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
        extract_textures(texture_efo, texture_dir)
        extract_textures(efo, texture_dir)
    else:
        
        texture_dir = head + "\\" + efoName[:-4] + "_" + "textures\\"
        extract_textures(efo, texture_dir)

    build_hierarchy(efo, texture_dir)
    return {'FINISHED'}


if __name__ == '__main__':
    main()
