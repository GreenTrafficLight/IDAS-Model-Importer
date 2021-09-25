from ..Utilities import *

class sSkeleton:

    def __init__(self, bs):
        self.bs = bs

        self.name = ""
        self.infoName = ""

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
            self.bone.append(self.bs.readUShort())
        self.blendBoneNumber = self.bs.readUInt()

        self.bs.readUInt() # size of sSkeleton name
        self.name = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # sSkeleton name
        self.bs.readUInt() # size of info sSkeleton name
        self.infoName = self.bs.bytesToString(self.bs.readBytes(self.bs.readUShort())).replace("\0", "") # info sSkeleton name
