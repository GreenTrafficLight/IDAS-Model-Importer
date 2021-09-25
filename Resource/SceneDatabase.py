from ..Utilities import *

class sSceneDatabase:
    
    def __init__(self, br):
        self.br = br
        
        self.name = ""
        self.infoName = ""

        self._sSerial = {}

        self.shapeHeader = {}
        self.state = {}
        self.geometry = {}
        self.displayList = {}
        self.texture = {}
        self.skeleton = {}
        self.textureImage = {}

        self.vertexArray = {}
        self.primitiveList = {}
        self.shape = {}
        self.bone = {}

        self.shapeHeaderSignatures = []
        self.stateSignatures = []
        self.geometrySignatures = []
        self.displayListSignatures = []
        self.textureSignatures = []
        self.skeletonSignatures = []
        self.textureImageSignatures = []


        self.load()

    def load(self):
        magic = self.br.bytesToString(self.br.readBytes(4))
        self.br.seek(4, 1)
        fileSize = self.br.readInt()
        self.br.seek(4, 1)
        unknown = self.br.readByte()
        
        if unknown == 0:
            pass
        
        elif unknown == 6:
            self.br.seek(4, 1)
            self.br.seek(1, 1)  # unknown byte
            self.br.seek(self.br.readUShort(), 1)  # _sSerial::_sSceneDatabase
            self.br.seek(1, 1)  # zero

        else:
            self.br.seek(-1, 1)
            self.br.seek(1, 1)  # unknown byte
            self.br.seek(self.br.readUShort(), 1)  # _sSerial::_sSceneDatabase
            self.br.seek(1, 1)  # zero

        self.br.bytesToString(self.br.readBytes(self.br.readByte()))
        self.br.bytesToString(self.br.readBytes(self.br.readByte()))  # yabukita

        self.br.seek(4, 1)  # 0x3ED (unknown)

        self.br.bytesToString(self.br.readBytes(self.br.readByte()))  # _sSerial

        self.br.readBytes(4)  # unknown array of bytes 0x4
        self.br.seek(1, 1)  # zero

        self.br.bytesToString(self.br.readBytes(self.br.readByte()))  # yabukita::Object

        self.br.readInt()  # 0x1 (unknown)

        # Read _sSerial
        self.get_sSerial()

        if "_sSerial::_sShapeHeader" in self._sSerial:
            self.br.seek(1, 1)  # zero

            # Read textures path
            self.getTexturesPath()
        
        else:
            self.getTextures()

            self.br.seek(1, 1)  # zero


        self.br.seek(2, 1)  # unknown 0x2
        self.br.seek(2, 1)  # unknown 0x2

        self.br.readInt()  # size of essd

        self.br.bytesToString(self.br.readBytes(4))

        self.br.seek(4, 1)  # zeros

        self.br.readBytes(4)  # 0x4112904

        skip = self.br.readInt()

        if skip == 2:
            self.br.seek(skip, 1)
        elif skip == 3:
            self.br.seek(skip, 1)
        elif skip == 23:
            self.br.bytesToString(self.br.readBytes(self.br.readShort())).replace("\0", "")
        else:
            self.br.seek(-4, 1)

        self.br.readInt()  # unknown 0x1

        # Read Signatures
        self.getSignatures()

        textureSize = self.br.readInt()
        textureImageSize = self.br.readInt()
        shapeHeaderSize = self.br.readInt()
        geometrySize = self.br.readInt()
        displayListSize = self.br.readInt()
        skeletonSize = self.br.readInt()

        if "userFile" in self._sSerial["_sSerial::_sSceneDatabase"]:

            self.br.readInt()  # size of texture names list (and infos ?)
            self.br.readInt()  # unknown
            self.br.readInt()  # size of texture names list
            textureNamesCount = self.br.readInt()

            for i in range(textureNamesCount):
                self.br.bytesToString(self.br.readBytes(self.br.readUInt()))

            if textureNamesCount != 0:
                self.br.readInt()  # size of textbl path
                self.br.readInt()  # count of textbl path ?
                self.br.bytesToString(self.br.readBytes(self.br.readUShort()))  # textbl path

        self.br.readInt()  # size of sSceneDatabase name
        self.name = self.br.bytesToString(self.br.readBytes(self.br.readShort()))  # sSceneDatabase name
        self.br.readInt()  # size of info sSceneDatabase name
        self.infoName = self.br.bytesToString(self.br.readBytes(self.br.readShort()))  # info sSceneDatabase name

    def get_sSerial(self): # Read the informations at the start
        while True:
            _sSerialName = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
            if "_sSerial::" in _sSerialName:
                self.br.seek(3, 1)  # zeros
                self._sSerial[_sSerialName] = {}
                while True:
                    name = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
                    if name == "":
                        break
                    self._sSerial[_sSerialName][name] = (self.br.readByte(), self.br.readByte())
                    self.br.seek(1, 1)  # zero
            else:
                break

    def getTexturesPath(self):
        while True:
            texturePath = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
            if texturePath == "":
                break

    def getTextures(self):
        while True:
            texture = self.br.bytesToString(self.br.readBytes(self.br.readByte())).replace("\0", "")
            if texture == "":
                break
            textureSignature = self.br.readShort()

    def getSignatures(self):

        # shapeHeader signatures
        self.br.readUInt()  # size of shapeHeader signatures
        count = self.br.readUInt()  # shapeHeader signatures count
        for signature in range(count):
            self.shapeHeaderSignatures.append(self.br.readUShort())

        # state signatures
        self.br.readUInt()  # size of state signatures
        count = self.br.readUInt()  # state signatures count
        for signature in range(count):
            self.stateSignatures.append(self.br.readUShort())

        # geometry signatures
        self.br.readUInt()  # size of geometry signatures
        count = self.br.readUInt()  # geometry signatures count
        for signature in range(count):
            self.geometrySignatures.append(self.br.readUShort())

        # displayList signatures
        self.br.readUInt()  # size of displayList signatures
        count = self.br.readUInt()  # displayList signatures count
        for signature in range(count):
            self.displayListSignatures.append(self.br.readUShort())

        # texture signatures
        self.br.readUInt()  # size of texture signatures
        count = self.br.readUInt()  # texture signatures count
        for signature in range(count):
            self.textureSignatures.append(self.br.readUShort())

        # skeleton signatures
        self.br.readUInt()  # size of skeleton signatures
        count = self.br.readUInt()  # skeleton signatures count
        for signature in range(count):
            self.skeletonSignatures.append(self.br.readUShort())

        # textureImage signatures
        self.br.readUInt()  # size of textureImage signatures
        count = self.br.readUInt()  # textureImage signatures count
        for signature in range(count):
            self.textureImageSignatures.append(self.br.readShort())
