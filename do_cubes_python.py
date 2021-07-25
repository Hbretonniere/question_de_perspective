import sys
import argparse
import numpy as np
import os
from PIL import Image


def reduce_image(image, max_pixels):
    '''
    :param image: 
    :return: image
    if image (as np array) is bigger than max_pixels, reduce it, preserving x/y ratio
    '''

    global new_image
    print(max_pixels, "max_pixels")
    reduction = int(np.sqrt((image.size[0]*image.size[1])/max_pixels))
    new_x = int(image.size[0]/reduction)
    new_y = int(image.size[1]/reduction)
    print("Original image too big (", image.size[0]*image.size[1], "=",
          image.size[0], "x", image.size[1],
          "), compared to max authorized", max_pixels, ". Reducing it to ", new_x, ", ", new_y, ".")
    new_image = image.resize((new_x, new_y), Image.ANTIALIAS)
    return(new_image)


def make_list_cube(image, overwrite, max_pixels, distance=70, depth_factor=3, pix_size=2):
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
    if os.path.isfile("data/list_objects/list_cube_" + str(image) + ".npy") and not overwrite:
        print("List of cubes (data/list_objects/list_cube_"+str(image) + ".npy already \
there and overwrite set to False. Skipping")
    else:
        final_npy = "data/list_objects/list_cube_" + str(image) + "-" + str(max_pixels) + ".npy"
        print("Creating list of cubes in", "data/list_objects/list_cube_" + str(image) + ".npy from ",
              "data/images/"+image+".png")

        im = Image.open("data/images/"+image+str(".png"))  # Can be many different formats
        print("im.size", im.size)
        if int(im.size[0]*im.size[1]) > max_pixels:
            reduce_image(im, max_pixels)
            im = new_image
        im = np.asarray(im, dtype=object)
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
                    r = np.random.uniform(1, depth_factor)  # random depth factor for the current pixel
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
        np.save(final_npy, list_cube)
        return list_cube


def find_available(image):
    indices = np.where(image != [255, 255, 255])

    available = []
    for i in indices:
        available = available + list(i)
    return(available[::2])


def make_list_cube_3D(images, overwrite=True, max_pixels=100, distance=70, pix_size=2):
    '''
    Creates a list of cubes in perspective representing an input 2D image.
    Args :
            - images : a list of 2 pngs or jpegs RGB (or RGBA) images
            - distance : the distance of the closest cube from the zero point perspective.
                         Need to be big enough for the image to be completely in the field
                         of view at the 0 point perspective
        
            - pix_size : The smallest size of the cubes. ( I think it need to be hard coded)
    Returns :
            - a numpy array containing for each non white pixel of the input image
              the (x, y, z) coordinates and its size (bigger if farther, smaller if closer)
              along with its RGB color.
              Also save the array to a .npy file with the name of the image.
    '''

    # IMAGE 1
    im1 = Image.open(f"data/images/{images[0]}.png")  # Can be many different formats
    im1 = np.asarray(im1, dtype=object)
    if im1.shape[2] == 4:  # We don't use the transparency of a RGBA image
        im1 = im1[:, :, :3]
    
    # IMAGE 2
    im2 = Image.open(f"data/images/{images[1]}.png")  # Can be many different formats
    im2 = np.asarray(im2, dtype=object)
    if im2.shape[2] == 4:  # We don't use the transparency of a RGBA image
        im2 = im2[:, :, :3]

    ''' ======== Pre-processing======== '''
    ''' Because of projection issue, we need to flip vertically and horizontally the image'''
    im1 = np.flip(im1)
    im1 = np.flip(im1, axis=1)

    size_x1 = np.shape(im1)[0]
    size_y1 = np.shape(im1)[1]
    list_cube1 = [[np.shape(im1)[1]*12, 0, 0, 0, 0], [0, 0, 0, 0, 0]] # initialize the list with shape infos
    nb_cubes1 = 1

    im2 = np.flip(im2)
    im2 = np.flip(im2, axis=1)

    size_x2 = np.shape(im2)[0]
    size_y2 = np.shape(im2)[1]
    list_cube2 = [[np.shape(im2)[1]*12, 0, 0, 0, 0], [0, 0, 0, 0, 0]] # initialize the list with shape infos
    nb_cubes2 = 1

    ''' ======== Creation of the perspective ========= '''
    ''' We iterate through all the pixels, along x and y of the first image'''
    for x1 in range(0, size_x1):
        for y1 in range(0, size_y1):
            if list(im1[x1, y1]) != [255, 255, 255]:  # continue if the pixel is white
                available_z1s = find_available(im2)

                ''' The 3D coordinates and the size of the cube are conditionned to the depth factor '''
                for z1 in available_z1s:
                    cube = [x1, y1, z1, pix_size, [0, 0, 0, 0]]
                    list_cube1 = np.vstack([list_cube1, cube])
                    nb_cubes1 += 1

    ''' We iterate through all the pixels, along x and y of the second image'''
    for x2 in range(0, size_x2):
        for y2 in range(0, size_y2):
            if list(im2[x2, y2]) != [255, 255, 255]:  # continue if the pixel is white
                available_z2s = find_available(im1)

                ''' The 3D coordinates and the size of the cube are conditionned to the depth factor '''
                for z2 in available_z2s:
                    cube = [z2, y2, x2, pix_size, [0, 0, 0, 0]]
                    list_cube2 = np.vstack([list_cube2, cube])
                    nb_cubes2 += 1

    list_cube = list(list_cube1) + list(list_cube2)
    np.save('./data/list_objects/list_cube_double_persp.npy', list_cube)
    return list_cube


parser = argparse.ArgumentParser()
parser.add_argument("--image_name", help="name of the image you want to put in perspective (for example smiley.\
                        It will search for original picture in data/images and search as image.png", type=str)
parser.add_argument("--overwrite", help="overwrite .npy if already created. Default False.",
                    type=bool, default=False)
parser.add_argument("--max_pixels", help="maximum number of pixels maximum size of the image. "
                                         "If the original image is bigger, it will be reduced "
                                         "to this size. Default 1000", type=int, default=1000)

args = parser.parse_args()
make_list_cube(args.image_name, args.overwrite, args.max_pixels)


# make_list_cube_3D(['custom_image1', 'custom_image2'], )