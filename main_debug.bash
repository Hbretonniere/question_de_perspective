#!/bin/bash
image_name=smiley
#image_name=my_face
nb_frames=10
fps=10
max_pixels=1000



python do_cubes.py  --image_name=$image_name --overwrite=True --max_pixels=$max_pixels
blender blender/museum.blend --python script_blender.py -- $image_name $nb_frames $max_pixels
python do_video.py --image_name=$image_name --fps=$fps --overwrite=True --max_pixels=$max_pixels

