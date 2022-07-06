import bpy
import struct
import bmesh
import numpy as np
import os

from math import *
from mathutils import *
from bpy_extras import image_utils
from collections import *

from .efo import *
from .pa8 import *
from .Utilities import *
from .Blender import *

# Meshes

def build_hierarchy(efo, texture_dir, filename):


    bpy.ops.object.add(type="ARMATURE")
    file = bpy.context.object
    file.rotation_euler = ( radians(90), 0, 0 )
    file.name = filename

    for skeletonSignature in efo._sSceneDatabase.skeleton.keys():

        skeleton = efo._sSceneDatabase.skeleton[skeletonSignature]

        bpy.ops.object.add(type="ARMATURE")
        ob = bpy.context.object
        ob.name = skeleton.name
        ob.parent = file

        amt = ob.data
        amt.name = skeleton.name

        bone_mapping = []
        
        for boneSignature in skeleton.bone:

            sBone = efo._sSceneDatabase.bone[boneSignature]
            bone_mapping.append(sBone.name)

            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bone = amt.edit_bones.new(sBone.name)

            bone.tail = (0.01 , 0.01, 0.01)
            
            quad = Quaternion((sBone.quaternion[3], sBone.quaternion[0], sBone.quaternion[1], sBone.quaternion[2]))
            mat = quad.to_matrix().to_4x4()
            mat = Matrix.Translation(sBone.translation) @ mat
            bone.matrix = mat

            if sBone.parentIndex != -1:

                parent = efo._sSceneDatabase.bone[sBone.parent]

                bone.parent = amt.edit_bones[parent.name]
                bone.matrix = amt.edit_bones[parent.name].matrix @ bone.matrix

                bone.head = bone.matrix.translation

        bones = amt.edit_bones
        for boneSignature in skeleton.bone:

            sBone = efo._sSceneDatabase.bone[boneSignature]

            if len(sBone.name) > 63: # Thanks Blender :)
                bone = bones[sBone.name[:63]]
            else:
                bone = bones[sBone.name]

            if sBone.parentIndex != -1:

                parent = efo._sSceneDatabase.bone[sBone.parent]
                
                bone.tail = bones[parent.name].head

        bpy.ops.object.mode_set(mode='OBJECT')
  
        empty_list = []

        for boneSignature in skeleton.bone:

            dummy = efo._sSceneDatabase.bone[boneSignature]

            if bpy.app.version >= (2, 90, 0):
                bpy.ops.object.empty_add(type='PLAIN_AXES', location=dummy.translation, scale=dummy.scale)
            else:
                bpy.ops.object.empty_add(type='PLAIN_AXES', location=dummy.translation)

            empty = bpy.context.active_object
            empty.empty_display_size = 0.05
            empty.name = dummy.name

            empty.matrix_local = dummy.mtxLocal
            
            if dummy.rotation != 0:
                empty.rotation_euler = dummy.rotation

            if dummy.parentIndex == -1:
                empty.parent = ob
                
            if dummy.parentName != "":
                
                empty.parent = empty_list[dummy.parentIndex]

            if dummy.shapeHeader != 0:
                
                shapeHeader = efo._sSceneDatabase.shapeHeader[dummy.shapeHeader]

                for shapeSignature in shapeHeader.shape:

                    shape = efo._sSceneDatabase.shape[shapeSignature]

                    build_mesh(efo._sSceneDatabase, shape,  empty, texture_dir, bone_mapping, ob)

            empty_list.append(empty)

def build_mesh(sSceneDatabase, shape, shapeHeader, texture_dir, bone_mapping, armature):

    mesh = bpy.data.meshes.new(shape.name)
    obj = bpy.data.objects.new(shape.name, mesh)

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
                vg_name = bone_mapping[vg + 1]
                if not vg_name in obj.vertex_groups:
                    group = obj.vertex_groups.new(name=vg_name)
                else:
                    group = obj.vertex_groups[vg_name]
                weight = vertexArray.array.array["boneWeights"][i + primitiveList.startNumber][k]
                if weight > 0.0:
                    group.add([i], weight, 'REPLACE')

    # Set normals
    mesh.use_auto_smooth = True

    if normals != []:
        mesh.normals_split_custom_set_from_vertices(normals)

    material = get_materials(sSceneDatabase, shape, texture_dir)

    mesh.materials.append(material)

    for blendGeometry in displayList.blendGeometry.values():

        mesh = bpy.data.meshes.new(blendGeometry.name)
        obj = bpy.data.objects.new(blendGeometry.name, mesh)

        shapeHeader.users_collection[0].objects.link(obj)

        modifier = obj.modifiers.new(armature.name, type="ARMATURE")
        modifier.object = bpy.data.objects[armature.name]

        obj.parent = shapeHeader

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

