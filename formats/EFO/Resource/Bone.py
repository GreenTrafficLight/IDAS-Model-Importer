from ....utilities import *

from .Skeleton import sSkeleton

class sBone(sSkeleton):
    
    def __init__(self, bs: BinaryReader, sSceneDatabase):
        self.bs = bs

        self.name = ""
        self.infoName = ""

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

        self.load(sSceneDatabase)

    def load(self, sSceneDatabase):
        self.bs.readUShort() # ???
        self.bs.readUInt() # size of sBone data

        self.shapeHeader = self.bs.readUShort()
    
        self.bs.readUInt() # parentName size
        self.parentName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

        self.vertexBlendTarget = self.bs.readByte()

        self.readMatrices()

        self.parentIndex = self.bs.readInt()
        self.blendIndex = self.bs.readInt()
        self.shapeHeaderIndex = self.bs.readInt()
        
        if "isInstance" in sSceneDatabase._sSerial["_sSerial::_sBone"]:
            self.isInstance = self.bs.readByte()

        self.parent = self.bs.readUShort()
        self.child = self.bs.readUShort()
        self.sibling = self.bs.readUShort()

        self.readUserParameters()

        self.readTransformations(sSceneDatabase)

        self.bs.readUInt() # size of sBone name
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # sBone name
        self.bs.readUInt() # size of info sBone name
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # info sBone name

    def readMatrices(self):
        self.mtxLocal = self.bs.readMatrix3x4()
        self.mtxDefault = self.bs.readMatrix3x4()

    def readUserParameters(self):
        self.bs.readUInt() # size of user parameters
        userParameterCount = self.bs.readUInt() # user parameters count
        for userParameter in range(userParameterCount):
            self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
            self.bs.readBytes(28) # ???

    def readTransformations(self, sSceneDatabase):
        self.scale = self.bs.readVector3f()
        if "rotation" in sSceneDatabase._sSerial["_sSerial::_sBone"]:
            self.rotation = self.bs.readVector3f()
        self.quaternion = self.bs.readVector4f()
        self.translation = self.bs.readVector3f()
