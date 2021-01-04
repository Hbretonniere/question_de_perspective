import os
import bpy
import numpy as np
import sys

nargv = len(sys.argv) - 1 
nb_frames = int(sys.argv[nargv])
name = sys.argv[nargv-1]
file = np.load("data/list_objects/list_cube_"+name+".npy", allow_pickle=True)

bpy.ops.render.render(write_still=True)

# from normal scale to blender scale
reduce = 12

if not os.path.exists('data/rendered/'+name):
    os.makedirs('data/rendered/'+name)

print(reduce)
for i in range(2, file.shape[0]):
    if i == 0:
        continue
    bpy.ops.mesh.primitive_cube_add(size=float(file[i][3])/reduce, location=(float(file[i][1])/reduce, float(file[i][2])/reduce, float(file[i][0])/reduce))
    cube_i = bpy.context.selected_objects[0]
    cube_i.name = 'cube_{}'.format(i)
    color = tuple(reversed(tuple(file[i][4]/255)))+(1,)
    cube_mat = bpy.data.materials.new("RGB")
    cube_mat.diffuse_color = color
    cube_mat.roughness = 1
    cube_i.data.materials.append(cube_mat)


if bpy.context.object.mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

scene = bpy.data.scenes["Scene"]
fov = 200.0
scene.camera.rotation_mode = 'XYZ'

rot_x = np.linspace(75, 85, nb_frames)*np.pi/180  # from a bit to the floor to parallel
rot_y = 0
rot_z = np.linspace(180, 360, nb_frames)*np.pi/180  # from facing the wall behind to facing the cubes
scene.camera.rotation_euler[1] = rot_y

translat_z = np.linspace(6, 2, nb_frames)

frame = 0
ymax = 38
ymin = -10
xmax = 18
for i, angle in enumerate(np.linspace(np.pi, 0, nb_frames)):
    frame += 1
    y = (ymax+ymin)/2 + (ymax-ymin)/2*np.cos(angle+np.pi)
    x = xmax*np.sin(angle+np.pi)

    # Set camera rotation in euler angles
    scene.camera.rotation_euler[2] = rot_z[i]
    scene.camera.rotation_euler[0] = rot_x[i]

    # Set camera translation
    scene.camera.location.z = translat_z[i]
    scene.camera.location.y = y
    scene.camera.location.x = x
    bpy.context.scene.render.filepath = './data/rendered/'+name+'/'+name+'_frame_{}'.format(frame)
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)

if nb_frames > 16:
    nb_frames_tr = nb_frames/8
else:
    nb_frames_tr = 2
zs_tr = np.linspace(2, 0, nb_frames_tr)
rot_x_tr = np.linspace(85, 90, nb_frames_tr)*np.pi/180

for i, y in enumerate(np.linspace(ymin, 0, nb_frames_tr)):
    frame += 1
    scene.camera.location.y = y
    scene.camera.location.z = zs_tr[i]
    scene.camera.rotation_euler[0] = rot_x_tr[i]

    bpy.context.scene.render.filepath = './data/rendered/'+name+'/'+name+'_frame_{}'.format(frame)
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
