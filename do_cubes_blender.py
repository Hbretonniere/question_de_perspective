'''
This script will be run by blender using the python 
interface API (https://docs.blender.org/api/current/info_overview.html).
It allows us to create a scene with the cubes in perspective. To
have a nice view, it creates the cubes from the list calculated in
do_cubes.py directly in a scene already made (museum.blend).
Then, we use the API to create the frames of the final video,
by moving the camera around the cubes following a 3d ellipse,
and rendering the scene at each step.

The video will be assembled in do_video.py

@author: Hubert Bretonnière

'''

import os
import bpy
import numpy as np
import sys
sys.path.insert(0,'./')

from blender_utils import full_screen, starting_position

''' initialisation '''

nargv = len(sys.argv) - 1
max_pixels = int(sys.argv[nargv])
# nb_frames = int(sys.argv[nargv-1])
image_name = sys.argv[nargv-1]
list_cubes = np.load("data/list_objects/list_cube_"+image_name+"-"+str(max_pixels)+".npy", allow_pickle=True)

bpy.ops.render.render(write_still=True)

# from normal scale to blender scale
reduce = 12

# We will save the images in a folder with the name of the original image
if not os.path.exists('data/rendered/'+image_name):
    os.makedirs('data/rendered/'+image_name)

''' =======================
    Creation of the cubes
    ========================
We loop for all the cubes of the list, and create a blender cube object,
with the right position and size. We rename it, and change its color by
creating a new blender material
To do : re-use a material if the color has been already seen'''
#+38

for i in range(2, list_cubes.shape[0]):
    bpy.ops.mesh.primitive_cube_add(size=float(list_cubes[i][3])/reduce,
                                    location=(float(list_cubes[i][1])/reduce,
                                    float(list_cubes[i][2])/reduce,
                                    float(list_cubes[i][0])/reduce))

    cube_i = bpy.context.selected_objects[0]
    cube_i.name = 'cube_{}'.format(i)
    color = tuple(reversed(tuple(list_cubes[i][4]/255)))+(1,)
    cube_mat = bpy.data.materials.new("RGB")
    cube_mat.diffuse_color = color
    cube_mat.roughness = 1  # make the material less shiny
    cube_i.data.materials.append(cube_mat)

context = bpy.context.copy()

full_screen()
starting_position()
