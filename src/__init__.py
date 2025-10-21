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
