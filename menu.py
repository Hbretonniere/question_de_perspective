from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import os
from PIL import Image

fig, ax = plt.subplots(figsize=(5, 5), constrained_layout=True)
plt.axis('off')
language = 'english'


im = Image.open("data/images/language_flags.png")
left, bottom, width, height = [0.05, 0.85, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height], label='flag')
ax2.imshow(im)
ax2.axis('off')

english_text = {'title': 'Choose what you want to do !',
                'visit': 'Visit the Museum',
                'draw': 'Draw your own art',
                'create': 'Create video',
                'see_video': 'See your video',
                'see_mondrian': 'See Mondrian video'}

french_text = {'title': '         Choisis ton action !',
               'visit': 'Visite le Musée',
               'draw': "Dessine ta propre \n oeuvre d'art",
               'create': 'Crée ta video',
               'see_video': 'Regarde ta vidéo',
               'see_mondrian': 'Regarde la vidéo Mondrian'}

text = english_text

fig.text(0.18, 0.8, text['title'], c='red', fontsize=15)

visit_ax = plt.axes([0.05, 0.5, 0.4, 0.1])
visit_button = Button(visit_ax, text['visit'], color='gray', hovercolor='red')

draw_ax = plt.axes([0.55, 0.5, 0.4, 0.1])
draw_button = Button(draw_ax, text['draw'], color='gray', hovercolor='Blue')

create_vid_ax = plt.axes([0.3, 0.3, 0.4, 0.1])
create_vid_button = Button(create_vid_ax, text['create'], color='gray', hovercolor='Blue')

video_ax = plt.axes([0.05, 0.1, 0.4, 0.1])
video_button = Button(video_ax, text['see_video'], color='gray', hovercolor='Blue')

mondrian_ax = plt.axes([0.55, 0.1, 0.4, 0.1])
mondrian_button = Button(mondrian_ax, text['see_mondrian'], color='gray', hovercolor='Blue')
menu = visit_button, draw_button, create_vid_button, video_button, mondrian_button


def select_language(event):
    x = event.xdata
    y = event.ydata
    if ((x < 720) & (y < 453) & (event.inaxes.get_label() == 'flag')):
        language = 'english'
    if ((x > 720) & (x < 1440) & (y < 453) & (event.inaxes.get_label() == 'flag')):
        language = 'french'
    if (event.inaxes.get_label() == 'flag'):
        change_language(language)
        plt.draw()
    return


def change_language(language):
    if language == 'french':
        text = french_text
    if language == 'english':
        text = english_text

    draw_button.label.set_text(text['draw'])
    visit_button.label.set_text(text['visit'])
    video_button.label.set_text(text['see_video'])
    mondrian_button.label.set_text(text['see_mondrian'])
    create_vid_button.label.set_text(text['create'])
    del fig.texts[0]

    fig.text(0.18, 0.8, text['title'], c='red', fontsize=15)


fig.canvas.mpl_connect('button_press_event', select_language)


def pixel_art(_):
    os.system('python pixel_art.py')


def visit(_):
    os.system('blender blender/museum.blend --python visit_museum.py')


def create_your_video(_):
    # plt.text(1.5, 0.5, 'Wait for the rendering of the video, takes few minutes.', color='red')
    plt.draw()
    os.system('blender -b blender/museum.blend --python create_video.py -- custom_image 30 1000')
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
