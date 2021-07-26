import bpy
import struct
import bmesh

from math import *
from mathutils import *
from .efo import *
from .utils import *
from .blender_functions import *
from io import BytesIO

def buildModel(efo, import_character):
    count = 0
    for shape in efo.efo_header.shapeDictionary.values():
        mesh = bpy.data.meshes.new(shape.geomName)
        obj = bpy.data.objects.new(shape.geomName, mesh)
        obj.rotation_euler = ( radians(90), 0, 0 )

        if bpy.app.version >= (2, 80, 0):
            bpy.context.scene.collection.objects.link(obj)
        else:
            bpy.context.scene.objects.link(obj)

        # Set vertex attributes
        vertices = []
        normals = []
        texCoordsLayer1 = []
        texCoordsLayer2 = []
        colors = []

        vertexBuffer = BinaryReader(BytesIO(shape.buffer.buffer[(shape.startNumber * shape.buffer.strideSize):]))

        #print(shape.geomName)
        #print(shape.buffer.strideSize)

        for i in range(shape.vertexNumber):

            if shape.buffer.strideSize == 12:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

            elif shape.buffer.strideSize == 16:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                r, g, b, a = vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255
                colors.append([r, g, b, a])

            elif shape.buffer.strideSize == 20:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

            elif shape.buffer.strideSize == 24:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                r, g, b, a = vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255
                colors.append([r, g, b, a])

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

                # n1, n2, n3 = vertexBuffer.readFloat(),vertexBuffer.readFloat(),vertexBuffer.readFloat()
                # normals.append([n1,n2,n3])

            elif shape.buffer.strideSize == 28:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                r, g, b, a = vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255
                colors.append([r, g, b, a])

            elif shape.buffer.strideSize == 32:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

            elif shape.buffer.strideSize == 36:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                r, g, b, a = vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255
                colors.append([r, g, b, a])

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

            elif shape.buffer.strideSize == 40:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                vertexBuffer.seek(8, 1)

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

                # vertexBuffer.seek(8,1)

            elif shape.buffer.strideSize == 44:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                r, g, b, a = vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255
                colors.append([r, g, b, a])

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer2.append([u, v])

            elif shape.buffer.strideSize == 48:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                vertexBuffer.seek(24, 1)

            elif shape.buffer.strideSize == 52:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                vertexBuffer.seek(16, 1)

                r, g, b, a = vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255, vertexBuffer.readUByte() / 255
                colors.append([r, g, b, a])

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

            elif shape.buffer.strideSize == 56:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                vertexBuffer.seek(32, 1)

            elif shape.buffer.strideSize == 60:
                x, y, z = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                vertices.append([x, y, z])

                n1, n2, n3 = vertexBuffer.readFloat(), vertexBuffer.readFloat(), vertexBuffer.readFloat()
                normals.append(Vector((n1,n2,n3)).normalized())

                vertexBuffer.seek(28, 1)

                u, v = vertexBuffer.readFloat(), vertexBuffer.readFloat()
                texCoordsLayer1.append([u, v])

                # vertexBuffer.seek(36,1)

        # Set Faces
        indices = []
        faceBuffer = BinaryReader(BytesIO(efo.efo_header.faceBuffer[(shape.indexStart * 2):]))
        for i in range(shape.indexNumber):
            indices.append(faceBuffer.readUShort())

        faces = StripToTriangle(indices, shape.indexNumber)

        bm = bmesh.new()
        bm.from_mesh(mesh)

        vertexList = {}
        facesList = []

        if texCoordsLayer1 != []:
            uv_layer1 = bm.loops.layers.uv.new()
        if texCoordsLayer2 != []:
            uv_layer2 = bm.loops.layers.uv.new()

        material = bpy.data.materials.get(shape.shader.materialName)
        if not material:
            material = bpy.data.materials.new(shape.shader.materialName)

        # Set vertices
        for j in range(len(vertices)):
            vertex = bm.verts.new(vertices[j])
            if normals != []:
                vertex.normal = normals[j]
            vertex.index = shape.startNumber + j

            vertexList[shape.startNumber + j] = vertex

        # Set faces
        for j in range(0, len(faces)):
            try:
                face = bm.faces.new([vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]])
                face.smooth = True
                facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
            except:
                """
                for Face in facesList:
                    if {vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]} == set(Face[1]):
                        face = Face[0].copy(verts=False, edges=False)
                        face.smooth = True
                        facesList.append([face, [vertexList[faces[j][0]], vertexList[faces[j][1]], vertexList[faces[j][2]]]])
                        break
                """""
                pass
                #print(shape.geomName)

        # Set uv
        for f in bm.faces:
            if texCoordsLayer1 != []:
                for l in f.loops:
                    l[uv_layer1].uv = [texCoordsLayer1[l.vert.index - shape.startNumber][0], 1 - texCoordsLayer1[l.vert.index - shape.startNumber][1]]
            if texCoordsLayer2 != []:
                for l in f.loops:
                    l[uv_layer2].uv = [texCoordsLayer2[l.vert.index - shape.startNumber][0], 1 - texCoordsLayer2[l.vert.index - shape.startNumber][1]]

        # Set colors
        if colors != []:
            color_layer = bm.loops.layers.color.new("Color")
            for f in bm.faces:
                for l in f.loops:
                    l[color_layer] = colors[l.vert.index - shape.startNumber]

        bm.to_mesh(mesh)
        bm.free()

        mesh.materials.append(material)

        # Set normals
        mesh.use_auto_smooth = True

        if normals != []:
            mesh.normals_split_custom_set_from_vertices(normals)

        count += 1
        #print(str(count) + " of : " + str(len(efo.efo_header.shapeDictionary)))

            
def main(filepath, clear_scene, import_character):
    if clear_scene == True:
        clearScene()
    efo = EFO(filepath)
    buildModel(efo, import_character)
    return {'FINISHED'}

if __name__ == '__main__':
    main()
