from .Utilities import *

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
            matrix = []
            for j in range(0, 12):
                matrix.append(binaryReader.readFloat())

            translation = (matrix[0], -matrix[2], matrix[1])
            mesh_index = matrix[3]
            rotation = (matrix[10], matrix[7], matrix[8], matrix[9])
            scale = matrix[11]
            
            self.list.append((mesh_index, translation, rotation, scale))