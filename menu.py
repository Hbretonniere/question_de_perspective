from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import os
from PIL import Image
import glob
import numpy as np

''' 
TO DOOOOOOO 
- ADD THE POSSIBILITY TO CREATE WHITE CUBES (FOR EXAMPLE WITH A COLOR LIKE (1E-6, 1E-6, 1E-6),
 and put the white apart to be the eraser
- ADAPT THE LANGUAGE OF THE PIXEL ART WITH THE LANGUAGE OF THE MENU.
- ADDS RANDOM PUZZLING OF THE SHAPES (2D) (PYRAMIFS, PARRALELLEPIPEDES, SQUARES...)
https://www.youtube.com/watch?v=SKfpYVK_r0E
'''

os.system('chmod 0444 blender/museum.blend')

fig, ax = plt.subplots(figsize=(5, 5), constrained_layout=True)
plt.axis('off')
language = 'english'


im = Image.open("data/images/language_flags.png")
left, bottom, width, height = [0.05, 0.8, 0.3, 0.3]
ax2 = fig.add_axes([left, bottom, width, height], label='flag')
ax2.imshow(im)
ax2.axis('off')

english_text = {'title': 'Choose what you want to do !',
                'visit': 'Visit the Museum',
                'draw': 'Draw your own art',
                'create': 'Create video',
                'see_video': 'See your video',
                'see_mondrian': 'See Mondrian video',
                'watch_video_warning': 'You need to create your video first !',
                'create_video_warning': 'You need to create your art first !',
                'cant_open': 'Sorry, I cannot open the video...',
                'help': 'If you want an easy navigation on the museum \n press "tab" inside the museum'}

italian_text = {'title': 'Scegli cosa vuoi fare !',
                'visit': 'Visita il Museo',
                'draw': 'Disegna la tua opera',
                'create': 'Crea il video',
                'see_video': 'Guarda il tuo video',
                'see_mondrian': 'Guarda il video di Mondian',
                'watch_video_warning': 'You need to create your video first !',
                'create_video_warning': 'You need to create your art first !',
                'cant_open': 'Sorry, I cannot opne the video...',
                'help': 'If you want an easy navigation on the museum \n press "tab" inside the museum'}

french_text = {'title': ' Choisis ton action !',
               'visit': 'Visite le Musée',
               'draw': "Dessine ta propre \n oeuvre d'art",
               'create': 'Crée ta video',
               'see_video': 'Regarde ta vidéo',
               'see_mondrian': 'Regarde la vidéo Mondrian',
               'watch_video_warning': "Tu dois créer ta vidéo avant de la regarder !",
               'create_video_warning': "Tu dois créer ton oeuvre d'art avant !",
               'cant_open': 'Désolé, je ne peux pas ouvrir la vidéo...',
               'help': 'Si tu veux naviguer facilement dans le musée \n appuie sur "tab" dans le musée'}

text = english_text


own_art = False
create_vid = False
fig.text(0.18, 0.8, text['title'], c='red', fontsize=15)
fig.text(0.1, 0.7, text['help'], c='red', fontsize=10)

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


def select_color(event):
    each = 5
    c = np.linspace(20, 200, each)
    plt.figure()
    colors = []
    for r in c:
        for g in c:
            for b in c:
                colors.append([r, g, b])
    
    plt.imshow()


def select_language(event):
    global language
    x = event.xdata
    y = event.ydata
    if ((x < 612) & (y < 453) & (event.inaxes.get_label() == 'flag')):
        language = 'english'
    elif ((x > 612) & (x < 2*612) & (y < 453) & (event.inaxes.get_label() == 'flag')):
        language = 'french'
    elif ((x > 2*612) & (x < 3*612) & (y < 453) & (event.inaxes.get_label() == 'flag')):
        language = 'italian'
    if (event.inaxes.get_label() == 'flag'):
        change_language(language)
        plt.draw()
    return


def change_language(language):
    global text
    if language == 'french':
        text = french_text
    if language == 'english':
        text = english_text
    if language == 'italian':
        text = italian_text

    draw_button.label.set_text(text['draw'])
    visit_button.label.set_text(text['visit'])
    video_button.label.set_text(text['see_video'])
    mondrian_button.label.set_text(text['see_mondrian'])
    create_vid_button.label.set_text(text['create'])
    # reset_button.label.set_text(text['reset'])
    del fig.texts[:]

    fig.text(0.18, 0.8, text['title'], c='red', fontsize=15)
    fig.text(0.1, 0.7, text['help'], c='red', fontsize=10)


fig.canvas.mpl_connect('button_press_event', select_language)


def pixel_art(_):
    os.system(f'python pixel_art.py {language}')
    if len(fig.texts) == 2:
        del(fig.texts[1])
    global own_art
    own_art = True


def visit(_):
    os.system('blender blender/museum.blend --python visit_museum.py')


def create_your_video(_):
    global create_vid
    if own_art:
        os.system('blender -b blender/museum.blend --python create_video.py -- custom_image 10 1000')
        os.system('python do_video_python.py --image_name=custom_image --fps=10 --max_pixels=1000 --overwrite=True')
        create_vid = True
    else:

        if len(fig.texts) == 2:
            del(fig.texts[1])
        fig.text(0.27, 0.7, text['create_video_warning'], color='red')
        plt.draw()


def read_video(_):
    if not create_vid:
        if len(fig.texts) == 2:
            del fig.texts[1]
        fig.text(0.25, 0.7, text['watch_video_warning'], color='red')
        plt.draw()

    else:
        name = glob.glob('data/rendered/custom_image/*.mp4')[0]
        print(name)
        open_exit = os.system('open ' + name)

        if open_exit != 0:
            open_exit = os.system('mpv -fs ' + name)
            if open_exit != 0:
                open_exit = os.system('vlc ' + name)
                if open_exit != 0:
                    plt.text(-0.9, 6, text["cant_open"], color='red')
                    plt.draw()


def read_mondrian(_):
    name = glob.glob('data/rendered/mondrian/*.mp4')[0]
    print(name)
    open_exit = os.system('open ' + name)
    if open_exit != 0:
        open_exit = os.system('mpv -fs ' + name)
        if open_exit != 0:
            open_exit = os.system('vlc ' + name)
            if open_exit != 0:
                plt.text(-0.9, 6, text["cant_open"], color='red')
                plt.draw()


draw_button.on_clicked(pixel_art)
visit_button.on_clicked(visit)
video_button.on_clicked(read_video)
mondrian_button.on_clicked(read_mondrian)
create_vid_button.on_clicked(create_your_video)
plt.show()
