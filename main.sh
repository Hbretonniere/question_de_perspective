#!/bin/bash
# First argument = name of the image
# Second argument = number of frames for the image
# third argument = frames per second for the video
image_name=$1
nb_frames=$2
fps=$3

python do_cubes.py  --image_name=$image_name
blender blender/museum.blend --python script_blender.py -- $image_name $nb_frames
python do_video.py --image_name=$image_name --fps=$fps
