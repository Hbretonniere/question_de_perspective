from math import ceil
import matplotlib as mpl
from matplotlib import gridspec
import matplotlib.pyplot as plt
import numpy as np

class pixel_art:
    def __init__(
        self, 
        fig, 
        gs, 
        size=15
    ):
        self.size = size
        self.canevas = fig.add_subplot(gs[0])
        self.canevas.set_xticks(np.arange(self.size))
        self.canevas.set_yticks(np.arange(self.size))
        self.canevas.set_xticklabels([""]*self.size)
        self.canevas.set_yticklabels([""]*self.size)
#         self.canevas.set_xlim([0, size])
        
        self.show_palette = fig.add_subplot(gs[1])
        self.show_palette.set_xticks(np.arange(3))
        self.show_palette.set_yticks(np.arange(3))
        self.show_palette.set_xticklabels([""]*3)
        self.show_palette.set_yticklabels([""]*3)        
        self.image = np.zeros((self.size, self.size))
        self.palette = np.arange(9)
        self.palette = self.palette.reshape(3, 3)
        
        self.cmap = mpl.colors.ListedColormap(['white', 'red', 'green', 'blue', 'cyan', 'orange', 'black', 'purple', 'yellow'])
        self.canevas.set_aspect('equal')
        self.canevas.imshow(self.image, vmin=0, vmax=9, cmap=self.cmap, extent=[-1, self.size-1, -1, self.size-1], origin='lower')
        self.canevas.grid()
        self.show_palette.imshow(self.palette, vmin=0, vmax=9, cmap=self.cmap, extent=[-1, 2, -1, 2], origin='lower')
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

            else :
#                 self.canevas.set_title(ax)
                self.image[ceil(click_y), ceil(click_x)] = self.couleur
                self.canevas.imshow(self.image, cmap=self.cmap, vmin=0, vmax=9,
                                    extent=[-1, self.size-1, -1, self.size-1], origin='lower')
                plt.draw()
        if event.button == 3:
            np.save('custom_image.npy', self.image)
            mpl.image.imsave('custom_image.png',self.image)

            
fig = plt.figure(figsize=(5, 5), constrained_layout=True)
gs = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[5, 3])
pixel_art(fig, gs)
plt.show()
