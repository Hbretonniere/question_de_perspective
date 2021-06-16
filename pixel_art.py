from math import ceil
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
from matplotlib.widgets import Button


class pixel_art:
    def __init__(
        self,
        fig,
        gs,
        size=15
    ):
        self.size = size

        self.canevas = fig.add_subplot(gs[0])
        self.canevas.set_title('Left click to paint the pixel \n with the color selected on the Canvas.', fontsize=10)
        self.canevas.set_xticks(np.arange(self.size))
        self.canevas.set_yticks(np.arange(self.size))
        self.canevas.set_xticklabels([""]*self.size)
        self.canevas.set_yticklabels([""]*self.size)

        self.show_palette = fig.add_subplot(gs[1])
        self.show_palette.set_title('Left click on the color to select it.', fontsize=7)
        self.show_palette.set_xticks(np.arange(3))
        self.show_palette.set_yticks(np.arange(3))
        self.show_palette.set_xticklabels([""]*3)
        self.show_palette.set_yticklabels([""]*3)

        self.image = np.zeros((self.size, self.size, 3)) + (255, 255, 255)
        self.image = self.image.astype(np.uint8)
        self.palette = np.asarray([[255, 0, 0], [0, 255, 0], [0, 0, 255],
                                  [253, 173, 11], [125, 28, 187], [28, 187, 183],
                                  [233, 249, 35], [0, 0, 0], [255, 255, 255]])
        self.palette = self.palette.reshape(3, 3, 3)

#         self.cmap = mpl.colors.ListedColormap(['white', 'red', 'green', 'blue', 'cyan', 'orange', 'black', 'purple', 'yellow'])
        self.canevas.set_aspect('equal')
        self.canevas.imshow(self.image, vmin=0, vmax=9, extent=[-1, self.size-1, -1, self.size-1], origin='lower')
        self.canevas.grid()
        self.show_palette.imshow(self.palette, vmin=0, vmax=9, extent=[-1, 2, -1, 2], origin='lower')
        fig.canvas.mpl_connect('button_press_event', self)
        self.couleur = 0

        ax_save_button = plt.axes([0.65, 0.2, 0.15, 0.1])
        ax_launch_button = plt.axes([0.82, 0.2, 0.15, 0.1])
        self.save_button = Button(ax_save_button, 'SAVE', color='gray', hovercolor='red')
        self.launch_button = Button(ax_launch_button, 'LAUNCH', color='gray', hovercolor='red')

    def __call__(self, event):
        click_x = event.xdata
        click_y = event.ydata
        ax = event.inaxes

        def save_drawing(val):
            im_to_save = np.copy(self.image)  # We need to inver the R and B channels
            im_to_save[:, :, 0] = self.image[:, :, 2]  # B to R
            im_to_save[:, :, 2] = self.image[:, :, 0]  # R to B
            im_to_save = np.flip(np.flip(im_to_save), axis=1)  # We need to flip horizontaly and verticaly
            np.save('data/images/custom_image.npy', im_to_save)
            im = Image.fromarray(im_to_save)
            im.save("data/images/custom_image.png")
            plt.suptitle("SAVED !", x=0.5, y=0.92, color='red')
            plt.draw()
        
        def save_and_launch(val):
            plt.suptitle("Wait for it !", x=0.5, y=0.92, color='red')
            plt.draw()
            os.system("sh main.sh custom_image 10 10")

        self.save_button.on_clicked(save_drawing)
        self.launch_button.on_clicked(save_and_launch)

        if event.button == 1:
            if ax == self.show_palette:
                self.couleur = self.palette[ceil(click_y), ceil(click_x)]
                plt.suptitle(" ", x=0.5, y=0.9)

            if ax == self.canevas:
                self.image[ceil(click_y), ceil(click_x)] = self.couleur
                self.canevas.imshow(self.image, vmin=0, vmax=9,
                                    extent=[-1, self.size-1, -1, self.size-1], origin='lower')
                plt.suptitle(" ", x=0.5, y=0.92)
                plt.draw()


fig = plt.figure(figsize=(5, 5), constrained_layout=True)
gs = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[5, 3])
pixel_art(fig, gs)
plt.show()
