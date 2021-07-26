class SHAPE:
    def __init__(self):
        self.shapeName = ""
        self.geomName = ""

        self.buffer = None
        self.shader = None

        # _sSerial::_sPrimitiveList
        self.primitiveType = 0
        self.primitiveNumber = 0
        self.indexStart = 0
        self.indexNumber = 0
        self.startNumber = 0
        self.endNumber = 0
        self.vertexNumber = 0

        self.subBuffers = []


class BUFFER:
    def __init__(self):
        self.buffer = None
        self.bufferName = None

        # _sSerial::_sGeometry
        self.vertexDesc = 0
        self.vertexNumber = 0
        self.vertexSize = 0
        self.strideSize = 0
        self.vertexArray = 0
        self.userVertexArray = 0
        self.userVertexArrayElementNumber = 0
        self.flag = 0


class SHADER:
    def __init__(self):
        self.shaderName = ""
        self.materialName = ""
        self.textures = []

        self.fillType = 0
        self.alphaRef = 0

        self.depthTest = 0
        self.depthBias = 0
        self.depthBiasRate = 0
        self.depthBiasSlope = 0

        self.cullMode = 0
        self.lightingModel = 0
        self.maxInfluence = 0
        self.uvSet = 0

        self.blendMode = 0
        self.blendSrc = 0
        self.blendDst = 0

        self.shininess = 0
        self.opacity = 0
        self.ambient = 0
        self.diffuse = 0
        self.specular = 0
        self.emission = 0
        self.constant = 0

        self.shaderDesc = 0
        self.extrashaderDesc = 0

        self.shaderParameter0 = 0
        self.shaderParameter1 = 0


class TEXTURE:
    def __init__(self):
        self.textureName = ""
        self.dds = None


class DDS:
    def __init__(self):
        self.ddsName = ""

        self.height = 0
        self.width = 0

        self.fourCC = 0

        self.pixelFormat = None

        self.buffer = None


class SKELETON:
    def __init__(self):
        self.boneList = []


class BONE :
    def __init__(self):
        self.boneName = ""
        self.index = 0

        self.parentName = 0

        self.parentIndex = 0
        self.blendIndex = 0
        self.shapeHeaderIndex = 0

        self.parent = 0
        self.child = 0
        self.sibling = 0

        self.boneMatrix = None


class DDSPixelFormat :
    def __init__(self):
        self.size = 0
        self.flags = 0
        self.fourCC = 0
        self.RGBBitCount = 0
        self.RBitMask = 0
        self.GBitMask = 0
        self.BBitMask = 0
        self.ABitMask = 0

