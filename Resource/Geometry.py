from ..Utilities import *

from .DisplayList import sDisplayList

class sGeometry(sDisplayList):

    def __init__(self, bs, sSceneDatabase):
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

        def __init__(self, bs, sGeometry):
            self.bs = bs
            self.sGeometry = sGeometry

            self.array = 0

            self.load()

        def load(self):
            self.bs.readUShort()
            self.bs.readUInt() # size of sVertexArray data

            self.bs.readUInt()

            if self.sGeometry.vertexDesc == 1:
                self.array = sGeometry.sVertexArray.sVertexArrayP(self.bs)
            
            elif self.sGeometry.vertexDesc == 3:
                self.array = sGeometry.sVertexArray.sVertexArrayPN(self.bs)

            elif self.sGeometry.vertexDesc == 9: 
                self.array = sGeometry.sVertexArray.sVertexArrayPC(self.bs)
            
            elif self.sGeometry.vertexDesc == 11:
                self.array = sGeometry.sVertexArray.sVertexArrayPNC(self.bs)

            elif self.sGeometry.vertexDesc == 33:
                self.array = sGeometry.sVertexArray.sVertexArrayPT(self.bs)

            elif self.sGeometry.vertexDesc == 35: 
                self.array = sGeometry.sVertexArray.sVertexArrayPNT(self.bs)

            elif self.sGeometry.vertexDesc == 41:
                self.array = sGeometry.sVertexArray.sVertexArrayPCT(self.bs)
                            
            elif self.sGeometry.vertexDesc == 43:
                self.array = sGeometry.sVertexArray.sVertexArrayPNCT(self.bs)

            elif self.sGeometry.vertexDesc == 47:
                self.array = sGeometry.sVertexArray.sVertexArrayPBCT(self.bs)
                

            elif self.sGeometry.vertexDesc == 107:
                self.array = sGeometry.sVertexArray.sVertexArrayPNCT2(self.bs)

            elif self.sGeometry.vertexDesc == 111:
                self.array = sGeometry.sVertexArray.sVertexArrayPBCT2(self.bs)

            elif self.sGeometry.vertexDesc == 1539:
                self.array = sGeometry.sVertexArray.sVertexArrayPNW2(self.bs)

            elif self.sGeometry.vertexDesc == 1571:
                self.array = sGeometry.sVertexArray.sVertexArrayPNTW2(self.bs)

            elif self.sGeometry.vertexDesc == 7715:
                self.array = sGeometry.sVertexArray.sVertexArrayPNTW4(self.bs)

            elif self.sGeometry.vertexDesc == 8193:
                self.array = sGeometry.sVertexArray.sVertexArrayPn(self.bs)

            #self.sGeometry.vertexArrayDic[self.sGeometry.vertexArray] = self.array


        class sVertexArrayP:
            def __init__(self, bs):
                self.array = {"positions" : []}

                count = bs.readUInt()

                for i in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])


        class sVertexArrayPN:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": []}

                count = bs.readUInt()

                for i in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])


        class sVertexArrayPn:
            def __init__(self, bs):
                self.array = {"positions" : [], "unknown": []}

                count = bs.readUInt()

                for i in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["unknown"].append([bs.readFloat(), bs.readFloat()])


        class sVertexArrayPC:
            def __init__(self, bs):
                self.array = {"positions" : [], "colors": []}

                count = bs.readUInt()

                for i in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["colors"].append([bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255])


        class sVertexArrayPT:
            def __init__(self, bs):
                self.array = {"positions" : [], "texCoordsLayer1": []}

                count = bs.readUInt()

                for i in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()])


        class sVertexArrayPNC:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": [], "colors": []}

                count = bs.readUInt()

                for i in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["colors"].append([bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255])


        class sVertexArrayPCT:
            def __init__(self, bs):
                self.array = {"positions" : [], "colors": [], "texCoordsLayer1": []}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["colors"].append([bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()])


        class sVertexArrayPNT:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": [], "texCoordsLayer1": []}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()])


        class sVertexArrayPNCT:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": [], "colors": [], "texCoordsLayer1": []}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["colors"].append([bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()])                        


        class sVertexArrayPNW2:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": [], "boneIndices": [], "boneWeights":[]}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["boneWeights"].append([bs.readUByte() / 255])
                    self.array["boneIndices"].append([bs.readUByte()])
                    self.array["boneWeights"][vertex].insert(0, bs.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(bs.readUByte())


        class sVertexArrayPBCT: # TO DO
            def __init__(self, bs):
                self.array = {"positions" : [], "bitangents": [], "colors": [], "texCoordsLayer1": []}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    
                    """
                    normal = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent_sign = bs.readFloat()
                    bitangents = (Vector.cross(tangent, bitangent) * tangent_sign)
                    self.array["bitangents"].append([normals[0], normals[1], normals[2]])
                    """

                    self.array["bitangents"].append([bs.readBytes(28)])
                    self.array["colors"].append([bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()])  


        class sVertexArrayPNCT2:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": [], "colors": [], "texCoordsLayer1": [], "texCoordsLayer2": []}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["colors"].append([bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()])   
                    self.array["texCoordsLayer2"].append([bs.readFloat(), bs.readFloat()])    


        class sVertexArrayPBCT2: # TO DO
            def __init__(self, bs):
                self.array = {"positions" : [], "bitangents": [], "colors": [], "texCoordsLayer1": [], "texCoordsLayer2": []}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    
                    """
                    normal = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent = Vector((bs.readFloat(), bs.readFloat(), bs.readFloat()))
                    tangent_sign = bs.readFloat()
                    bitangents = (Vector.cross(tangent, bitangent) * tangent_sign)
                    self.array["bitangents"].append([normals[0], normals[1], normals[2]])
                    """
                    
                    self.array["bitangents"].append([bs.readBytes(28)])
                    self.array["colors"].append([bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255, bs.readUByte() / 255])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()])   
                    self.array["texCoordsLayer2"].append([bs.readFloat(), bs.readFloat()])    


        class sVertexArrayPNTW2:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": [], "texCoordsLayer1": [], "boneIndices": [], "boneWeights":[]}

                count = bs.readUInt()

                for vertex in range(count):

                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()]) 
                    self.array["boneWeights"].append([bs.readUByte() / 255])
                    self.array["boneIndices"].append([bs.readUByte()])
                    self.array["boneWeights"][vertex].insert(0, bs.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(bs.readUByte())

        # TO DO
        class sVertexArrayPNTW4:
            def __init__(self, bs):
                self.array = {"positions" : [], "normals": [], "texCoordsLayer1": [], "boneIndices": [], "boneWeights":[]}

                count = bs.readUInt()

                for vertex in range(count):
                    self.array["positions"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["normals"].append([bs.readFloat(), bs.readFloat(), bs.readFloat()])
                    self.array["texCoordsLayer1"].append([bs.readFloat(), bs.readFloat()]) 
                    self.array["boneWeights"].append([bs.readUByte() / 255])
                    self.array["boneIndices"].append([bs.readUByte()])
                    self.array["boneWeights"][vertex].insert(0, bs.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(bs.readUByte())
                    self.array["boneWeights"][vertex].insert(3, bs.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(bs.readUByte())
                    self.array["boneWeights"][vertex].insert(2, bs.readUByte() / 255)
                    self.array["boneIndices"][vertex].append(bs.readUByte())