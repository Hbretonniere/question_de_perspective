import sys
import argparse
import glob
import re
import os
import moviepy.video.io.ImageSequenceClip

parser = argparse.ArgumentParser()
parser.add_argument("--image_name", help=" file name of the image you want to put in perspective (for example smiley.jpg)" , type=str)
parser.add_argument("--fps", help="frame per second for the video (for example 10)" , type=int)
args = parser.parse_args()
image_name = args.image_name
fps = args.fps


def sort_nicely(liste):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    liste.sort(key=alphanum_key)
    return liste


if os.path.isfile('data/rendered/'+image_name+'/'+image_name+'_video.mp4'):
    print('data/rendered/'+image_name+'/'+image_name+'_video.mp4 already there, skipping')
else:
    image_files = [img for img in sort_nicely(glob.glob('data/rendered/'+image_name+'/'+image_name+'*.png'))]
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile('data/rendered/'+image_name+'/'+image_name+'_video.mp4')
