from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import cv2
import os
import glob

fig = plt.figure(figsize=(5, 5), constrained_layout=True)


draw_ax = plt.axes([0.1, 0.2, 0.4, 0.1])
draw_button = Button(draw_ax, 'Draw your own art', color='gray', hovercolor='Blue')

visit_ax = plt.axes([0.55, 0.2, 0.4, 0.1])
visit_button = Button(visit_ax, 'Visit the Museum', color='gray', hovercolor='red')

video_ax = plt.axes([0.1, 0.5, 0.4, 0.1])
video_button = Button(video_ax, 'See your video', color='gray', hovercolor='Blue')

mondrian_ax = plt.axes([0.55, 0.5, 0.4, 0.1])
mondrian_button = Button(mondrian_ax, 'See Mondrian video', color='gray', hovercolor='Blue')

create_vid_ax = plt.axes([0.3, 0.7, 0.4, 0.1])
create_vid_button = Button(create_vid_ax, 'Create video', color='gray', hovercolor='Blue')


def pixel_art(_):
    os.system('python pixel_art.py')


def visit(_):
    os.system('blender blender/museum.blend --python visit_museum.py')


def create_your_video(_):
    # plt.text(1.5, 0.5, 'Wait for the rendering of the video, takes few minutes.', color='red')
    plt.draw()
    os.system('blender -b blender/museum.blend --python create_video.py -- custom_image 2 1000')
    os.system('python do_video_python.py --image_name=custom_image --fps=10 --max_pixels=1000 --overwrite=True')
    

def read_video(_):
    try:
        os.system('open data/rendered/custom_image/*.mp4')
    except Exception:
        try:
            os.system('mpv -fs data/rendered/custom_image/*.mp4')
        except Exception:
            plt.text(0.9, 0.1, "Sorry, can't open the video on your OS")


def read_mondrian(_):
    try:
        os.system('open data/rendered/mondrian/*.mp4')
    except Exception:
        try:
            os.system('mpv -fs data/rendered/mondrian/*.mp4')
        except Exception:
            plt.text(0.9, 0.1, "Sorry, can't open the video on your OS")


draw_button.on_clicked(pixel_art)
visit_button.on_clicked(visit)
video_button.on_clicked(read_video)
mondrian_button.on_clicked(read_mondrian)
create_vid_button.on_clicked(create_your_video)
plt.show()
