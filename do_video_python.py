import sys
import argparse
import glob
import re
import os
import moviepy.video.io.ImageSequenceClip

parser = argparse.ArgumentParser()
parser.add_argument("--image_name", help=" file name of the image you want to put in perspective (for example smiley.jpg)" , type=str)
parser.add_argument("--fps", help="frame per second for the video (for example 10)" , type=int)
parser.add_argument("--max_pixels", help="maximum number of pixels " , type=int)
parser.add_argument("--overwrite", help="overwrite .npy if already created. Default False.",
                    type=bool, default=False)
args = parser.parse_args()
image_name = args.image_name
fps = args.fps
overwrite = args.overwrite
max_pixels = args.max_pixels


def sort_nicely(liste):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    liste.sort(key=alphanum_key)
    return liste


frame_name = './data/rendered/'+image_name+'/'+image_name+'_max_pixels'+str(max_pixels)+\
                 '_frame_'
image_files = sort_nicely(glob.glob(frame_name+'*.png'))

# let the final frame for 2 seconds on the end of the video
for i in range(2*fps):
    image_files.append(image_files[-1])
nb_frames = len(image_files)
video_name = 'data/rendered/'+image_name+'/'+image_name+'_'+\
str(nb_frames)+'frames_'+'max_pixels'+str(max_pixels)+'_'+str(fps)+'fps.mp4'
if os.path.isfile(video_name) and not overwrite:
    print(video_name+' already there, and overwrite set to False. Skipping')
else:

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(video_name)
