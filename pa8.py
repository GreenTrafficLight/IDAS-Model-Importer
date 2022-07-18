from cgi import test
from .Utilities import *

from math import *
from mathutils import *

class PA:
    def __init__(self, filepath):
        pa_file = open(filepath, 'rb')
        binaryReader = BinaryReader(pa_file)

        self.list = []
        self.list2 = []

        header = binaryReader.bytesToString(binaryReader.readBytes(4))
        binaryReader.seek(4, 1)
        size = binaryReader.readUInt()
        count = binaryReader.readUInt()

        binaryReader.seek(16, 1)

        for i in range(count):
            values = []
            for j in range(0, 12):
                values.append(binaryReader.readFloat())

            rotation_matrix = Matrix.Identity(3)

            translation = (values[0], values[1], values[2])
            mesh_index = values[3]

            x_rotation = Matrix.Rotation(radians(values[8]), 3, 'X')
            y_rotation = Matrix.Rotation(radians(values[9]), 3, 'Y')
            z_rotation = Matrix.Rotation(radians(values[10]), 3, 'Z')
            euler_rotation_matrix = z_rotation @ x_rotation @ y_rotation
            
            #euler_rotation_matrix = Euler((radians(values[8]), radians(values[9]), radians(values[10])), 'XYZ').to_matrix()

            # y axis
            rotation_matrix[0][0] = values[6]
            rotation_matrix[0][2] = values[4]
            rotation_matrix[2][0] = -values[4]
            rotation_matrix[2][2] = values[6]

            rotation_matrix @= euler_rotation_matrix
            rotation_matrix = rotation_matrix.to_4x4()

            scale = values[11]
            
            self.list.append((mesh_index, translation, rotation_matrix, scale))