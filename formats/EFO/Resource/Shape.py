from ....utilities import *

from .ShapeHeader import sShapeHeader

class sShape(sShapeHeader):
    
    def __init__(self, bs: BinaryReader, sSceneDatabase):
        self.bs = bs

        self.name = ""
        self.infoName = ""

        self.state = 0
        self.displayList = 0

        self.BSphere = None
        self.BBoxCenter = None
        self.BBoxSize = None

        self.load(sSceneDatabase)

    def load(self, sSceneDatabase):
        self.bs.readUShort()
        self.bs.readUInt() # size of sShape

        self.readSignatures()
        self.readBoundingBox(sSceneDatabase)

        self.bs.readUInt()
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        self.bs.readUInt()
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

    def readSignatures(self):
        self.state = self.bs.readShort()
        self.displayList = self.bs.readShort()

    def readBoundingBox(self, sSceneDatabase):
        if "BSphere" in sSceneDatabase._sSerial["_sSerial::_sShape"] and "BBoxCenter" in sSceneDatabase._sSerial["_sSerial::_sShape"] and "BBoxSize" in sSceneDatabase._sSerial["_sSerial::_sShape"]:
            self.BSphere = self.bs.readVector4f()
            self.BBoxCenter = self.bs.readVector3f()
            self.BBoxSize = self.bs.readVector3f()
    
    class sPrimitiveList:

        def __init__(self, bs: BinaryReader, sSceneDatabase):
            self.bs = bs

            self.primitiveType = 0
            self.primitiveNumber = 0
            self.indexStart = 0
            self.indexNumber = 0
            self.startNumber = 0
            self.endNumber = 0
            self.vertexNumber = 0

            self.load(sSceneDatabase)

        def load(self, sSceneDatabase):
            self.bs.readShort() # ???
            self.bs.readUInt() # size of sPrimitiveList data
            
            self.primitiveType = self.bs.readUInt()
            self.primitiveNumber = self.bs.readUInt()
            self.indexStart = self.bs.readUInt()
            self.indexNumber = self.bs.readUInt()
            self.startNumber = self.bs.readUInt()
            
            if "endNumber" in sSceneDatabase._sSerial["_sSerial::_sPrimitiveList"]:
                self.endNumber = self.bs.readUInt()
            
            self.vertexNumber = self.bs.readUInt()
