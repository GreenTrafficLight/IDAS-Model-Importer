from os import system
from .utils import *

class sSceneDatabase:
    def __init__(self, br):
        self.br = br
        
        self._sSerial = {}

        self.shapeHeader = {}
        self.state = {}
        self.geometry = {}
        self.displayList = {}
        self.texture = {}
        self.skeleton = {}
        self.textureImage = {}

        self.vertexArray = {}
        self.primitiveList = {}
        self.shape = {}

        self.shapeHeaderSignatures = []
        self.stateSignatures = []
        self.geometrySignatures = []
        self.displayListSignatures = []
        self.textureSignatures = []
        self.skeletonSignatures = []
        self.textureImageSignatures = []

        self.load()

    def load(self):
        magic = self.br.bytesToString(self.br.readBytes(4))
        self.br.seek(4, 1)
        fileSize = self.br.readInt()
        self.br.seek(4, 1)
        unknown = self.br.readByte()
        if unknown == 6:
            self.br.seek(4, 1)
        else:
            self.br.seek(-1, 1)

        self.br.seek(1, 1)  # unknown byte
        self.br.seek(self.br.readUShort(), 1)  # _sSerial::_sSceneDatabase
        self.br.seek(1, 1)  # zero

        self.br.bytesToString(self.br.readBytes(self.br.readByte())) # modelName
        self.br.bytesToString(self.br.readBytes(self.br.readByte()))  # yabukita

        self.br.seek(4, 1)  # 0x3ED (unknown)

        self.br.bytesToString(self.br.readBytes(self.br.readByte()))  # _sSerial

        self.br.readBytes(4)  # unknown array of bytes 0x4
        self.br.seek(1, 1)  # zero

        self.br.bytesToString(self.br.readBytes(self.br.readByte()))  # yabukita::Object

        self.br.readInt()  # 0x1 (unknown)

        # Read _sSerial
        self.get_sSerial()

        if "_sSerial::_sShapeHeader" in self._sSerial:
            self.br.seek(1, 1)  # zero

            # Read textures path
            self.getTexturesPath()
        
        else:
            self.getTextures()

            self.br.seek(1, 1)  # zero

        self.br.seek(2, 1)  # unknown 0x2
        self.br.seek(2, 1)  # unknown 0x2

        self.br.readInt()  # size of essd

        self.br.bytesToString(self.br.readBytes(4))

        self.br.seek(4, 1)  # zeros

        self.br.readBytes(4)  # 0x4112904

        skip = self.br.readInt()

        if skip == 2:
            self.br.seek(skip, 1)
        elif skip == 3:
            self.br.seek(skip, 1)
        elif skip == 23:
            self.br.bytesToString(self.br.readBytes(self.br.readShort())).replace("\0", "")
        else:
            self.br.seek(-4, 1)

        self.br.readInt()  # unknown 0x1

        # Read Signatures
        self.getSignatures()

        # unknown 0x18
        self.br.readInt()
        self.br.readInt()
        self.br.readInt()
        self.br.readInt()
        self.br.readInt()
        self.br.readInt()

        self.br.readInt()  # size of texture names list (and infos ?)
        self.br.readInt()  # unknown
        self.br.readInt()  # size of texture names list
        textureNamesCount = self.br.readInt()

        for i in range(textureNamesCount):
            self.br.bytesToString(self.br.readBytes(self.br.readUInt()))

        if textureNamesCount != 0:
            self.br.readInt()  # size of textbl path
            self.br.readInt()  # count of textbl path ?
            self.br.bytesToString(self.br.readBytes(self.br.readUShort()))  # textbl path

        self.br.readInt()  # size of model name
        self.br.bytesToString(self.br.readBytes(self.br.readShort()))  # model name
        self.br.readInt()  # size of info model name
        self.br.bytesToString(self.br.readBytes(self.br.readShort()))  # info model name

    def get_sSerial(self): # Read the informations at the start
        while True:
            _sSerialName = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
            if "_sSerial::" in _sSerialName:
                self.br.seek(3, 1)  # zeros
                self._sSerial[_sSerialName] = {}
                while True:
                    name = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
                    if name == "":
                        break
                    self._sSerial[_sSerialName][name] = (self.br.readByte(), self.br.readByte())
                    self.br.seek(1, 1)  # zero
            else:
                break

    def getTexturesPath(self):
        while True:
            texturePath = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
            if texturePath == "":
                break

    def getTextures(self):
        while True:
            texture = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
            if texture == "":
                break

    def getSignatures(self):

        # shapeHeader signatures
        self.br.readUInt()  # size of shapeHeader signatures
        count = self.br.readUInt()  # shapeHeader signatures count
        for signature in range(count):
            self.shapeHeaderSignatures.append(self.br.readUShort())

        # state signatures
        self.br.readUInt()  # size of state signatures
        count = self.br.readUInt()  # state signatures count
        for signature in range(count):
            self.stateSignatures.append(self.br.readUShort())

        # geometry signatures
        self.br.readUInt()  # size of geometry signatures
        count = self.br.readUInt()  # geometry signatures count
        for signature in range(count):
            self.geometrySignatures.append(self.br.readUShort())

        # displayList signatures
        self.br.readUInt()  # size of displayList signatures
        count = self.br.readUInt()  # displayList signatures count
        for signature in range(count):
            self.displayListSignatures.append(self.br.readUShort())

        # texture signatures
        self.br.readUInt()  # size of texture signatures
        count = self.br.readUInt()  # texture signatures count
        for signature in range(count):
            self.textureSignatures.append(self.br.readUShort())

        # skeleton signatures
        self.br.readUInt()  # size of skeleton signatures
        count = self.br.readUInt()  # skeleton signatures count
        for signature in range(count):
            self.skeletonSignatures.append(self.br.readUShort())

        # textureImage signatures
        self.br.readUInt()  # size of textureImage signatures
        count = self.br.readUInt()  # textureImage signatures count
        for signature in range(count):
            self.textureImageSignatures.append(self.br.readUShort())


    class sShapeHeader:
        def __init__(self, bs):
            self.bs = bs

            self.sShapeHeaderName = ""
            self.sShapeHeaderInfoName = ""

            self.flag = 0
            
            self.shapeDic = {}
            self.shape = []

            self.BSphere = 0
            self.BBoxCenter = 0
            self.BBoxSize = 0

            self.sortGroup = 0

            self.stateNameList = []
            self.textureNameList = []

            self.load()

        def load(self):
            self.bs.readUShort()  # unknown 0x2
            self.bs.readUInt()  # size of shape
            
            self.flag = self.bs.readUInt()

            self.readShapeSignatures()
            self.readBoundingBox()

            self.sortGroup = self.bs.readShort()

            self.readStateNameList()
            self.readTextureNameList()

            self.bs.readUInt()
            self.sShapeHeaderName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
            self.bs.readUInt()
            self.sShapeHeaderInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

            print(self.bs.tell())

        def readShapeSignatures(self):
            self.bs.readUInt()  # size of shape signatures
            shapeCount = self.bs.readUInt()  # count of shape signatures
            for shape in range(shapeCount):
                self.shape.append(self.bs.readUShort())

        def readBoundingBox(self):
            self.BSphere = Vector4.fromBytes(self.bs.readBytes(16))
            self.BBoxCenter = Vector3.fromBytes(self.bs.readBytes(12))
            self.BBoxSize = Vector3.fromBytes(self.bs.readBytes(12))

        def readStateNameList(self):
            self.bs.readUInt() # size of stateName list
            stateNameCount = self.bs.readUInt() # count of stateName
            for stateName in range(stateNameCount):
                self.stateNameList.append(self.bs.bytesToString(self.bs.readBytes(self.bs.readShort())).replace("\0", ""))

        def readTextureNameList(self):
            self.bs.readUInt() # size of textureName list
            textureNameCount = self.bs.readUInt() # count of textureName
            for textureName in range(textureNameCount):
                self.textureNameList.append(self.bs.bytesToString(self.bs.readBytes(self.bs.readShort())).replace("\0", ""))


        class sShape:
            def __init__(self, bs, sSceneDatabase):
                self.bs = bs
                self.sSceneDatabase = sSceneDatabase

                self.sShapeName = ""
                self.sShapeInfoName = ""

                self.state = 0
                self.displayList = 0

                self.BSphere = 0
                self.BBoxCenter = 0
                self.BBoxSize = 0

                self.load()

            def load(self):
                #state = self.bs.readUShort()
                #if state == 4: # ???
                    #self.bs.readBytes(self.bs.readUInt())
                    #state = self.bs.readUShort()

                self.bs.readUShort()
                self.bs.readUInt() # size of sShape

                self.readSignatures()
                self.readBoundingBox()

                self.bs.readUInt()
                self.sShapeName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                self.bs.readUInt()
                self.sShapeInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

            def readSignatures(self):
                self.state = self.bs.readShort()
                self.displayList = self.bs.readShort()

            def readBoundingBox(self):
                if "BSphere" in self.sSceneDatabase._sSerial["_sSerial::_sShape"] and "BBoxCenter" in self.sSceneDatabase._sSerial["_sSerial::_sShape"] and "BBoxSize" in self.sSceneDatabase._sSerial["_sSerial::_sShape"]:
                    self.BSphere = Vector4.fromBytes(self.bs.readBytes(16))
                    self.BBoxCenter = Vector3.fromBytes(self.bs.readBytes(12))
                    self.BBoxSize = Vector3.fromBytes(self.bs.readBytes(12))


            class sState:
                def __init__(self, bs):
                    self.bs = bs

                    self.sStateName = ""
                    self.sStateInfoName = ""

                    self.fillType = 0
                    self.alphaRef = 0
                    
                    self.depthTest = 0
                    self.depthBias = 0
                    self.depthBiasRate = 0
                    self.depthBiasSlope = 0
                    
                    self.cullMode = 0
                    self.lightingModel = 0
                    self.maxInfluence = 0
                    self.uvSet = 0
                    
                    self.blendMode = 0
                    self.blendSrc = 0
                    self.blendDst = 0
                    
                    self.shininess = 0
                    self.opacity = 0
                    self.ambient = 0
                    self.diffuse = 0
                    self.specular = 0
                    self.emission = 0
                    self.constant = 0       

                    self.shaderDesc = 0
                    self.extrashaderDesc = 0

                    self.shaderName = None
                    self.texture = []
                    self.textureRef = None
                    self.shaderParameter0 = None
                    self.shaderParameter1 = None
                    self.userParameter = None

                    self.load()

                def load(self):
                    self.bs.readUShort()  # unknown 0x2
                    self.bs.readUInt()  # size of sState

                    self.readShaderProperties()

                    self.bs.readUInt() # size of shader name
                    self.shaderName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

                    self.readTextureSignatures()

                    self.bs.readBytes(self.bs.readInt())  # unknown 0x8

                    self.shaderParameter0 = self.bs.readBytes(16)
                    self.shaderParameter1 = self.bs.readBytes(16)

                    self.readUserParameters()

                    self.bs.readUInt() # size of sState name
                    self.sStateName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # material name
                    self.bs.readUInt() # size of info sState name
                    self.sStateInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # info material name

                def readShaderProperties(self):

                    self.fillType = self.bs.readByte()
                    self.alphaRef = self.bs.readByte()
                    
                    self.depthTest = self.bs.readByte()
                    self.depthBias = self.bs.readByte()
                    self.depthBiasRate = self.bs.readFloat()
                    self.depthBiasSlope = self.bs.readFloat()
                    
                    self.cullMode = self.bs.readByte()
                    self.lightingModel = self.bs.readByte()
                    self.maxInfluence = self.bs.readByte()
                    self.uvSet = self.bs.readByte()
                    
                    self.blendMode = self.bs.readByte()
                    self.blendSrc = self.bs.readByte()
                    self.blendDst = self.bs.readByte()
                    
                    self.shininess = self.bs.readFloat()
                    self.opacity = self.bs.readByte()
                    self.ambient = self.bs.readFloat()
                    self.diffuse = self.bs.readFloat()
                    self.specular = self.bs.readFloat()
                    self.emission = self.bs.readFloat()
                    self.constant = self.bs.readFloat()       

                    self.shaderDesc = self.bs.readUInt()
                    self.extrashaderDesc = self.bs.readUInt()

                def readTextureSignatures(self):

                    self.bs.readUInt()  # size of texture signatures name
                    textureSignatureCount = self.bs.readUInt()  # texture signatures count
                    for texture in range(textureSignatureCount):
                        self.texture.append(self.bs.readUShort())

                def readUserParameters(self):
                    self.bs.readUInt() # size of user parameters
                    userParameterCount = self.bs.readUInt() # user parameters count

                    for userParameter in range(userParameterCount):
                        self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                        self.bs.readBytes(4) # unknown 0x4
                        self.bs.readBytes(8) # zeros(?)
                        parameter = Vector3.fromBytes(self.bs.readBytes(12))
                        self.bs.readBytes(4) # zeros(?)


            class sDisplayList:
                def __init__(self, bs):
                    self.bs = bs

                    self.sDisplayListName = ""
                    self.sDisplayListInfoName = ""

                    self.geometry = None
                    self.primitiveList = []
                    self.blendGeometry = []
                    self.index = None
                    self.displayListRef = None
                    self.polygonNumber = None

                    self.load()

                def load(self):
                    self.bs.readShort() # ???
                    self.bs.readUInt() # size of sDisplayList data

                    self.readProperties()

                    self.bs.readUInt()
                    self.sDisplayListName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                    self.bs.readUInt()
                    self.sDisplayListInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

                def readProperties(self):
                    self.geometry = self.bs.readUShort()

                    # primitiveList
                    primitiveListSize = self.bs.readUInt()
                    primitiveListCount = self.bs.readUInt()
                    for primitiveList in range(primitiveListCount):
                        self.primitiveList.append(self.bs.readUShort())
                    
                    # blendGeometry
                    blendGeometrySize = self.bs.readUInt()
                    blendGeometryCount = self.bs.readUInt()
                    for blendGeometry in range(blendGeometryCount):
                        self.blendGeometry.append(self.bs.readUShort())
                    
                    # index ?
                    self.index = self.bs.readBytes(self.bs.readUInt()) # unknown signature

                    self.displayListRef = self.bs.readUShort()
                    self.polygonNumber = self.bs.readUInt()


                class sGeometry:
                    def __init__(self, bs, sSceneDatabase):
                        self.bs = bs
                        self.sSceneDatabase = sSceneDatabase

                        self.sGeometryName = ""
                        self.sGeometryInfoName = ""

                        self.vertexArrayDic = {}

                        self.vertexDesc = 0
                        self.vertexNumber = 0
                        self.vertexSize = 0
                        self.strideSize = 0
                        self.vertexArray = 0
                        self.userVertexArray = 0
                        self.userVertexArrayElementNumber = 0
                        self.flag = 0

                        self.load()

                    def load(self):
                        self.bs.readUShort()
                        self.bs.readUInt() # size of sGeometry data

                        self.readProperties()

                        self.vertexArrayDic[self.vertexArray] = 0

                        self.bs.readUInt()
                        self.sGeometryName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                        self.bs.readUInt()
                        self.sGeometryInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

                    def readProperties(self):
                        self.vertexDesc = self.bs.readUInt()
                        self.vertexNumber = self.bs.readUInt()
                        self.vertexSize = self.bs.readUInt()
                        self.strideSize = self.bs.readUInt()
                        self.vertexArray = self.bs.readUShort()

                        if "userVertexArray" in self.sSceneDatabase._sSerial["_sSerial::_sGeometry"]:
                            self.userVertexArray = self.bs.readUShort()

                        if "userVertexArrayElementNumber" in self.sSceneDatabase._sSerial["_sSerial::_sGeometry"]:
                            self.userVertexArrayElementNumber = self.bs.readUInt()
                        
                        self.flag = self.bs.readUByte()


                class sVertexArray:
                    def __init__(self, bs, sGeometry):
                        self.bs = bs
                        self.sGeometry = sGeometry

                        self.array = 0

                        self.load()

                    def load(self):
                        self.bs.readUShort()
                        self.bs.readUInt() # size of sVertexArray data

                        self.array = self.bs.readBytes(self.bs.readUInt())
                        
                        #self.bs.readUInt()

                        #self.array = self.bs.readBytes(self.sGeometry.strideSize * count)
                        #self.sGeometry.vertexArrayDic[self.sGeometry.vertexArray] = self.array
                        #self.sGeometry.vertexArray = (self.sGeometry.vertexArray, self.array)

                    class sVertexArrayP:
                        def __init__(self):
                            self.positions = []

                    class sVertexArrayPN:
                        def __init__(self):
                            self.positions = []
                            self.normals = []

                    class sVertexArrayPNC:
                        def __init__(self):
                            self.positions = []
                            self.normals = []
                            self.colors = []

                    class sVertexArrayPNCT:
                        def __init__(self):
                            self.positions = []
                            self.normals = []
                            self.colors = []
                            self.texCoords = []

                    class sVertexArrayPNCT2:
                        def __init__(self):
                            self.positions = []
                            self.normals = []
                            self.colors = []
                            self.texCoords = []

                    class sVertexArrayPNT:
                        def __init__(self):
                            self.positions = []
                            self.normals = []
                            self.texCoords = []

                    class sVertexArrayPNTW2:
                        def __init__(self):
                            self.positions = []
                            self.normals = []
                            self.texCoords = []


            class sPrimitiveList:
                def __init__(self, bs):
                    self.bs = bs

                    self.primitiveType = 0
                    self.primitiveNumber = 0
                    self.indexStart = 0
                    self.indexNumber = 0
                    self.startNumber = 0
                    self.endNumber = 0
                    self.vertexNumber = 0

                    self.load()

                def load(self):
                    self.bs.readShort() # ???
                    self.bs.readUInt() # size of sPrimitiveList data
                    
                    self.primitiveType = self.bs.readUInt()
                    self.primitiveNumber = self.bs.readUInt()
                    self.indexStart = self.bs.readUInt()
                    self.indexNumber = self.bs.readUInt()
                    self.startNumber = self.bs.readUInt()
                    self.endNumber = self.bs.readUInt()
                    self.vertexNumber = self.bs.readUInt()


            class sTexture:
                def __init__(self, bs, sSceneDatabase):
                    self.bs = bs
                    self.sSceneDatabase = sSceneDatabase

                    self.sTextureName = ""
                    self.sTextureInfoName = ""

                    self.alphaRef = 0
                    
                    self.height = 0  
                    self.width = 0
                    
                    self.format = 0
                    self.alphaMode = 0
                    
                    self.wrapU = 0
                    self.wrapV = 0
                    
                    self.minFilter = 0
                    self.magFilter = 0
                    self.mipFilter = 0
                    
                    self.useMipmap = 0
                    self.maxMipmapLevel = 0
                    
                    self.anisoNumber = 0
                    self.preserveFormat = 0
                    self.lodBias = 0
                    
                    self.fileName = 0
                    self.plugName = 0

                    self.normalMapCompressMode = 0
                    
                    self.uvScale = 0
                    self.uvOffset = 0
                    self.uvSetIndex = 0
                    
                    self.textureType = 0
                    self.textureID = 0
                    self.textureImage = 0

                    self.mipmapFileName = 0
                    self.userParameter = 0
                    
                    self.load()

                def load(self):
                    self.bs.readShort() # ???
                    self.bs.readUInt() # size of sTexture data

                    self.readTextureProperties()

                    self.bs.readUInt() 
                    self.sTextureName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                    self.bs.readUInt()
                    self.sTextureInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

                def readTextureProperties(self):

                    self.alphaRef = self.bs.readUByte()
                    
                    self.height = self.bs.readUShort()  
                    self.width = self.bs.readUShort() 
                    
                    self.format = self.bs.readUByte()
                    self.alphaMode = self.bs.readUByte()
                    
                    self.wrapU = self.bs.readUByte()
                    self.wrapV = self.bs.readUByte()
                    
                    self.minFilter = self.bs.readUByte()
                    self.magFilter = self.bs.readUByte()
                    self.mipFilter = self.bs.readUByte()
                    
                    self.useMipmap = self.bs.readUByte()
                    self.maxMipmapLevel = self.bs.readUByte()
                    
                    self.anisoNumber = self.bs.readUByte()
                    self.preserveFormat = self.bs.readUByte()
                    self.lodBias = self.bs.readUInt()

                    self.bs.readUInt() # fileName Size
                    self.fileName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                    
                    
                    if "plugName" in self.sSceneDatabase._sSerial["_sSerial::_sTexture"]:
                        self.bs.readUInt() # plugName Size
                        self.plugName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

                    self.bs.readUInt() # normalMapCompressMode Size
                    self.normalMapCompressMode = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                    
                    self.uvScale = self.bs.readBytes(8)
                    self.uvOffset = self.bs.readBytes(8)
                    self.uvSetIndex = self.bs.readByte()
                    
                    self.textureType = self.bs.readByte()
                    self.textureID = self.bs.readByte()
                    self.textureImage = self.bs.readShort()

                    # TO DO
                    self.bs.readUInt() # size of mipmap FileNames
                    mipmapFileNameCount = self.bs.readUInt() # mipmap FileNames count
                    self.mipmapFileName = 0 

                    # TO DO
                    if "userParameter" in self.sSceneDatabase._sSerial["_sSerial::_sTexture"]:
                        self.bs.readUInt() # size of user parameters
                        userParameterCount = self.bs.readUInt() # user parameters count
                        self.userParameter = 0 


                class sTextureImage:
                    def __init__(self, bs):
                        self.bs = bs

                        self.sTextureImageName = ""
                        self.sTextureImageInfoName = ""

                        self.file = 0
                        self.maxMipmapLevel = 0
                        self.fileName = 0
                        self.separateImageSize = 0
                        self.separateImageOffset = 0

                        self.load()
                        
                    def load(self):
                        self.bs.readShort() # ???
                        self.bs.readUInt() # size of sTextureImage data

                        self.readImage()

                        self.maxMipmapLevel = self.bs.readByte()

                        self.bs.readUInt() # fileName Size
                        self.fileName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                        
                        self.separateImageSize = self.bs.readUInt()
                        self.separateImageOffset = self.bs.readUInt()

                        self.bs.readUInt() 
                        self.sTextureImageName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                        self.bs.readUInt()
                        self.sTextureImageInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

                    def readImage(self):
                        self.file = self.bs.readBytes(self.bs.readUInt())


    class sSkeleton:
        def __init__(self, bs):
            self.bs = bs

            self.boneDic = {}
            self.bone = []
            self.blendBoneNumber = 0

            self.load()

        def load(self):
            self.bs.readShort() # ???
            self.bs.readUInt() # size of sSkeleton data

            self.bs.readUInt() # size of bone
            
            boneCount = self.bs.readUInt()
            for bone in range(boneCount):
                self.bone.append(self.bs.readUShort)
            self.blendBoneNumber = self.bs.readUInt()


        class sBone:
            def __init__(self, bs):
                self.bs = bs

                self.shapeHeader = 0
                self.parentName = 0
                self.vertexBlendTarget = 0
            
                self.mtxLocal = 0
                self.mtxDefault = 0
                
                self.parentIndex = 0
                self.blendIndex = 0
                self.shapeHeaderIndex = 0
                self.isInstance = 0
                
                self.parent = 0
                self.child = 0
                self.sibling = 0
                
                self.userParameter = 0
            
                self.scale = 0
                self.rotation = 0
                self.quaternion = 0
                self.translation = 0

                self.load()

            def load(self):
                self.bs.readUShort() # ???
                self.bs.readUInt() # size of sBone data

                self.shapeHeader = self.bs.readUShort()
            
                self.bs.readUInt() # parentName size
                self.parentName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

                self.vertexBlendTarget = self.bs.readByte()

                self.readMatrices()

                self.parentIndex = self.bs.readUInt()
                self.blendIndex = self.bs.readUInt()
                self.shapeHeaderIndex = self.bs.readUInt()
                
                self.isInstance = self.bs.readByte()

                self.parent = self.bs.readUShort()
                self.child = self.bs.readUShort()
                self.sibling = self.bs.readUShort()

                self.readUserParameters()

                self.readTransformations()

            def readMatrices(self):
                self.mtxLocal = self.bs.readBytes(48)
                self.mtxDefault = self.bs.readBytes(48)

            def readUserParameters(self):
                self.bs.readUInt() # size of user parameters
                userParameterCount = self.bs.readUInt() # user parameters count
                for userParameter in range(userParameterCount):
                    self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
                    self.bs.readBytes(28) # ???

            def readTransformations(self):
                self.scale = self.bs.readBytes(12)
                self.rotation = self.bs.readBytes(12)
                self.quaternion = self.bs.readBytes(16)
                self.translation = self.bs.readBytes(12)


