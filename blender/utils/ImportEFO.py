import bpy
import struct
import bmesh
import numpy as np
import os

from math import *
import mathutils
from bpy_extras import image_utils
from collections import *

from ...formats.EFO import EFO
from ...utilities import *

# Meshes

def build_hierarchy(efo, textureDir, filename):

    for skeletonSignature in efo._sSceneDatabase.skeleton.keys():

        skeleton = efo._sSceneDatabase.skeleton[skeletonSignature]

        amt = bpy.data.armatures.new(skeleton.name)
        ob = bpy.data.objects.new(skeleton.name, amt)
        ob.rotation_euler = (radians(90), 0, 0)

        sceneCollection = bpy.context.scene.collection  # Get the default collection
        sceneCollection.objects.link(ob)

        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')

        bone_mapping = []

        for boneSignature in skeleton.bone:

            sBone = efo._sSceneDatabase.bone[boneSignature]
            bone_mapping.append(sBone.name)

            bone = ob.data.edit_bones.new(sBone.name)
            bone.tail = (0.01, 0.01, 0.01)

            quad = mathutils.Quaternion((sBone.quaternion[3], sBone.quaternion[0], sBone.quaternion[1], sBone.quaternion[2]))
            mat = quad.to_matrix().to_4x4()
            mat = mathutils.Matrix.Translation(sBone.translation) @ mat
            bone.matrix = mat

            if sBone.parentIndex != -1:
                parent = efo._sSceneDatabase.bone[sBone.parent]
                bone.parent = ob.data.edit_bones[parent.name]
                bone.matrix = bone.parent.matrix @ bone.matrix
                bone.head = bone.matrix.translation

        bones = ob.data.edit_bones
        for boneSignature in skeleton.bone:

            sBone = efo._sSceneDatabase.bone[boneSignature]
            bone_name = sBone.name[:63] if len(sBone.name) > 63 else sBone.name
            bone = bones[bone_name]

            if sBone.parentIndex != -1:
                parent = efo._sSceneDatabase.bone[sBone.parent]
                bone.tail = bones[parent.name].head

        bpy.ops.object.mode_set(mode='OBJECT')

        empty_list = []

        for boneSignature in skeleton.bone:
            
            dummy = efo._sSceneDatabase.bone[boneSignature]

            empty = bpy.data.objects.new(dummy.name, None)
            empty.empty_display_type = 'PLAIN_AXES'
            empty.empty_display_size = 0.05

            sceneCollection.objects.link(empty)

            empty.location = mathutils.Vector(dummy.translation)
            empty.matrix_local = mathutils.Matrix(Matrix4x3To4x4(dummy.mtxLocal))
            
            if dummy.rotation != 0:
                empty.rotation_euler = mathutils.Vector(dummy.rotation)

            if dummy.parentIndex == -1:
                empty.parent = ob
                
            if dummy.parentName != "":
                
                empty.parent = empty_list[dummy.parentIndex]

            if dummy.shapeHeader != 0:
                
                shapeHeader = efo._sSceneDatabase.shapeHeader[dummy.shapeHeader]

                for shapeSignature in shapeHeader.shape:

                    shape = efo._sSceneDatabase.shape[shapeSignature]

                    build_mesh(efo._sSceneDatabase, shape, empty, textureDir, bone_mapping, ob)

            empty_list.append(empty)

def build_mesh(sSceneDatabase, shape, empty, textureDir, boneMapping, armature):  

    mesh = bpy.data.meshes.new(shape.name)
    obj = bpy.data.objects.new(shape.name, mesh)

    empty.users_collection[0].objects.link(obj)

    modifier = obj.modifiers.new(armature.name, type="ARMATURE")
    modifier.object = bpy.data.objects[armature.name]

    obj.parent = empty

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
        except:
            for Face in facesList:
                if set([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]) == set(Face[1]):
                    face = Face[0].copy(verts=False, edges=True)
                    face.normal_flip()
                    face.smooth = True
                    break
                
        facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])

    # Set uv
    for f in bm.faces:
        if "texCoordsLayer1" in vertexArray.array.array:
            for l in f.loops:
                l[uv_layer1].uv = [vertexArray.array.array["texCoordsLayer1"][l.vert.index][0], 1 - vertexArray.array.array["texCoordsLayer1"][l.vert.index][1]]
        if "texCoordsLayer2" in vertexArray.array.array:
            for l in f.loops:
                l[uv_layer2].uv = [vertexArray.array.array["texCoordsLayer2"][l.vert.index][0], 1 - vertexArray.array.array["texCoordsLayer2"][l.vert.index][1]]

    # Set colors
    if "colors" in vertexArray.array.array:
        color_layer = bm.loops.layers.color.new("Color")
        for f in bm.faces:
            for l in f.loops:
                l[color_layer] = vertexArray.array.array["colors"][l.vert.index]

    bm.to_mesh(mesh)
    bm.free()

    for i in range(primitiveList.vertexNumber):
        if "boneIndices" in vertexArray.array.array:
            for k, vg in enumerate(vertexArray.array.array["boneIndices"][i + primitiveList.startNumber]):
                vg_name = boneMapping[vg + 1]
                if not vg_name in obj.vertex_groups:
                    group = obj.vertex_groups.new(name=vg_name)
                else:
                    group = obj.vertex_groups[vg_name]
                weight = vertexArray.array.array["boneWeights"][i + primitiveList.startNumber][k]
                if weight > 0.0:
                    group.add([i], weight, 'REPLACE')

    # Set normals
    if bpy.app.version < (4, 1, 0):
        mesh.use_auto_smooth = True

    if normals != []:
        mesh.normals_split_custom_set_from_vertices(normals)

    material = get_materials(sSceneDatabase, shape, textureDir)

    mesh.materials.append(material)

    for blendGeometry in displayList.blendGeometry.values():

        mesh = bpy.data.meshes.new(blendGeometry.name)
        obj = bpy.data.objects.new(blendGeometry.name, mesh)

        empty.users_collection[0].objects.link(obj)

        modifier = obj.modifiers.new(armature.name, type="ARMATURE")
        modifier.object = bpy.data.objects[armature.name]

        obj.parent = empty

        obj.hide_set(True)

        vertexArray = sSceneDatabase.vertexArray[blendGeometry.vertexArray]
        
        bm = bmesh.new()
        bm.from_mesh(mesh)

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
            except:
                for Face in facesList:
                    if set([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]) == set(Face[1]):
                        face = Face[0].copy(verts=False, edges=True)
                        face.normal_flip()
                        face.smooth = True
                        break
                    
            facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])

        bm.to_mesh(mesh)
        bm.free()

