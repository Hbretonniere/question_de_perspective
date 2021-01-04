#!/bin/bash
# First argument = name of the image
# Second argument = number of frames for the image
# third argument = frames per second for the video

path=$(pwd)
python $path/do_cubes.py $1
echo $3
blender blender/museum.blend --python script_blender.py -- $1 $2

python $path/do_video.py $1 $3
