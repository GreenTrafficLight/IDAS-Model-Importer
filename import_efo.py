import bpy
import struct
import bmesh

from math import *
from mathutils import *
from .efo import *
from .utils import *
from .blender_functions import *
from io import BytesIO

def build(efo):
    for shapeHeaderSignature in efo._sSceneDatabase.shapeHeader.keys():

        shapeHeader = efo._sSceneDatabase.shapeHeader[shapeHeaderSignature]
        
        for shapeSignature in shapeHeader.shape:

            shape = efo._sSceneDatabase.shape[shapeSignature]
            displayList = efo._sSceneDatabase.displayList[shape.displayList]
            geometry = efo._sSceneDatabase.geometry[displayList.geometry]
            # if displayListRef == 0 (displayList with the index buffer)
            # displayListRef = index buffer
            state = efo._sSceneDatabase.state[shape.state]

            pass

            
def main(filepath, clear_scene, import_character):
    if clear_scene == True:
        clearScene()
    efo = EFO(filepath)
    #buildModel(efo, import_character)
    build(efo)
    return {'FINISHED'}

if __name__ == '__main__':
    main()
