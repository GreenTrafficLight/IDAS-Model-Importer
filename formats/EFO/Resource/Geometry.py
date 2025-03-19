from ....utilities import *

from .DisplayList import sDisplayList

class sGeometry(sDisplayList):

    def __init__(self, bs: BinaryReader, sSceneDatabase):
        self.bs = bs

        self.name = ""
        self.infoName = ""

        self.vertexArrayDic = {}

        self.vertexDesc = 0
        self.vertexNumber = 0
        self.vertexSize = 0
        self.strideSize = 0
        self.vertexArray = 0
        self.userVertexArray = 0
        self.userVertexArrayElementNumber = 0
        self.flag = 0

        self.load(sSceneDatabase)

    def load(self, sSceneDatabase):
        self.bs.readUShort()
        self.bs.readUInt() # size of sGeometry data

        self.readProperties(sSceneDatabase)

        self.bs.readUInt()
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        self.bs.readUInt()
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

        #self.vertexArrayDic[self.vertexArray] = sSceneDatabase.sShapeHeader.sShape.sDisplayList.sGeometry.sVertexArray(self.bs)

    def readProperties(self, sSceneDatabase):
        self.vertexDesc = self.bs.readUInt()
        self.vertexNumber = self.bs.readUInt()
        self.vertexSize = self.bs.readUInt()
        self.strideSize = self.bs.readUInt()
        self.vertexArray = self.bs.readUShort()

        if "userVertexArray" in sSceneDatabase._sSerial["_sSerial::_sGeometry"]:
            self.userVertexArray = self.bs.readUShort()

        if "userVertexArrayElementNumber" in sSceneDatabase._sSerial["_sSerial::_sGeometry"]:
            self.userVertexArrayElementNumber = self.bs.readUInt()
        
        if "flag" in sSceneDatabase._sSerial["_sSerial::_sGeometry"]:
            self.flag = self.bs.readByte()


    class sVertexArray:

        def __init__(self, bs: BinaryReader, sGeometry: 'sGeometry'):
            self.bs = bs
            self.sGeometry = sGeometry

            self.array = None

            self.load()

        def load(self):
            self.bs.readUShort()
            self.bs.readUInt() # size of sVertexArray data

            self.bs.readUInt()

            if self.sGeometry.vertexDesc == 1:
                self.array = sGeometry.sVertexArray.sVertexArrayP()
            
            elif self.sGeometry.vertexDesc == 3:
                self.array = sGeometry.sVertexArray.sVertexArrayPN()

            elif self.sGeometry.vertexDesc == 9: 
                self.array = sGeometry.sVertexArray.sVertexArrayPC()
            
            elif self.sGeometry.vertexDesc == 11:
                self.array = sGeometry.sVertexArray.sVertexArrayPNC()

            elif self.sGeometry.vertexDesc == 33:
                self.array = sGeometry.sVertexArray.sVertexArrayPT()

            elif self.sGeometry.vertexDesc == 35: 
                self.array = sGeometry.sVertexArray.sVertexArrayPNT()

            elif self.sGeometry.vertexDesc == 41:
                self.array = sGeometry.sVertexArray.sVertexArrayPCT()
                            
            elif self.sGeometry.vertexDesc == 43:
                self.array = sGeometry.sVertexArray.sVertexArrayPNCT()

            elif self.sGeometry.vertexDesc == 47:
                self.array = sGeometry.sVertexArray.sVertexArrayPBCT()
                
            elif self.sGeometry.vertexDesc == 107:
                self.array = sGeometry.sVertexArray.sVertexArrayPNCT2()

            elif self.sGeometry.vertexDesc == 111:
                self.array = sGeometry.sVertexArray.sVertexArrayPBCT2()

            elif self.sGeometry.vertexDesc == 1539:
                self.array = sGeometry.sVertexArray.sVertexArrayPNW2()

            elif self.sGeometry.vertexDesc == 1571:
                self.array = sGeometry.sVertexArray.sVertexArrayPNTW2()

            elif self.sGeometry.vertexDesc == 7715:
                self.array = sGeometry.sVertexArray.sVertexArrayPNTW4()

            elif self.sGeometry.vertexDesc == 8193:
                self.array = sGeometry.sVertexArray.sVertexArrayPn()

            if self.array is None:
                raise TypeError("Unknown vertexDesc: " + str(self.sGeometry.vertexDesc))

            self.array.read(self.bs)

            #self.sGeometry.vertexArrayDic[self.sGeometry.vertexArray] = self.array

        # P = Postions
        # N = Normals
        # n = ?
        # C = Colors
        # T = UV Coordinates
        # W = Bone indices and weights
        # B = Bitangents

        class sVertexArrayP:
            def __init__(self):
                self.array = {"positions" : []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for i in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])

        class sVertexArrayPN:
            def __init__(self):
                self.array = {"positions" : [], "normals": []}

            def read(self, br):

                count = br.readUInt()

                for i in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])

        class sVertexArrayPn:
            def __init__(self):
                self.array = {"positions" : [], "unknown": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for i in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["unknown"].append([br.readFloat(), br.readFloat()])

        class sVertexArrayPC:
            def __init__(self):
                self.array = {"positions" : [], "colors": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for i in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

        class sVertexArrayPT:
            def __init__(self):
                self.array = {"positions" : [], "texCoordsLayer1": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for i in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()])

        class sVertexArrayPNC:
            def __init__(self):
                self.array = {"positions" : [], "normals": [], "colors": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for i in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])

        class sVertexArrayPCT:
            def __init__(self):
                self.array = {"positions" : [], "colors": [], "texCoordsLayer1": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()])

        class sVertexArrayPNT:
            def __init__(self):
                self.array = {"positions" : [], "normals": [], "texCoordsLayer1": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()])

        class sVertexArrayPNCT:
            def __init__(self):
                self.array = {"positions" : [], "normals": [], "colors": [], "texCoordsLayer1": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()])                        

        class sVertexArrayPNW2:
            def __init__(self):
                self.array = {"positions" : [], "normals": [], "boneIndices": [], "boneWeights":[]}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["boneWeights"].append([br.readUByte() / 255])
                    self.array["boneIndices"].append([br.readUByte()])
                    self.array["boneWeights"][vertex].insert(0, br.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(br.readUByte())

        class sVertexArrayPBCT: # TO DO
            def __init__(self):
                self.array = {"positions" : [], "bitangents": [], "colors": [], "texCoordsLayer1": []}
            
            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    
                    """
                    normal = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent_sign = bs.readFloat()
                    bitangents = (Vector.cross(tangent, bitangent) * tangent_sign)
                    self.array["bitangents"].append([normals[0], normals[1], normals[2]])
                    """

                    self.array["bitangents"].append([br.readBytes(28)])
                    self.array["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()])  

        class sVertexArrayPNCT2:
            def __init__(self):
                self.array = {"positions" : [], "normals": [], "colors": [], "texCoordsLayer1": [], "texCoordsLayer2": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()])   
                    self.array["texCoordsLayer2"].append([br.readFloat(), br.readFloat()])    

        class sVertexArrayPBCT2: # TO DO
            def __init__(self):
                self.array = {"positions" : [], "bitangents": [], "colors": [], "texCoordsLayer1": [], "texCoordsLayer2": []}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    
                    """
                    normal = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent_sign = bs.readFloat()
                    bitangents = (Vector.cross(tangent, bitangent) * tangent_sign)
                    self.array["bitangents"].append([normals[0], normals[1], normals[2]])
                    """
                    
                    self.array["bitangents"].append([br.readBytes(28)])
                    self.array["colors"].append([br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255, br.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()])   
                    self.array["texCoordsLayer2"].append([br.readFloat(), br.readFloat()])    

        class sVertexArrayPNTW2:
            def __init__(self):
                self.array = {"positions" : [], "normals": [], "texCoordsLayer1": [], "boneIndices": [], "boneWeights":[]}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):

                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()]) 
                    self.array["boneWeights"].append([br.readUByte() / 255])
                    self.array["boneIndices"].append([br.readUByte()])
                    self.array["boneWeights"][vertex].insert(0, br.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(br.readUByte())

        # TO DO
        class sVertexArrayPNTW4:
            def __init__(self):
                self.array = {"positions" : [], "normals": [], "texCoordsLayer1": [], "boneIndices": [], "boneWeights":[]}

            def read(self, br: BinaryReader):

                count = br.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["normals"].append([br.readFloat(), br.readFloat(), br.readFloat()])
                    self.array["texCoordsLayer1"].append([br.readFloat(), br.readFloat()]) 
                    self.array["boneWeights"].append([br.readUByte() / 255])
                    self.array["boneIndices"].append([br.readUByte()])
                    self.array["boneWeights"][vertex].insert(0, br.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(br.readUByte())
                    self.array["boneWeights"][vertex].insert(3, br.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(br.readUByte())
                    self.array["boneWeights"][vertex].insert(2, br.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(br.readUByte())