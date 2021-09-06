import struct
from mathutils import *

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