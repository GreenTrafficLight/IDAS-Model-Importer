from ..Utilities import *

from .Shape import sShape

class sState(sShape):
   
    def __init__(self, bs, sSceneDatabase):
        self.bs = bs

        self.name = ""
        self.infoName = ""

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
        
        #self.userParameter = []
        self.userParameter = {}

        self.load(sSceneDatabase)

    def load(self, sSceneDatabase):
        self.bs.readUShort()  # unknown 0x2
        self.bs.readUInt()  # size of sState

        self.readShaderProperties(sSceneDatabase)

        self.bs.readUInt() # size of shader name
        self.shaderName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

        self.readTextureSignatures()

        self.bs.readBytes(self.bs.readInt())  # unknown 0x8

        self.shaderParameter0 = self.bs.readBytes(16)
        self.shaderParameter1 = self.bs.readBytes(16)

        self.readUserParameters()

        self.bs.readUInt() # size of sState name
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # material name
        self.bs.readUInt() # size of info sState name
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # info material name

    def readShaderProperties(self, sSceneDatabase):

        self.fillType = self.bs.readByte()
        self.alphaRef = self.bs.readByte()
        
        if "depthTest" in sSceneDatabase._sSerial["_sSerial::_sState"]:
            self.depthTest = self.bs.readByte()
        if "depthBias" in sSceneDatabase._sSerial["_sSerial::_sState"]:
            self.depthBias = self.bs.readByte()
        if "depthBiasRate" in sSceneDatabase._sSerial["_sSerial::_sState"]:
            self.depthBiasRate = self.bs.readFloat()
        if "depthBiasSlope" in sSceneDatabase._sSerial["_sSerial::_sState"]:
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

        if "constant" in sSceneDatabase._sSerial["_sSerial::_sState"]:
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

        """
        for i in range(userParameterCount):
            _sUserParameter = sSceneDatabase.sShapeHeader.sShape.sState.sUserParameter()
            _sUserParameter.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
            self.bs.readBytes(4) # unknown 0x4
            self.bs.readBytes(8) # zeros(?)
            _sUserParameter.value = Vector3.fromBytes(self.bs.readBytes(12))
            self.bs.readBytes(4) # zeros(?)

            self.userParameter.append(_sUserParameter)
        """
        for i in range(userParameterCount):
            userParameterName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
            self.bs.readBytes(4) # unknown 0x4
            self.bs.readBytes(8) # zeros(?)
            userParameterValue = Vector3.fromBytes(self.bs.readBytes(12))
            self.bs.readBytes(4) # zeros(?)
            
            self.userParameter[userParameterName] = userParameterValue

    class sUserParameter:
        def __init__(self):
            super().__init__()

            self.name = ""
            self.value = 0
