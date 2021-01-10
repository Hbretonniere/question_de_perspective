"""
Created on Fri May  1 15:18:40 2020
@author: Hubert Bretonnière
"""
from PIL import Image
import numpy as np
import os
import moviepy.video.io.ImageSequenceClip
import re
import glob




def get_hex_color(x):
    'Transform a RBG color to its hexadecimal code'
    r = max(0, min(x[0], 255))
    g = max(0, min(x[1], 255))
    b = max(0, min(x[2], 255))
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)




