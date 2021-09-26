# efo_BlenderAddons

![Akina Lake](https://i.imgur.com/9hStcZR.png)

A Blender addon 2.8+ to import .efo from Initial D Arcade Stage (I mainly tested the .efo from Initial D Arcade Stage Zero, but it should work with the versions 5 to 8). This addon can be also used to import trees and spectators (.pa8)

P.S : This is a script that is focused in importing the models like in **CAR**, **CHARACTERS** and **COURSE**. I haven't done a lot of testing in the .efo that are present in the **ACROBATA** and others folders.

## NOTES

To get the correct materials of a car, you will to import a .efo from the folder **COLORS** first.

In order to port the gallery and the trees correctly, you will need the folder named **path**. The folders need to be like it was originally in the game folder. 

* For the trees :
  * (your folder)/(name of the course)/efo
  * (your folder)/(name of the course)/path
  
* For the gallery :
   * (your folder)/common/
   * (your folder)/(name of the course)/efo
   * (your folder)/(name of the course)/path

## OTHERS

* **IMPORTING A MAP TAKE A LOT OF MEMORY (up to 1-4GB depending on the map)**
* The gallery doesn't use rotations. In the game, they turn according to where the camera is.
* For the characters, there isn't any bones for the mouths and hands, the game use different models for the expressions and gestures. However, the expressions doesn't have any UV so that's why there is only one face textured for the characters. I don't know how they did it.

## TO DO (not interested in the moment)

(To most likely to least likely)

* Add automatic reposition for mesh with locators (i.e : Mufflers and drivers)
* Fix Miki bone weights (let's be honest, nobody like him anyways lol)
* Add support for other paths
* Add support for binormals and tangents for the courses (This would at the top, but I don't know if Blender support the assignement of binormals and tangents)
* Rework the materials (I didn't use all the properties, but Blender is missing some/are different than the one used in the game) 
* Make a import all .efo for the cars
* Add support for the animations of characters (.edo) (Never worked with animations, that why it's way down here)
* Rework the shaders (The game use shaders that are probably impossible to re-create in Blender)

## Errors that need to be fixed in the script

* Miki bone weights and indices are wrong

## Errors that are normal

* Sayuki2.efo is the same model as Sayuki.efo
* Gallery of Dry (Summer) and Rain (Summer) need to be scaled to with a factor of 4.5 (Select all the objets from the gallery parent and then [scale them by using the individual origin option](https://www.youtube.com/watch?v=Q_EsYIJy-vA&t=89s))
* AE86T2_Window_genuine_00.efo has broken normals, which is probably normal since you can't see it due to shader used in the game
* If you import a map, you will see it will have weird black thingy on some part, this is normal because of the alpha channel (i.e : Nagao)
* (to add)

## Codes that helped me

[DGIorio Blender addons](https://drive.google.com/drive/folders/10DGQFPF6aeco2tUxp6MBfSidR-8lhNxe)