class EFO:
    def __init__(self, filepath):
        efo_file = open(filepath, 'rb')
        binaryReader = BinaryReader(efo_file)

        self._sSceneDatabase = sSceneDatabase(binaryReader)
        print(binaryReader.tell())
        
        if "_sSerial::_sShapeHeader" in self._sSceneDatabase._sSerial:  # TEST

            for shapeHeader in self._sSceneDatabase.shapeHeaderSignatures:
                
                _sShapeHeader = sSceneDatabase.sShapeHeader(binaryReader)
                print(binaryReader.tell())
                self._sSceneDatabase.shapeHeader[shapeHeader] = _sShapeHeader

                for shape in _sShapeHeader.shape:
                    
                    _sShape = sSceneDatabase.sShapeHeader.sShape(binaryReader, self._sSceneDatabase)
                    print(binaryReader.tell())
                    #_sShapeHeader.shapeDic[shape] = _sShape
                    self._sSceneDatabase.shape[shape] = _sShape

                    if _sShape.state not in self._sSceneDatabase.state:
                        _sState = sSceneDatabase.sShapeHeader.sShape.sState(binaryReader)
                        print(binaryReader.tell())
                        self._sSceneDatabase.state[_sShape.state] = _sState


                    for texture in _sState.texture:
                        if texture not in self._sSceneDatabase.texture:
                            _sTexture = sSceneDatabase.sShapeHeader.sShape.sTexture(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            self._sSceneDatabase.texture[texture] = _sTexture
                            
                            if _sTexture.textureImage > 0 and _sTexture.textureImage not in self._sSceneDatabase.textureImage:

                                _sTextureImage = sSceneDatabase.sShapeHeader.sShape.sTexture.sTextureImage(binaryReader)
                                print(binaryReader.tell())
                                self._sSceneDatabase.textureImage[_sTexture.textureImage] = _sTextureImage


                    if _sShape.displayList not in self._sSceneDatabase.displayList:
                    
                        _sDisplayList = sSceneDatabase.sShapeHeader.sShape.sDisplayList(binaryReader)
                        print(binaryReader.tell())
                        self._sSceneDatabase.displayList[_sShape.displayList] = _sDisplayList

                        if _sDisplayList.geometry not in self._sSceneDatabase.geometry:
                            
                            _sGeometry = sSceneDatabase.sShapeHeader.sShape.sDisplayList.sGeometry(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            self._sSceneDatabase.geometry[_sDisplayList.geometry] = _sGeometry

                            _sVertexArray = sSceneDatabase.sShapeHeader.sShape.sDisplayList.sVertexArray(binaryReader, _sGeometry)
                            print(binaryReader.tell())
                            self._sSceneDatabase.vertexArray[_sGeometry.vertexArray] = _sVertexArray

                        _sPrimitiveList = sSceneDatabase.sShapeHeader.sShape.sPrimitiveList(binaryReader)
                        print(binaryReader.tell())
                        self._sSceneDatabase.primitiveList[_sDisplayList.primitiveList[0]] = _sPrimitiveList

                        # ???
                        binaryReader.readBytes(binaryReader.readUInt())
                        binaryReader.readBytes(binaryReader.readUInt())

                        print(binaryReader.tell())

                        #if _sDisplayList.geometry != self._sSceneDatabase.geometrySignatures[0] and self._sSceneDatabase.geometrySignatures[0] not in self._sSceneDatabase.geometry:
                        # TO FIX
                        #if _sDisplayList.geometry == min(self._sSceneDatabase.geometrySignatures) and _sShape.displayList == min(self._sSceneDatabase.displayListSignatures):
                        if _sShape.displayList != self._sSceneDatabase.displayListSignatures[0] and self._sSceneDatabase.displayListSignatures[0] not in self._sSceneDatabase.displayList:

                            _sDisplayList = sSceneDatabase.sShapeHeader.sShape.sDisplayList(binaryReader)
                            print(binaryReader.tell())
                            self._sSceneDatabase.displayList[self._sSceneDatabase.displayListSignatures[0]] = _sDisplayList

                            if _sDisplayList.geometry not in self._sSceneDatabase.geometry:
                                
                                _sGeometry = sSceneDatabase.sShapeHeader.sShape.sDisplayList.sGeometry(binaryReader, self._sSceneDatabase)
                                print(binaryReader.tell())
                                self._sSceneDatabase.geometry[_sDisplayList.geometry] = _sGeometry

                                _sVertexArray = sSceneDatabase.sShapeHeader.sShape.sDisplayList.sVertexArray(binaryReader, _sGeometry)
                                print(binaryReader.tell())
                                self._sSceneDatabase.vertexArray[_sGeometry.vertexArray] = _sVertexArray

                            _sPrimitiveList = sSceneDatabase.sShapeHeader.sShape.sPrimitiveList(binaryReader)
                            print(binaryReader.tell())
                            self._sSceneDatabase.primitiveList[_sDisplayList.primitiveList[0]] = _sPrimitiveList

                            # ???
                            binaryReader.readBytes(binaryReader.readUInt())
                            binaryReader.readBytes(binaryReader.readUInt())
                            
                            print(binaryReader.tell())
            
                print(binaryReader.tell())

            print(binaryReader.tell())