# Materials

def get_materials(sSceneDatabase, shape, textureDir):

    state = sSceneDatabase.state[shape.state]
    
    material = bpy.data.materials.get(state.name)
    
    if not material:
        
        material = bpy.data.materials.new(state.name)

        material.use_nodes = True
        
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        bsdf =  material.node_tree.nodes["Principled BSDF"]
        output = material.node_tree.nodes["Material Output"]

        if "teaSA_color" in state.userParameter:
            bsdf.inputs['Base Color'].default_value = (state.userParameter["teaSA_color"][0], state.userParameter["teaSA_color"][1], state.userParameter["teaSA_color"][2], 1)

        if bpy.app.version < (4, 0, 0):
            bsdf.inputs['Specular'].default_value = state.specular
        else:
            bsdf.inputs['Specular IOR Level'].default_value = state.specular
        
        if bpy.app.version >= (2, 92, 0):
            bsdf.inputs['Emission Strength'].default_value = state.emission

        if state.texture != []:
            
            for texture in state.texture:

                get_image(sSceneDatabase, textureDir, texture, state, nodes, links, bsdf, output)

    elif material:

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        node = nodes.get("Image Texture", None)
        
        if node is None and state.texture != []:
            
            bsdf =  material.node_tree.nodes["Principled BSDF"]
            output = material.node_tree.nodes["Material Output"]

            for texture in state.texture:

                get_image(sSceneDatabase, textureDir, texture, state, nodes, links, bsdf, output)

    if state.fillType == 0:
        material.blend_method = 'OPAQUE'
    elif state.fillType == 1:
        material.blend_method = 'CLIP'
    elif state.fillType == 2:
        material.blend_method = 'BLEND'
    else:
        material.blend_method = 'OPAQUE'

    return material

# Textures

def get_image(sSceneDatabase, textureDir, texture, state, nodes, links, bsdf, output):
        
        sTexture = sSceneDatabase.texture[texture]

        texture_filepath = f"{textureDir}{sTexture.fileName}"

        if os.path.isfile(texture_filepath):

            texture_file = image_utils.load_image(texture_filepath, check_existing=True)

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
                
                if bpy.app.version < (4, 0, 0):
                    links.new(bsdf.inputs['Specular'], specularTextureImage_node.outputs['Color'])
                else:
                    links.new(bsdf.inputs['Specular IOR Level'], specularTextureImage_node.outputs['Color'])

            elif sTexture.textureType == 6: # ???

                pass

            else:
                
                print(sTexture.textureType)
                pass

def extract_textures(efo, textureDir):

    for textureImageSignature, textureImage in efo._sSceneDatabase.textureImage.items():
        if textureImageSignature > 0 and textureImage.fileName != None and not os.path.isfile(textureDir + textureImage.fileName):
            if not os.path.exists(textureDir):
                os.mkdir(textureDir)
            f = open(textureDir + textureImage.fileName, "wb")
            f.write(textureImage.file)
            f.close()

#

def import_efo(filepath, files, clearScene, importTextures):
    
    if clearScene == True:
        clear_scene()

    folder = (os.path.dirname(filepath))

    for i, j in enumerate(files):

        path_to_file = (os.path.join(folder, j.name))

        efo = EFO(path_to_file)
        efoName = path_to_file.split("\\")[-1]

        head = os.path.split(path_to_file)[0]

        if importTextures:

            texture = head + "\\" + "texture.efo"
            if os.path.exists(texture):

                texture_efo = EFO(texture)
                texture_dir = path_to_file.replace(efoName, "textures\\")
                extract_textures(texture_efo, texture_dir)
                extract_textures(efo, texture_dir)

            else:
                
                texture_dir = head + "\\" + efoName[:-4] + "_" + "textures\\"
                extract_textures(efo, texture_dir)
        
        else :

            texture_dir = ""

        build_hierarchy(efo, texture_dir, os.path.splitext(efoName)[0])

    return {'FINISHED'}