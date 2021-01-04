import os
import csv
import bpy
import numpy as np
import sys

nargv = len(sys.argv) - 1
nb_frames = int(sys.argv[nargv])
name = sys.argv[nargv-1]
bpy.ops.render.render(write_still=True)
file = np.load("data/list_objects/list_cube_"+name+".npy", allow_pickle=True)

# from normal scale to blender scale
reduce = file[0][0]

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

rxs = np.linspace(70, 85, nb_frames)*np.pi/180
ry = 0
rzs = np.linspace(np.pi+np.pi/6, 2*np.pi, nb_frames)
scene.camera.rotation_euler[1] = ry

zs = np.linspace(6, 2, nb_frames)

frame = 0
ymax = 40
ymin = -2
for i, angle in enumerate(np.linspace(np.pi+np.pi/6, 2*np.pi, nb_frames)):
    frame += 1
    y = ymax*np.cos(angle+np.pi)
    x = 18*np.sin(angle)

    # Set camera rotation in euler angles
    rz = rzs[i]
    scene.camera.rotation_euler[2] = rz
    scene.camera.rotation_euler[0] = rxs[i]


    # Set camera translation
    scene.camera.location.z = zs[i]
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
rxs_tr = np.linspace(85, 90, nb_frames_tr)*np.pi/180

for i, y in enumerate(np.linspace(ymin, 0, nb_frames_tr)):
    frame += 1
    scene.camera.location.y = y
    scene.camera.location.z = zs_tr[i]
    scene.camera.rotation_euler[0] = rxs_tr[i]

    bpy.context.scene.render.filepath = './data/rendered/'+name+'/'+name+'_frame_{}'.format(frame)
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
