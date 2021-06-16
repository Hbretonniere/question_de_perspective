from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import numpy as np
import os

fig = plt.figure(figsize=(5, 5), constrained_layout=True)


draw_ax = plt.axes([0.1, 0.2, 0.4, 0.1])
draw_button = Button(draw_ax, 'Draw your own art', color='gray', hovercolor='Blue')

visit_ax = plt.axes([0.55, 0.2, 0.4, 0.1])
visit_button = Button(visit_ax, 'Visit the Museum', color='gray', hovercolor='red')

def pixel_art(_):
    os.system('python pixel_art.py')

def visit(_):
    os.system('blender blender/museum.blend --python visit_museum.py')


draw_button.on_clicked(pixel_art)
visit_button.on_clicked(visit)

plt.show()
