
# if bpy.context.object.mode == 'EDIT':
#     bpy.ops.object.mode_set(mode='OBJECT')
# bpy.ops.object.select_all(action='DESELECT')
''' ==============================
        Creation of the frames
    ==============================
The image is creating on the [x, z] plane, and the perspective is following the y axis. The perfect perspective is at
the origin (0,0,0)
To do a nice video, we want to move the camera around the cubes, from the back to the final position.
To do so, we move the camera along half an ellipse from behind the cubes (ymax=25) to a bit behind the cube (ymin=-5)
We rotate the facing direction of the camera along the z axis so it always faces the cubes during the movement.
We also incline a bit the ellipse by changing the height of the camera (z=6 to z=2), and rotating it a bit
along the x axis so it faces the cubes.
Finally, we add a last translation from a point a bit behind and above the 0 point to the zero point to have
the perfect perspective.
'''

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
# parser = argparse.ArgumentParser()
# parser.add_argument("--image_name", help="name of the image you want to put in perspective (for example "
#                                         "smiley.jpg)", type=str)
# parser.add_argument("--nb_frames", help="number of frames you want to rendered (for example 20))",
#                    type=int)
# args = parser.parse_args()
# nb_frames = args.nb_frames
# image_name = args.image_name

nargv = len(sys.argv) - 1
max_pixels = int(sys.argv[nargv])
nb_frames = int(sys.argv[nargv-1])
image_name = sys.argv[nargv-2]
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

''' ====== Ellipse ======= '''
'''Initialisation of the camera movements'''

scene = bpy.data.scenes["Scene"]
fov = 200.0
scene.camera.rotation_mode = 'XYZ'

rot_x = np.linspace(75, 85, nb_frames)*np.pi/180  # begin facing a bit the floor and going to more parralle to the floor
rot_y = 0  # no rotation along the y axis
rot_z = np.linspace(180, 360, nb_frames)*np.pi/180  # from facing the wall behind to facing the cubes
scene.camera.rotation_euler[1] = rot_y

translat_z = np.linspace(6, 2, nb_frames)

frame = 0
ymax = 38
ymin = -15
xmax = 20
''' The (x,y) ellipse coordinates are parameterized by a single angle, from 360 to 180, with nb_frames steps'''

for i, angle in enumerate(np.linspace(2*np.pi, np.pi, nb_frames)):
    frame += 1
    frame_name = './data/rendered/'+image_name+'/'+image_name+'_max_pixels'+str(max_pixels)+\
                 '_frame_'+str(frame)
    if os.path.isfile(frame_name):
        print(frame_name,'already created, skipping')
    else:
        print('creating ', frame_name)
        y = (ymax+ymin)/2 + (ymax-ymin)/2*np.cos(angle)
        x = xmax*np.sin(angle)

        # Set camera rotation in euler angles
        scene.camera.rotation_euler[2] = rot_z[i]
        scene.camera.rotation_euler[0] = rot_x[i]

        # Set camera translation
        scene.camera.location.z = translat_z[i]
        scene.camera.location.y = y
        scene.camera.location.x = x

        # Render and save the current frame
        bpy.context.scene.render.filepath = frame_name
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.ops.render.render(write_still=True)

''' ====== Final Translations ======= '''
''' The number of steps is conditioned on the number used for the ellipse
To do : give better meaning of 'nb_frames' '''

if nb_frames > 16:
    nb_frames_tr = nb_frames/6
else:
    nb_frames_tr = 2

zs_tr = np.linspace(2, 0, nb_frames_tr)   # from a bit above to 0
rot_x = np.linspace(85, 90, nb_frames_tr)*np.pi/180  # from a bit facing the floor to parrallel to the flooor

for i, y in enumerate(np.linspace(ymin, 0, nb_frames_tr)):
    frame += 1
    frame_name = './data/rendered/'+image_name+'/'+image_name+'_max_pixels'+str(max_pixels)+\
                 '_frame_'+str(frame)
    if os.path.isfile(frame_name):
        print(frame_name, 'already created, skipping')
    else:
        print('creating', frame_name)
        scene.camera.location.y = y
        scene.camera.location.z = zs_tr[i]
        scene.camera.rotation_euler[0] = rot_x[i]
        bpy.context.scene.render.filepath = frame_name
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.ops.render.render(write_still=True)

cam = bpy.data.objects['Camera']
cam.location.x = 0
cam.location.y = 0
cam.location.z = 0
cam.rotation_euler[0] = 0
