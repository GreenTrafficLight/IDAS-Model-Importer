from ..Utilities import *

from .Shape import sShape

class sTexture(sShape):

    def __init__(self, bs, sSceneDatabase):
        self.bs = bs

        self.name = ""
        self.infoName = ""

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

        self.mipmapFileName = []
        self.userParameter = 0
        
        self.load(sSceneDatabase)

    def load(self, sSceneDatabase):
        self.bs.readShort()
        self.bs.readUInt() # size of sTexture data

        self.readTextureProperties(sSceneDatabase)

        self.bs.readUInt() 
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        self.bs.readUInt()
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

    def readTextureProperties(self, sSceneDatabase):

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

        if "preserveFormat" in sSceneDatabase._sSerial["_sSerial::_sTexture"]:
            self.preserveFormat = self.bs.readUByte()
        
        self.lodBias = self.bs.readUInt()

        self.bs.readUInt() # fileName Size
        self.fileName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        
        
        if "plugName" in sSceneDatabase._sSerial["_sSerial::_sTexture"]:
            self.bs.readUInt() # plugName Size
            self.plugName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

        self.bs.readUInt() # normalMapCompressMode Size
        self.normalMapCompressMode = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        
        self.uvScale = (self.bs.readFloat() , self.bs.readFloat())
        self.uvOffset = (self.bs.readFloat() , self.bs.readFloat())
        self.uvSetIndex = self.bs.readByte()
        
        self.textureType = self.bs.readByte()
        self.textureID = self.bs.readByte()
        self.textureImage = self.bs.readShort()

        self.bs.readUInt() # size of mipmap FileNames
        mipmapFileNameCount = self.bs.readUInt() # mipmap FileNames count
        for mipmapFileName in range(mipmapFileNameCount):
            self.mipmapFileName.append(self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")) 

        # TO DO
        if "userParameter" in sSceneDatabase._sSerial["_sSerial::_sTexture"]:
            self.bs.readUInt() # size of user parameters
            userParameterCount = self.bs.readUInt() # user parameters count
            self.userParameter = 0 
