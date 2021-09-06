from ..Utilities import *

from .Shape import sShape

class sDisplayList(sShape):

    def __init__(self, bs, sSceneDatabase):
        self.bs = bs
        self.sSceneDatabase = sSceneDatabase

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
        
        self.index = self.bs.readBytes(self.bs.readUInt()) # unknown signature

        self.displayListRef = self.bs.readUShort()

        if "polygonNumber" in self.sSceneDatabase._sSerial["_sSerial::_sDisplayList"]:
            self.polygonNumber = self.bs.readUInt()
