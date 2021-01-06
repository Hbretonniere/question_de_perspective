import sys
import argparse
import numpy as np
import os
from PIL import Image
#from perspective_utils import make_list_cube

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
    if os.path.isfile("data/list_objects/list_cube_" + str(image) + ".npy"):
        print("List of cubes (data/list_objects/list_cube_"+str(image) + ".npy) "
                                                                         "already created, skipping")
    else:
        print("Creating list of cubes in", "data/list_objects/list_cube_" + str(image) + ".npy from ",
              "data/images/"+image+".png")
        im = np.asarray(Image.open("data/images/"+image+str(".png")),dtype=object)  # Can be many different formats
        if im.shape[2] == 4:  # We don't use the transparency of a RGBA image
            im = im[:, :, :3]

        ''' ======== Pre-processing======== '''
        ''' Because of projection issue, we need to flip vertically and horizontally the image'''
        im = np.flip(im)
        im = np.flip(im, axis=1)

        size_x = np.shape(im)[0]
        size_y = np.shape(im)[1]
        list_cube = [[np.shape(im)[1]*12, 0, 0, 0, 0], [0, 0, 0, 0, 0]] # initialize the list with shape infos
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
                    ''' We need do check that there is no conflict between the cubes (no intersection). 
                    To do so, for each new cube, we see if it's intersecting it. We retry a new random depth factor untill
                    we have no conflict. 
                    To do : There must be a more elegant way to do that... '''
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

#image = str(sys.argv[1])
parser = argparse.ArgumentParser()
parser.add_argument("--image_name", help="name of the image you want to put in perspective (for example smiley.\
                        It will search for original picture in data/images and search as image.png", type=str)
args = parser.parse_args()
make_list_cube(args.image_name)
