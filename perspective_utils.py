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
    ''' sort list of string combining letters and numbers.
    adapted from https://gist.github.com/limed/473a498641bbc7761a20 '''

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    liste.sort(key=alphanum_key)
    return liste


def get_hex_color(x):
    'Transform a RBG color to its hexadecimal code'
    r = max(0, min(x[0], 255))
    g = max(0, min(x[1], 255))
    b = max(0, min(x[2], 255))
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


def make_list_cube(image, distance=70, depth_factor=3, pix_size=2):
    ''' 
    Creates a list of cubes in perspective representing an input 2D image.
    Args : 
            - image : a png or jpeg RGB (or RGBA) image
            - distance : the distance of the closest cube from the zero point perspective.
                         Need to be big enough for the image to be completely in the field
                         of view at the 0 point perspective
            - depth_factor : the maximum ratio between the closest and the farest cube distance.
                             ( or similarly between the min and max sizes of the cubes)
            - pix_size : The smallest size of the cubes. ( I think it need to be hard coded)
    Returns :
            - a numpy array containing for each non white pixel of the input image
              the (x, y, z) coordinates and its size (bigger if farther, smaller if closer)
              along with its RGB color.
              Also save the array to a .npy file with the name of the image.
    '''

    im = np.asarray(Image.open("data/images/"+image+str(".png")))  # Can be many different formats

    if im.shape[2] == 4:  # We don't use the transparency of a RGBA image
        im = im[:, :, :3]

    ''' ======== Pre-processing======== '''
    ''' Because of projection issue, we need to flip vertically and horizontaly the image'''
    im = np.flip(im)
    im = np.flip(im, axis=1)

    size_x = np.shape(im)[0]  
    size_y = np.shape(im)[1]
    list_cube = [[np.shape(im)[1]*12, 0, 0, 0, 0], [0, 0, 0, 0, 0]] # intialize the list with shape infos
    nb_cubes = 1

    ''' ======== Creation of the perspective ========= '''
    ''' We iterate through all the pixels, along x and y'''
    for x0 in range(0, size_x):
        for y0 in range(0, size_y):
            if list(im[x0, y0]) != [255, 255, 255]:  # continue if the pixel is white
                r = np.random.uniform(1, depth_factor) # random depth factor for the current pixel
                ''' The 3D coordinates and the size of the cube are conditionned to the depth factor '''
                x = r * (x0 - float(size_x) / 2.)
                y = r * (y0 - float(size_y) / 2.)
                z = r * distance
                p = float(r) * pix_size / 2.  # size of the cube (side)
                c = im[x0, y0]
                cube = [x, y, z, p, c]
                ''' We need do check that there is no conflict between the cubes (no interscetion). 
                To do so, for each new cube, we see if it's intersecting it. We retry a new random depth factor untill
                we have no conflict. 
                To do : Is must have a more elegant way to do that... '''
                for s in range(1, nb_cubes):
                    d = np.sqrt((x - (list_cube[s])[0])**2 + (y - (list_cube[s])[1])**2 + (z - (list_cube[s])[2])**2)
                    if float(d) < np.sqrt(2)*(r+(list_cube[s])[3]):  # if yes, cubes are intersecting then break
                        break
                    else:
                        continue
                list_cube = np.vstack([list_cube, cube])
                nb_cubes += 1
    np.save("data/list_objects/list_cube_" + str(image) + ".npy", list_cube)
    return list_cube


def make_movie(name, fps):
    ''' Creates a video from frames'''
    image_files = [img for img in sort_nicely(glob.glob('data/rendered/'+name+'/'+name+'*.png'))]
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile('data/rendered/'+name+'/'+name+'_video.mp4')
