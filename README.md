# efo_BlenderAddons

A Blender addon 2.8+ to import .efo from Initial D Arcade Stage (I mainly tested the .efo from Initial D Arcade Stage Zero, but it should work with the versions 5 to 8).

## NOTES

To get the correct materials of a car, you will to import a .efo from the folder **COLORS** first.

In order to port the gallery and the trees correctly, you will need the folder named **path**. The folders need to be like it was originally in the game folder. 

* For the trees :
  * /(name of the course)/efo
  * /(name of the course)/path
  
* For the gallery :
   * /common/
   * /(name of the course)/efo
   * /(name of the course)/path

## TO DO (not interested in the moment)

* Add support for the animations of characters (.edo)
* Rework the shaders
* Make a import all .efo for the cars (?)
* Add support for binormals and tangents for the course

## List of models with problems

* Sayuki2.efo is the same model as Sayuki.efo
* Gallery of Dry (Summer) and Ran (Summer) need to be scaled to with a factor of 4.5 (
* AE86T2_Window_genuine_00.efo has broken normals, which is probably normal since you can't see it due to shader used in the game
* (to add)

## Codes that helped me

[DGIorio Blender addons](https://drive.google.com/drive/folders/10DGQFPF6aeco2tUxp6MBfSidR-8lhNxe)



