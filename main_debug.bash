#!/bin/bash
image_name=smiley
nb_frames=2
fps=10

python do_cubes.py  --image_name=$image_name #--overwrite=True
#blender blender/museum.blend --python script_blender.py -- $image_name $nb_frames
python do_video.py --image_name=$image_name --fps=$fps --overwrite=True
