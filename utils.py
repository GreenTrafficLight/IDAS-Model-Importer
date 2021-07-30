import struct


class BinaryReader:
    def __init__(self, data, endian="<"):
        self.data = data
        self.endian = endian
        
        self.seek(0)

        self.stream = self.data.tell()

    def seek(self, offset, option=0):
        if option == 1:
            self.data.seek(offset, 1)
        elif option == 2:
            self.data.seek(offset, 2)
        else:
            self.data.seek(offset, 0)

    def tell(self):
        return self.data.tell()

    def read(self, size):
        return self.data.read(size)

    def readChar(self):
        return struct.unpack(self.endian + "c", self.read(1))[0]

    def readByte(self):
        return struct.unpack(self.endian + "b", self.read(1))[0]

    def readUByte(self):
        return struct.unpack(self.endian + "B", self.read(1))[0]

    def readShort(self):
        return struct.unpack(self.endian + "h", self.read(2))[0]

    def readUShort(self):
        return struct.unpack(self.endian + "H", self.read(2))[0]

    def readInt(self):
        return struct.unpack(self.endian + "i", self.read(4))[0]

    def readUInt(self):
        return struct.unpack(self.endian + "I", self.read(4))[0]

    def readLong(self):
        return struct.unpack(self.endian + "l", self.read(8))[0]

    def readULong(self):
        return struct.unpack(self.endian + "L", self.read(8))[0]

    def readBytes(self, size):
        ret = bytearray()
        for i in range(size):
            ret.append(struct.unpack(self.endian + "B", self.read(1))[0])
        return bytes(ret)

    def readFloat(self):
        return struct.unpack(self.endian + "f", self.read(4))[0]

    def readDouble(self):
        return struct.unpack(self.endian + "d", self.read(8))[0]

    def readString(self, encoding="utf-8"):
        bytes = []

        while True:
            character = self.read(1)
            if character == "\x00":
                break
            else:
                bytes.append(character)

        return bytes.decode(encoding)

    def bytesToString(self, byteArray, encoding="utf-8"):
        return byteArray.decode(encoding)


class Matrix4x4:
    def __init__(self, matrix=((0.0, 0.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0, 0.0))):
        self.matrix = matrix

    def fromBytes(data):
        matrix = Matrix()
        matrix[0] = struct.unpack("ffff", data[0:16])
        matrix[1] = struct.unpack("ffff", data[16:32])
        matrix[2] = struct.unpack("ffff", data[32:48])
        matrix[3] = struct.unpack("ffff", data[48:64])

        return matrix


class Vector4:
    def __init__(self, vector4=(0.0, 0.0, 0.0, 0.0)):
        self.vector4 = vector4

    def fromBytes(data):
        x, y, z, w = struct.unpack("ffff", data)
        return x, y, z, w


class Vector3:
    def __init__(self, vector3=(0.0, 0.0, 0.0)):
        self.vector3 = vector3

    def fromBytes(data):
        x, y, z = struct.unpack("fff", data)
        return x, y, z

def StripToTriangle(triangleStripList):
    faces = []
    cte = 0
    for i in range(2, len(triangleStripList)):
        if triangleStripList[i] == 65535 or triangleStripList[i - 1] == 65535 or triangleStripList[i - 2] == 65535:
            if i % 2 == 0:
                cte = -1
            else:
                cte = 0
            pass
        else:
            if (i + cte) % 2 == 0:
                a = triangleStripList[i - 2]
                b = triangleStripList[i - 1]
                c = triangleStripList[i]
            else:
                a = triangleStripList[i - 1]
                b = triangleStripList[i - 2]
                c = triangleStripList[i]

            if a != b and b != c and c != a:
                faces.append([a, b, c])
    return faces