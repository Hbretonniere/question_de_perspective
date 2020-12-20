import csv
import bpy
import numpy as np

bpy.ops.render.render(write_still=True)
file = csv.reader(open("data/list_objects/list_cube_smiley.csv"))
cube_mat = bpy.data.materials['cube_material']

for i, line in enumerate(file):
    bpy.ops.mesh.primitive_cube_add(size=float(line[3])/4, location=(float(line[1])/4, float(line[2])/4, float(line[0])/4))
    cube_i = bpy.context.selected_objects[0]
    cube_i.name = 'cube_{}'.format(i)
    cube_i.data.materials.append(cube_mat)


if bpy.context.object.mode == 'EDIT':
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

scene = bpy.data.scenes["Scene"]

nb_frames = 10
fov = 200.0
scene.camera.rotation_mode = 'XYZ'

rxs = np.linspace(75, 85, nb_frames)*np.pi/180
ry = 0
rzs = np.linspace(np.pi+np.pi/6, 2*np.pi, nb_frames)
scene.camera.rotation_euler[1] = ry

zs = np.linspace(7, 3, nb_frames)

frame = 0
ymax = 25
ymin = -10
for i, angle in enumerate(np.linspace(np.pi+np.pi/6, 2*np.pi, nb_frames)):
    frame += 1
    y = (ymax+ymin)+ymax*np.cos(angle+np.pi)
    x = 25*np.sin(angle)

    # Set camera rotation in euler angles
    rz = rzs[i]
    scene.camera.rotation_euler[2] = rz
    scene.camera.rotation_euler[0] = rxs[i]


    # Set camera translation
    scene.camera.location.z = zs[i]
    scene.camera.location.y = y
    scene.camera.location.x = x
    bpy.context.scene.render.filepath = './data/rendered/frame_{}'.format(frame)
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)

nb_frames_tr = 5
zs_tr = np.linspace(3, 0, nb_frames_tr)
rxs_tr = np.linspace(85, 90, nb_frames_tr)*np.pi/180

for i, y in enumerate(np.linspace(ymin, 0, nb_frames_tr)):
    frame += 1
    scene.camera.location.y = y
    scene.camera.location.z = zs_tr[i]
    scene.camera.rotation_euler[0] = rxs_tr[i]

    bpy.context.scene.render.filepath = './data/rendered/frame_{}'.format(frame)
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
