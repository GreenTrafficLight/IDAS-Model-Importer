import struct
from mathutils import *

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

class Matrix4x3:
    def __init__(self, matrix=((0.0, 0.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0, 0.0))):
        self.matrix = matrix

    def fromBytes(data):
        matrix = Matrix()
        matrix[0] = struct.unpack("ffff", data[0:16])
        matrix[1] = struct.unpack("ffff", data[16:32])
        matrix[2] = struct.unpack("ffff", data[32:48])

        return matrix

class Matrix3x3:
    def __init__(self, matrix=((0.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0),
                               (0.0, 0.0, 0.0))):
        self.matrix = matrix

    def fromBytes(data):
        matrix = Matrix.Identity(3)
        matrix[0] = struct.unpack("fff", data[0:12])
        matrix[1] = struct.unpack("fff", data[12:24])
        matrix[2] = struct.unpack("fff", data[24:36])

        return matrix