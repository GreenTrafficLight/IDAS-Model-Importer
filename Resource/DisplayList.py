from ..Utilities import *

from .Shape import sShape

class sDisplayList(sShape):

    def __init__(self, bs, sSceneDatabase):
        self.bs = bs

        self.name = ""
        self.infoName = ""

        self.geometry = None
        self.primitiveList = []
        self.blendGeometry = {}
        self.index = None
        self.displayListRef = None
        self.polygonNumber = None

        self.load(sSceneDatabase)

    def load(self, sSceneDatabase):
        self.bs.readShort() # ???
        self.bs.readUInt() # size of sDisplayList data

        self.readProperties(sSceneDatabase)

        self.bs.readUInt()
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")
        self.bs.readUInt()
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "")

    def readProperties(self, sSceneDatabase):
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
            self.blendGeometry[self.bs.readUShort()] = None
        
        self.index = self.bs.readBytes(self.bs.readUInt()) # unknown signature

        self.displayListRef = self.bs.readUShort()

        if "polygonNumber" in sSceneDatabase._sSerial["_sSerial::_sDisplayList"]:
            self.polygonNumber = self.bs.readUInt()
