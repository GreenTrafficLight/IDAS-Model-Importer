# efo_BlenderAddons

![Akina Lake](https://i.imgur.com/9hStcZR.png)

A Blender addon 2.8+ to import .efo from Initial D Arcade Stage (I mainly tested the .efo from Initial D Arcade Stage Zero, but it should work with the versions 5 to 8). This addon can be also used to import trees and spectators (.pa8)

P.S : This is a script that is focused in importing the models like in **CAR**, **CHARACTERS** and **COURSE**. I haven't done a lot of testing in the .efo that are present in the **ACROBATA** and others folders.

## NOTES

* **IMPORTING A MAP TAKE A LOT OF MEMORY (up to 1-4GB of memory depending on the map)**
* To get the correct materials of a car, you will to import a .efo from the folder **COLORS** first.
* The gallery doesn't use rotations. In the game, they turn according to where the camera is.
* Some models can have black parts, it means it's double faced
* Sayuki2.efo is the same model as Sayuki.efo
* Gallery of Dry (Summer) and Rain (Summer) need to have a scale of 4.5 (Select all the objets from the gallery parent and then [scale them by using the individual origin option](https://www.youtube.com/watch?v=Q_EsYIJy-vA&t=89s))
* If you import a map, you will see it will have weird black thingy on some part, this is normal because of the alpha channel (i.e : Nagao)

## IMPORTING TREES/GALLERY

In order to port the gallery and the trees correctly, you will need the folder named **path**. The folders need to be like it was originally in the game folder. 

* For the trees :
  * (your folder)/(name of the course)/efo
  * (your folder)/(name of the course)/path
  
* For the gallery :
   * (your folder)/common/
   * (your folder)/(name of the course)/efo
   * (your folder)/(name of the course)/path

## TO DO

* Add automatic reposition for mesh with locators (i.e : Mufflers and drivers)
* Fix Miki bone weights
* Add support for other paths
* Add support for binormals and tangents for the courses (This would at the top, but I don't know if Blender support the assignement of binormals and tangents)
* Add support for the animations of characters (.edo)

## Errors that need to be fixed

* Miki bone weights and indices are wrong






