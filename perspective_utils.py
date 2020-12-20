# -*- coding: utf-8 -*-
"""
Created on Fri May  1 15:18:40 2020

@author: Hubert Bretonnière
"""
from PIL import Image
from random import randint
import numpy as np


def make_list_cube(image, distance=35, depth_factor=2, pix_size=2):

    im = np.asarray(Image.open("data/images/"+image+str(".png")))  # Can be many different formats
    size_x = np.shape(im)[0]  # Get the width and hight of the image for iterating over
    size_y = np.shape(im)[1]
    list_cube = [[0, 0, 0, 0], [0, 0, 0, 0]]  # on initialise a avec deux lignes pour ne pas avoir de problemes de dimension dans la boucle
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
                new_a = [x, y, z, p]
                for s in range(1, size):
                    d = np.sqrt((x - (list_cube[s])[0])**2 + (y - (list_cube[s])[1])**2 + (z - (list_cube[s])[2])**2)
                    if float(d) < np.sqrt(2)*(r+(list_cube[s])[3]):  # if yes, cubes are intersecting then break
                        break
                    else:
                        continue
                list_cube = np.vstack([list_cube, new_a])
                size = size+1
    file_out = open("data/list_objects/list_cube_" + str(image) + ".csv", "w")
    for i in range(2, size+1):
        file_out.write(str((list_cube[i])[0])+','+str((list_cube[i])[1])+','+str((list_cube[i])[2])+','+str((list_cube[i])[3])+'\n')

    file_out.close