def get_materials(sSceneDatabase, shape, texture_dir):

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

        bsdf.inputs['Specular'].default_value = state.specular
        if bpy.app.version >= (2, 92, 0):
            bsdf.inputs['Emission Strength'].default_value = state.emission

        if state.texture != []:
            
            for texture in state.texture:

                get_image(sSceneDatabase, texture_dir, texture, state, nodes, links, bsdf, output)

    elif material:

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        node = nodes.get("Image Texture", None)
        
        if node is None and state.texture != []:
            
            bsdf =  material.node_tree.nodes["Principled BSDF"]
            output = material.node_tree.nodes["Material Output"]

            for texture in state.texture:

                get_image(sSceneDatabase, texture_dir, texture, state, nodes, links, bsdf, output)

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

def get_image(sSceneDatabase, texture_dir, texture, state, nodes, links, bsdf, output):
        
        sTexture = sSceneDatabase.texture[texture]

        texture_filepath = f"{texture_dir}{sTexture.fileName}"

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
                
                links.new(bsdf.inputs['Specular'], specularTextureImage_node.outputs['Color'])

            elif sTexture.textureType == 6: # ???

                pass

            else:
                
                print(sTexture.textureType)
                pass

def extract_textures(efo, texture_dir):

    for textureImageSignature, textureImage in efo._sSceneDatabase.textureImage.items():
        if textureImageSignature > 0 and textureImage.fileName != None and not os.path.isfile(texture_dir + textureImage.fileName):
            if not os.path.exists(texture_dir):
                os.mkdir(texture_dir)
            f = open(texture_dir + textureImage.fileName, "wb")
            f.write(textureImage.file)
            f.close()

# Paths

def import_trees_path(pa, tree_path_name, tree_meshes, import_trees):

    path = add_empty(tree_path_name, empty_rotation=(radians(90), 0, 0))

    C = bpy.context

    lod_chosen = ["a", "b", "c"]

    if import_trees == "OPT_B":

        a_lod_empty = add_empty("a", path)
        lod_chosen = "a"

    if import_trees == "OPT_C":

        b_lod_empty = add_empty("b", path)
        lod_chosen = "b"

    if import_trees == "OPT_D":

        c_lod_empty = add_empty("c", path)
        lod_chosen = "c"

    for i in range(len(pa.list)): #len(pa.list)

        name = format(int(pa.list[i][0]), "02")

        src_obj = {lod:meshs for (lod, meshs) in tree_meshes.items() if name in lod[:3]}

        for lod, meshs in src_obj.items():

            if lod_chosen in lod[:3]:
                
                for mesh in meshs :

                    new_obj = mesh.copy()
                    new_obj.matrix_local = Matrix.Translation(pa.list[i][1]) @ pa.list[i][2] @ Matrix.Scale(pa.list[i][3], 4)
                    new_obj.name = tree_path_name + "_" + str(i)

                    bpy.context.view_layer.update()

                    if "a" in lod[:3]:
                        new_obj.parent = a_lod_empty
                    elif "b" in lod[:3]:
                        new_obj.parent = b_lod_empty
                    elif "c" in lod[:3]:
                        new_obj.parent = c_lod_empty

                    C.collection.objects.link(new_obj)

def import_gallery_path(pa, gallery_path_name, gallery_meshes):

    path = add_empty(gallery_path_name, empty_rotation=(radians(90), 0, 0))

    C = bpy.context

    for i in range(len(pa.list)): #len(pa.list)

        name = format(int(pa.list[i][0]), "02")

        src_obj = {lod:meshs for (lod, meshs) in gallery_meshes.items() if name in lod[:3]}
                
        for lod, meshs in src_obj.items():

            for mesh in meshs :

                new_obj = mesh.copy()
                new_obj.matrix_local = Matrix.Translation(pa.list[i][1]) @ pa.list[i][2] @ Matrix.Scale(pa.list[i][3], 4)
                new_obj.name = gallery_path_name + "_" + str(i)

                bpy.context.view_layer.update()
                
                new_obj.parent = path
                
                C.collection.objects.link(new_obj)

def get_meshes_for_path(fileName):

    lods = defaultdict(list)

    objects = bpy.context.scene.objects[fileName]

    def recurse(ob, parent, depth):
        if not ob.children:
            lods[ob.parent.name].append(ob)
            return
        
        for child in ob.children:
            recurse(child, ob,  depth + 1)

    recurse(objects, objects.parent, 0)

    return lods

#

