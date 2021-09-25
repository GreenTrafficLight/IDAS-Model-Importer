from ..Utilities import *

from .Texture import sTexture

class sTextureImage(sTexture):
    
    def __init__(self, bs, sSceneDatabase):
        self.bs = bs

        self.name = ""
        self.infoName = ""

        self.file = 0
        self.maxMipmapLevel = 0
        self.fileName = None

        self.flag = 0

        self.separateImageSize = 0
        self.separateImageOffset = 0

        self.load(sSceneDatabase)
        
    def load(self, sSceneDatabase):
        self.bs.readShort()
        self.bs.readUInt() # size of sTextureImage data

        self.readImage()

        self.maxMipmapLevel = self.bs.readByte()

        if "fileName" in sSceneDatabase._sSerial["_sSerial::_sTextureImage"]:
            self.bs.readUInt() # fileName Size
            self.fileName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        
        if "flag" in sSceneDatabase._sSerial["_sSerial::_sTextureImage"]:
            self.flag = self.bs.readUInt()

        if "separateImageSize" in sSceneDatabase._sSerial["_sSerial::_sTextureImage"]:
            self.separateImageSize = self.bs.readUInt()
        if "separateImageOffset" in sSceneDatabase._sSerial["_sSerial::_sTextureImage"]:
            self.separateImageOffset = self.bs.readUInt()

        self.bs.readUInt() 
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        self.bs.readUInt()
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

    def readImage(self):
        self.file = self.bs.readBytes(self.bs.readUInt())
