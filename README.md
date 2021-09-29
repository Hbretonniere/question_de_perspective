# What is question de perspective ? :

It's a project that creates a random 3D projection of any image you want, and then create a scene and a video where you
see the perspective illusion become real !

 For example, let's take this Mondrian painting :

<img src="./data/for_readme/mondrian.png" alt="Mondrian" width="200">

The project will decompose each pixel to a cube and create this random looking disposition:

![perspective](./data/for_readme/perspective_mondrian.png)

But as you moves around the cubes, the illusion slowly disappear : when it comes to the perfect point, represented
as a black ring, all the cubes get perfectly aligned and reveal the image :

![gif](./data/for_readme/gif_mondrian.gif)

You can also draw you own pixel art masterpiece and automaticaly "perspective" it to the museum !

This project has been developped from scratch, only in python & blender. This python & blender only constrain was challenging, which sometimes constrains me to reinvent the wheel, but that's where the fun lies...


```diff
- Just follow the instructions of the menu, by launching "python menu.py"
```


```diff
- PLEASE READ THE NEXT OF THE README FOR MORE INFO ABOUT THE DEPENDENCIES!
```
# Dependencies
To be sure to have all the dependencies, you can create a conda environment using :

`conda env create -f env.yml`
 
 And then do `conda activate perspective`

Otherwise, the project doesn't require much libraries, and they are all quite common. You can easily pip install them
manually.

```diff
- You also need to install Blender :
```
https://www.blender.org/download/