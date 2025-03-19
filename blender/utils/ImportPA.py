import bpy
import struct
import bmesh
import numpy as np
import os

from math import *
from mathutils import *
from bpy_extras import image_utils
from collections import *

from ...formats import *
from ...utilities import *

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
