from ..Utilities import *

from .SceneDatabase import sSceneDatabase

class sShapeHeader(sSceneDatabase):
    
    def __init__(self, bs, sSceneDatabase):
        self.bs = bs
        self.sSceneDatabase = sSceneDatabase

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

        if "sortGroup" in self.sSceneDatabase._sSerial["_sSerial::_sShapeHeader"]:
            self.sortGroup = self.bs.readShort()

        if "stateNameList" in self.sSceneDatabase._sSerial["_sSerial::_sShapeHeader"]:
            self.readStateNameList()
        
        if "textureNameList" in self.sSceneDatabase._sSerial["_sSerial::_sShapeHeader"]:
            self.readTextureNameList()

        self.bs.readUInt()
        self.sShapeHeaderName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        self.bs.readUInt()
        self.sShapeHeaderInfoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

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
