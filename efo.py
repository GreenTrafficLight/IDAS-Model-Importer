from os import system
from mathutils import *
from .Resource import *
from .Utilities import *

class EFO:
    
    def __init__(self, filepath):
        efo_file = open(filepath, 'rb')
        binaryReader = BinaryReader(efo_file)

        self._sSceneDatabase = sSceneDatabase(binaryReader)
        print(binaryReader.tell())
        
        if "_sSerial::_sShapeHeader" in self._sSceneDatabase._sSerial:

            for shapeHeader in self._sSceneDatabase.shapeHeaderSignatures:
                
                _sShapeHeader = sShapeHeader(binaryReader, self._sSceneDatabase)
                print(binaryReader.tell())
                self._sSceneDatabase.shapeHeader[shapeHeader] = _sShapeHeader

                for shape in _sShapeHeader.shape:
                    
                    _sShape = sShape(binaryReader, self._sSceneDatabase)
                    print(binaryReader.tell())
                    #_sShapeHeader.shapeDic[shape] = _sShape
                    self._sSceneDatabase.shape[shape] = _sShape

                    if _sShape.state not in self._sSceneDatabase.state:
                        _sState = sState(binaryReader, self._sSceneDatabase)
                        print(binaryReader.tell())
                        self._sSceneDatabase.state[_sShape.state] = _sState


                    for texture in _sState.texture:

                        if texture not in self._sSceneDatabase.texture:
                            _sTexture = sTexture(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            self._sSceneDatabase.texture[texture] = _sTexture
                            
                            if _sTexture.textureImage > 0 and _sTexture.textureImage not in self._sSceneDatabase.textureImage:

                                _sTextureImage = sTextureImage(binaryReader, self._sSceneDatabase)
                                print(binaryReader.tell())
                                self._sSceneDatabase.textureImage[_sTexture.textureImage] = _sTextureImage

                            elif _sTexture.textureImage < 0:

                                self._sSceneDatabase.textureImage[_sTexture.textureImage] = None


                    if _sShape.displayList not in self._sSceneDatabase.displayList:
                    
                        _sDisplayList = sDisplayList(binaryReader, self._sSceneDatabase)
                        print(binaryReader.tell())
                        self._sSceneDatabase.displayList[_sShape.displayList] = _sDisplayList

                        if _sDisplayList.geometry not in self._sSceneDatabase.geometry:
                            
                            _sGeometry = sGeometry(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            self._sSceneDatabase.geometry[_sDisplayList.geometry] = _sGeometry

                            _sVertexArray = sGeometry.sVertexArray(binaryReader, _sGeometry)
                            print(binaryReader.tell())
                            self._sSceneDatabase.vertexArray[_sGeometry.vertexArray] = _sVertexArray

                        _sPrimitiveList = sShape.sPrimitiveList(binaryReader, self._sSceneDatabase)
                        print(binaryReader.tell())
                        self._sSceneDatabase.primitiveList[_sDisplayList.primitiveList[0]] = _sPrimitiveList

                        # ???
                        binaryReader.readBytes(binaryReader.readUInt())
                        binaryReader.readBytes(binaryReader.readUInt())

                        # TEST
                        for blendGeometry in _sDisplayList.blendGeometry:

                            _sGeometry = sGeometry(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            _sDisplayList.blendGeometry[blendGeometry] = _sGeometry

                            _sVertexArray = sGeometry.sVertexArray(binaryReader, _sGeometry)
                            print(binaryReader.tell())
                            self._sSceneDatabase.vertexArray[_sGeometry.vertexArray] = _sVertexArray


                        print(binaryReader.tell())

                        if _sShape.displayList != self._sSceneDatabase.displayListSignatures[0] and self._sSceneDatabase.displayListSignatures[0] not in self._sSceneDatabase.displayList:

                            _sDisplayList = sDisplayList(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            self._sSceneDatabase.displayList[self._sSceneDatabase.displayListSignatures[0]] = _sDisplayList

                            if _sDisplayList.geometry not in self._sSceneDatabase.geometry:
                                
                                _sGeometry = sGeometry(binaryReader, self._sSceneDatabase)
                                print(binaryReader.tell())
                                self._sSceneDatabase.geometry[_sDisplayList.geometry] = _sGeometry
                                
                                _sVertexArray = sGeometry.sVertexArray(binaryReader, _sGeometry)
                                print(binaryReader.tell())
                                self._sSceneDatabase.vertexArray[_sGeometry.vertexArray] = _sVertexArray

                            _sPrimitiveList = sShape.sPrimitiveList(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            self._sSceneDatabase.primitiveList[_sDisplayList.primitiveList[0]] = _sPrimitiveList

                            # ???
                            binaryReader.readBytes(binaryReader.readUInt())
                            binaryReader.readBytes(binaryReader.readUInt())
                            
                            print(binaryReader.tell())
            
                print(binaryReader.tell())

            print(binaryReader.tell())

            # TEST for characters
            for stateSignature in self._sSceneDatabase.stateSignatures:

                if stateSignature not in self._sSceneDatabase.state:

                    _sState = sState(binaryReader, self._sSceneDatabase)
                    print(binaryReader.tell())
                    self._sSceneDatabase.state[_sShape.state] = _sState

                    for texture in _sState.texture:
                        
                        if texture not in self._sSceneDatabase.texture:
                            
                            _sTexture = sTexture(binaryReader, self._sSceneDatabase)
                            print(binaryReader.tell())
                            self._sSceneDatabase.texture[texture] = _sTexture

                            if _sTexture.textureImage > 0 and _sTexture.textureImage not in self._sSceneDatabase.textureImage:

                                _sTextureImage = sTextureImage(binaryReader, self._sSceneDatabase)
                                print(binaryReader.tell())
                                self._sSceneDatabase.textureImage[_sTexture.textureImage] = _sTextureImage

            print(binaryReader.tell())

            # TEST for characters
            for textureSignature in self._sSceneDatabase.textureSignatures:

                if textureSignature not in self._sSceneDatabase.texture:
                    
                    _sTexture = sTexture(binaryReader, self._sSceneDatabase)
                    print(binaryReader.tell())
                    self._sSceneDatabase.texture[textureSignature] = _sTexture

                    if _sTexture.textureImage > 0 and _sTexture.textureImage not in self._sSceneDatabase.textureImage:

                        _sTextureImage = sTextureImage(binaryReader, self._sSceneDatabase)
                        print(binaryReader.tell())
                        self._sSceneDatabase.textureImage[_sTexture.textureImage] = _sTextureImage                

            print(binaryReader.tell())

            for skeleton in self._sSceneDatabase.skeletonSignatures:

                _sSkeleton = sSkeleton(binaryReader)
                print(binaryReader.tell())
                self._sSceneDatabase.skeleton[skeleton] = _sSkeleton

                for bone in _sSkeleton.bone:

                    _sSbone = sBone(binaryReader, self._sSceneDatabase)
                    print(binaryReader.tell())
                    self._sSceneDatabase.bone[bone] = _sSbone
                    _sSkeleton.boneDic[bone] = _sSbone

            print(binaryReader.tell())

        else:
            
            if self._sSceneDatabase.textureImageSignatures != [] and self._sSceneDatabase.textureSignatures != [] :
                
                if self._sSceneDatabase.textureImageSignatures[0] < self._sSceneDatabase.textureSignatures[0]:

                    for textureSignature in self._sSceneDatabase.textureSignatures:

                        if textureSignature not in self._sSceneDatabase.texture:

                            _sTextureImage = sTextureImage(binaryReader, self._sSceneDatabase)

                            _sTexture = sTexture(binaryReader, self._sSceneDatabase)
                            self._sSceneDatabase.texture[textureSignature] = _sTexture

                            self._sSceneDatabase.textureImage[_sTexture.textureImage] = _sTextureImage

                elif self._sSceneDatabase.textureSignatures[0] < self._sSceneDatabase.textureImageSignatures[0]:

                    for textureSignature in self._sSceneDatabase.textureSignatures:

                        if textureSignature not in self._sSceneDatabase.texture:
                            
                            _sTexture = sTexture(binaryReader, self._sSceneDatabase)
                            self._sSceneDatabase.texture[textureSignature] = _sTexture

                            if _sTexture.textureImage > 0 and _sTexture.textureImage not in self._sSceneDatabase.textureImage:

                                _sTextureImage = sTextureImage(binaryReader, self._sSceneDatabase)
                                self._sSceneDatabase.textureImage[_sTexture.textureImage] = _sTextureImage

            else:
            
                for textureImageSignature in self._sSceneDatabase.textureImageSignatures:
                        
                    _sTextureImage = sTextureImage(binaryReader, self._sSceneDatabase)
                    self._sSceneDatabase.textureImage[textureImageSignature] = _sTextureImage

    def read_sShapeHeader(sSceneDatabase, shapeHeader):
        _sShapeHeader = sShapeHeader(binaryReader)
        sSceneDatabase.shapeHeader[shapeHeader] = _sShapeHeader