def main(filepath, clear_scene, import_textures, import_trees, import_gallery):
    if clear_scene == True:
        clearScene()
    efo = EFO(filepath)
    efoName = filepath.split("\\")[-1]

    head = os.path.split(filepath)[0]

    if import_textures:

        texture = head + "\\" + "texture.efo"
        if os.path.exists(texture):

            texture_efo = EFO(texture)
            texture_dir = filepath.replace(efoName, "textures\\")
            extract_textures(texture_efo, texture_dir)
            extract_textures(efo, texture_dir)

        else:
            
            texture_dir = head + "\\" + efoName[:-4] + "_" + "textures\\"
            extract_textures(efo, texture_dir)
    
    else :

        texture_dir = ""

    build_hierarchy(efo, texture_dir, os.path.splitext(efoName)[0])

    if import_trees != 'OPT_A' :

        path_dir = os.path.dirname(os.path.dirname(filepath)) + "\\" + "path" + "\\"
        
        if os.path.isdir(path_dir):

            paths_tree = []
        
            # Get Path

            for filename_dir in os.listdir(path_dir):
                if os.path.splitext(filename_dir)[1] == ".pa8" and "_path_tree" in filename_dir:
                    paths_tree.append(filename_dir)

            for file in paths_tree:
                if file.split("_")[-1] != "l.pa8" and file.split("_")[-1] != "r.pa8" and file.split("_")[-1] != "cull.pa8" and file.split("_")[-1] != "test.pa8":
                    path_tree = file

            # Get efo

            for filename_dir in os.listdir(head):
                if os.path.splitext(filename_dir)[1] == ".efo" and '_'.join(efoName.split("_")[0:3]) + "_tree" in filename_dir and filename_dir.split("_")[-1] != "test.efo" and filename_dir.split("_")[-1] != "n.efo":
                    treePath = head + "\\" + filename_dir

            treeName = treePath.split("\\")[-1]
            
            if efoName != treeName :
                
                tree = EFO(treePath)

                treeNameHead = os.path.split(filepath)[0]
                common_texture_dir = treeNameHead + "\\" + treeName[:-4] + "_" + "textures\\"
                extract_textures(tree, common_texture_dir)

                build_hierarchy(tree, common_texture_dir, os.path.splitext(treeName)[0])

            tree_meshes = get_meshes_for_path(os.path.splitext(treeName)[0])
            
            pa = PA(path_dir + path_tree)
            import_trees_path(pa, os.path.splitext(path_tree)[0], tree_meshes, import_trees)

            # delete tree meshes
            delete_hierarchy(os.path.splitext(treeName)[0])

    if import_gallery != 'OPT_A':

        path_dir = os.path.dirname(os.path.dirname(filepath)) + "\\" + "path" + "\\"

        if os.path.isdir(path_dir):

            common_dir = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))  + "\\" + "common" + "\\"

            for filename_dir in os.listdir(path_dir):
                if os.path.splitext(filename_dir)[1] == ".pa8" and "_path_gallery" in filename_dir:
                    path_gallery = filename_dir

            # Dry (Summer)

            if import_gallery == "OPT_B": 

                if "day" in efoName :
                    
                    galleryPath = common_dir + "cmn_gal_sum_day_dry_ny.efo"

                elif "ngt" in efoName :

                    galleryPath = common_dir + "cmn_gal_sum_ngt_dry_ny.efo"

            # Rain (Summer)

            elif import_gallery == "OPT_C": 

                if "day" in efoName :

                    galleryPath = common_dir + "cmn_gal_sum_day_ran_ny.efo"

                elif "ngt" in efoName :

                    galleryPath = common_dir + "cmn_gal_sum_ngt_ran_ny.efo"

            # Dry (Winter)

            elif import_gallery == "OPT_D": 

                if "day" in efoName :

                    galleryPath = common_dir + "cmn_gal_win_day_dry_ny.efo"

                elif "ngt" in efoName :

                    galleryPath = common_dir + "cmn_gal_win_ngt_dry_ny.efo"

            # Rain (Winter)

            elif import_gallery == "OPT_E": 

                if "day" in efoName :

                    galleryPath = common_dir + "cmn_gal_win_day_ran_ny.efo"

                elif "ngt" in efoName :

                    galleryPath = common_dir + "cmn_gal_win_ngt_ran_ny.efo"

            # Dry (Snow)

            elif import_gallery == "OPT_F": 

                if "day" in efoName :

                    galleryPath = common_dir + "cmn_gal_snw_day_dry_kk.efo"

                elif "ngt" in efoName :

                    galleryPath = common_dir + "cmn_gal_snw_ngt_dry_kk.efo"

            # Rain (Snow)

            elif import_gallery == "OPT_G": 

                if "day" in efoName :

                    galleryPath = common_dir + "cmn_gal_snw_day_ran_kk.efo"

                elif "ngt" in efoName :
                    
                    galleryPath = common_dir + "cmn_gal_snw_ngt_ran_kk.efo"
                    
            gallery = EFO(galleryPath)
            galleryName = galleryPath.split("\\")[-1]

            galleryNameHead = os.path.split(filepath)[0]
            common_texture_dir = galleryNameHead + "\\" + galleryName[:-4] + "_" + "textures\\"
            extract_textures(gallery, common_texture_dir)

            build_hierarchy(gallery, common_texture_dir, os.path.splitext(galleryName)[0])

            gallery_meshes = get_meshes_for_path(os.path.splitext(galleryName)[0])

            pa = PA(path_dir + path_gallery)
            import_gallery_path(pa, os.path.splitext(path_gallery)[0], gallery_meshes)

            # delete gallery meshes
            delete_hierarchy(os.path.splitext(galleryName)[0])


    return {'FINISHED'}


if __name__ == '__main__':
    main()
