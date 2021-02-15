from math import ceil
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class pixel_art:
    def __init__(
        self,
        fig,
        gs,
        size=15
    ):
        self.size = size

        self.canevas = fig.add_subplot(gs[0])
        self.canevas.set_title('Left click to paint with the selected color. \n Right click (or ctrl click) to save.', fontsize=7)
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
                                  [233, 249, 35], [197, 95, 8], [255, 255, 255]])
        self.palette = self.palette.reshape(3, 3, 3)

#         self.cmap = mpl.colors.ListedColormap(['white', 'red', 'green', 'blue', 'cyan', 'orange', 'black', 'purple', 'yellow'])
        self.canevas.set_aspect('equal')
        self.canevas.imshow(self.image, vmin=0, vmax=9, extent=[-1, self.size-1, -1, self.size-1], origin='lower')
        self.canevas.grid()
        self.show_palette.imshow(self.palette, vmin=0, vmax=9, extent=[-1, 2, -1, 2], origin='lower')
        fig.canvas.mpl_connect('button_press_event', self)
        self.couleur = 0

#         cbar.ax.set_ticks([])
    def __call__(self, event):
        click_x = event.xdata
        click_y = event.ydata
        ax = event.inaxes
        if event.button == 1:
            if ax == self.show_palette:
                self.couleur = self.palette[ceil(click_y), ceil(click_x)]
                plt.suptitle(" ", x=0.5, y=0.9)

            else:
                self.image[ceil(click_y), ceil(click_x)] = self.couleur
                self.canevas.imshow(self.image, vmin=0, vmax=9,
                                    extent=[-1, self.size-1, -1, self.size-1], origin='lower')
                plt.suptitle(" ", x=0.5, y=0.9)
                plt.draw()
        if event.button == 3:
            im_to_save = np.copy(self.image)  # We need to inver the R and B channels
            im_to_save[:, :, 0] = self.image[:, :, 2]  # B to R
            im_to_save[:, :, 2] = self.image[:, :, 0]  # R to B
            im_to_save = np.flip(np.flip(im_to_save), axis=1)  # We need to flip horizontaly and verticaly
            np.save('data/images/custom_image.npy', im_to_save)
            im = Image.fromarray(im_to_save)
            im.save("data/images/custom_image.png")
            plt.suptitle("SAVED !", x=0.5, y=0.9, color='red')
            plt.draw()


fig = plt.figure(figsize=(5, 5), constrained_layout=True)
gs = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[5, 3])
pixel_art(fig, gs)
plt.show()
