# What is question de perspective ? :

It's a project that creates a random 3D projection of any image you want, and then create a scene and a video where you
see the perspective illusion become real !

 For example, lets take this Mondrian painting :

<img src="./data/for_readme/mondrian.png" alt="Mondrian" width="200">

The project will decompose each pixel to a cube and create this random looking disposition :

![perspective](./data/for_readme/perspective_mondrian.png)

But as the camera rotates around the cubes, the illusion slowly disappear : when it comes to the perfect point, represented
as a black ring, al the cubes get perfectly aligned and reveal the input image :

![gif](./data/for_readme/gif_mondrian.gif)

You can also create your own pixel art using the following command at the root of the project :

`ipython pixel_art.py` 

It will create a a blanck pixel art canvas, along with a color palette. You can now click on the color palette, and then 
paint it in the canvas !
When you're happy with your masterpiece, you can right click (or ctrl click) to save it, and even directly launch the rendering of the animation by double clicking.

PLEASE READ THE NEXT OF THE README FOR MORE INFO ABOUT AN EXAMPLE AND THE DEPENDENCIES!
# Dependencies
To be sure to have all the dependencies, you can create a conda environment using :

`conda env create -f env.yml`

Otherwise, the project doesn't require too much libraries, and they are all quite common. You can easily pip install them
manually.

You also need to install Blender : https://www.blender.org/download/

# Run an example
To run the program, do :

`sh main.sh image nb_frames fps`

where :

image = file name of the image you want to put in perspective (for example smiley). It will search for original picture in data/images and search for image.png

`sh main.sh img nb_frames fps`

img = file name of the image you want to put in perspective (for example smiley). It will search for original picture in data/images and search as image.png


nb_frames = number of frames you want to render (for example 20)


fps = frame per second for the video (for example 10)

try it with the example : run 
`sh main.sh smiley 20 10`
at the root of the project
