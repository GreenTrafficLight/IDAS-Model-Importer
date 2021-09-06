from ..Utilities import *

from .ShapeHeader import sShapeHeader

class sShape(sShapeHeader):
    
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
    
    class sPrimitiveList:

        def __init__(self, bs, sSceneDatabase):
            self.bs = bs
            self.sSceneDatabase = sSceneDatabase

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
            
            if "endNumber" in self.sSceneDatabase._sSerial["_sSerial::_sPrimitiveList"]:
                self.endNumber = self.bs.readUInt()
            
            self.vertexNumber = self.bs.readUInt()
