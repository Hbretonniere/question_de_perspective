#!/bin/bash

max_pixels=1000
#maximum number of pixels maximum size of the image.
# If the original image is bigger, it will be reduced to this size. Default 1000

image_name=$1
#name of the image you want to put in perspective (for example smiley)
#It will search for original picture in data/images and search as image.png
nb_frames=$2
fps=$3

python do_cubes.py  --image_name=$image_name --overwrite=True --max_pixels=$max_pixels
blender blender/museum.blend --python script_blender.py -- $image_name $nb_frames $max_pixels
python do_video.py --image_name=$image_name --fps=$fps --overwrite=True --max_pixels=$max_pixels
