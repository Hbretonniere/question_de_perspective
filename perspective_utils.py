# -*- coding: utf-8 -*-
"""
Created on Fri May  1 15:18:40 2020

@author: Hubert Bretonnière
"""
from PIL import Image
import numpy as np
import moviepy.video.io.ImageSequenceClip
import re
import glob


def sort_nicely(liste):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    liste.sort(key=alphanum_key)
    return liste


def get_hex_color(x):
    r = max(0, min(x[0], 255))
    g = max(0, min(x[1], 255))
    b = max(0, min(x[2], 255))
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


def make_list_cube(image, distance=70, depth_factor=3, pix_size=2):

    im = np.asarray(Image.open("data/images/"+image+str(".png")))  # Can be many different formats
    if im.shape[2] == 4:
        im = im[:, :, :3]
    im = np.flip(im)
    im = np.flip(im, axis=1)
    size_x = np.shape(im)[0]  # Get the width and hight of the image for iterating over
    size_y = np.shape(im)[1]
    list_cube = [[np.shape(im)[1]/13*4, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    print(list_cube)
    size = 1
    # parcourt pixel de l'image reelle
    for x0 in range(0, size_x):
        for y0 in range(0, size_y):
            if list(im[x0, y0]) != [255, 255, 255]:
                r = np.random.uniform(1, depth_factor)  # randint(100, 300)/100. #r=facteur de reduction aleatoire (entre 100 et 300% de la taille du pixel de base)
                x = r * (x0 - float(size_x) / 2.)
                y = r * (y0 - float(size_y) / 2.)
                z = r * distance
                p = float(r) * pix_size / 2.
                c = im[x0, y0]
                new_a = [x, y, z, p, c]
                for s in range(1, size):
                    d = np.sqrt((x - (list_cube[s])[0])**2 + (y - (list_cube[s])[1])**2 + (z - (list_cube[s])[2])**2)
                    if float(d) < np.sqrt(2)*(r+(list_cube[s])[3]):  # if yes, cubes are intersecting then break
                        break
                    else:
                        continue
                list_cube = np.vstack([list_cube, new_a])
                size = size+1
    np.save("data/list_objects/list_cube_" + str(image) + ".npy", list_cube)


def make_movie(name, fps):
    image_files = [img for img in sort_nicely(glob.glob('data/rendered/'+name+'*.png'))]
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile('data/rendered/'+name+'_video.mp4')
