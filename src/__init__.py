#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
from .config_variables import * 

from .cmdline_controll import *

from PIL import Image, PngImagePlugin, JpegImagePlugin, ImageDraw, ImageFont
import cv2
import numpy as np
from sys import argv


from pygame import Surface, surfarray, SRCALPHA, font, draw, Rect, image
from pygame.transform import scale
from pygame.sprite import Sprite, Group

from random import randint
from moviepy import AudioFileClip, ImageSequenceClip


from os import listdir as os_path
from os.path import exists as path_exist
from os import getcwd as GETPWD
from time import time as time_now

class Sprites_(Sprite):
        def __init__(self, _file: str | Image.Image = None):
            super().__init__()
            if type(_file) == Image.Image:
                try:
                    self.image = image.frombytes(_file.tobytes(), _file.size,  _file.mode)
                    self.mode = _file.mode
                except ValueError:
                    self.image = image.frombytes(_file.tobytes(), _file.size, 'RGB')
                    self.mode = 'RGB'
            elif type(_file) == np.ndarray:
                _tmp_img = Image.fromarray(_file).convert()
                self.image = image.frombytes(_tmp_img.tobytes(), _tmp_img.size,_tmp_img.mode)
                self.mode = _tmp_img.mode
            else:
                self.image = image.load(_file)
            self.rect = self.image.get_rect()    
