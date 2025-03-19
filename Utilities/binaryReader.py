import struct

import mathutils

class BinaryReader:

    def __init__(self, data, endian="<"):
        self.data = data
        self.endian = endian
        
        self.seek(0)

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

    def readVector3f(self):
        x, y, z = struct.unpack(self.endian + "fff", self.read(12))
        return x, y, z
    
    def readVector4f(self):
        x, y, z, w = struct.unpack(self.endian + "ffff", self.read(16))
        return x, y, z, w

    def readMatrix4x4(self):
        matrix = []
        matrix.append(struct.unpack(self.endian + "ffff", self.read(16)))
        matrix.append(struct.unpack(self.endian + "ffff", self.read(16)))
        matrix.append(struct.unpack(self.endian + "ffff", self.read(16)))
        matrix.append(struct.unpack(self.endian + "ffff", self.read(16)))
        return matrix
    
    def readMatrix3x4(self):
        matrix = []
        matrix.append(struct.unpack(self.endian + "ffff", self.read(16)))
        matrix.append(struct.unpack(self.endian + "ffff", self.read(16)))
        matrix.append(struct.unpack(self.endian + "ffff", self.read(16)))
        return matrix

    def readMatrix3x3(self):
        matrix = []
        matrix.append(struct.unpack(self.endian + "fff", self.read(12)))
        matrix.append(struct.unpack(self.endian + "fff", self.read(12)))
        matrix.append(struct.unpack(self.endian + "fff", self.read(12)))
        return matrix

    def bytesToString(self, byteArray, encoding="utf-8"):
        try:
            return byteArray.decode(encoding)
        except:
            string = ""
            for b in byteArray:
                if b < 127:
                    string += chr(b)
            return string