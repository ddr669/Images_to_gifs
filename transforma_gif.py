#!/bin/venv python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
###################
###### Imports #######
from PIL import Image
import cv2


import numpy as np
from sys import argv
from pygame import Surface, surfarray, SRCALPHA, font, draw, Rect, image
from pygame.transform import scale
from pygame.sprite import Sprite, Group
from cmdline_verify import cmdline_verify
from cmdline_verify import __help__, return_file_
from random import randint
from moviepy import VideoClip,AudioFileClip, CompositeAudioClip,CompositeVideoClip, ImageSequenceClip
from os import listdir as os_path
from time import time as time_now

###### Sprites #######
class Sprites_(Sprite):
    def __init__(self, color=(0,0,0,0), height: int = None, width: int = None,
                 _file: str = None):
        super().__init__()
        if type(_file) == Image.Image:
            self.image = image.frombytes(_file.tobytes(), _file.size, 'RGB')
        else:
            self.image = image.load(_file) if _file else Surface([width, height])
        if width:
            draw.rect(self.image,color,Rect(0,0,width,height))
        self.rect = self.image.get_rect()
        if self.rect[-1] >= 720 or self.rect[-2] >= 1024:
            self.image = scale(self.image, (720, 500))
            self.rect = self.image.get_rect()

DEBUG_INFO = 1


def make_video_from_video(
                        file, out: str = "video_as_gif.gif",
                        frame_counter: int = 90, text: str = "10",
                        font_color: tuple = (0,0,0),
                        lower_color: list = np.array([140,140,140]),
                        upper_color: list = np.array([220,220,220]),
                        start_clip: int = 0,
                        end_clip: int = 90,
                        remove_bg: bool = False,
                        new_bg_color: tuple = (),
                        ):
    
    global DEBUG_INFO

    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: Ini")
    init_time = time_now()
    cap = cv2.VideoCapture(file)
    
    
    counter = 0
    sub_counter = 0 
    FRAMES = []
    CLIPS = []
    while cap.isOpened():
        ret, cv2_frame = cap.read()
        
        
        if ret:
            converted = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(converted)
            FRAMES.append(make_image_from_fonts(pil_image,
                                                text=text,
                                                font_color=font_color,
                                                lower_target=lower_color,
                                                upper_target=upper_color,
                                                remove_bg=remove_bg,
                                                new_bg_color=new_bg_color))
         

        elif ret:
            pass
        else:
            break
        counter += 1
        sub_counter += 1
        if counter >= frame_counter:
            break
    cap.release() 
   
    #Image.Image.width
    #Image.Image.getdata()
    if DEBUG_INFO:
        print("[!done load array in heap]")

    frames = [np.array(_) for _ in FRAMES]
    scene = ImageSequenceClip(frames, fps=60)
    audioclip = AudioFileClip(file)
    audioclip.duration = scene.duration
    scene.audio = audioclip
    
    scene.write_videofile(out)
    #final_video = CompositeVideoClip([clip, audioclip])
    #final_video.write_videofile(filename=out,audio=True)


    #frame0 = FRAMES[0]
    #frame0.save(f"out/{out}", save_all=True,append_images=FRAMES,duration=frame_counter, loop=0)

    now_time = time_now()
    tempo_de_exec = now_time - init_time
    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: time elapsed -> {tempo_de_exec}")
    
def make_gif_from_video(
                        file, out: str = "video_as_gif.gif",
                        frame_counter: int = 90, text: str = "10",
                        font_color: tuple = (0,0,0),
                        lower_color: list = np.array([140,140,140]),
                        upper_color: list = np.array([220,220,220]),
                        remove_bg: bool = False,
                        new_bg_color: tuple = (),
                        ):
    global DEBUG_INFO
    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: Ini")
    init_time = time_now()
    cap = cv2.VideoCapture(file)
    counter = 0
    sub_counter = 0 
    FRAMES = []
    while cap.isOpened():
        ret, cv2_frame = cap.read()
        if ret and sub_counter % 3 == 0:
            converted = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(converted)
            FRAMES.append(make_image_from_fonts(pil_image,
                                                text=text,
                                                font_color=font_color,
                                                lower_target=lower_color,
                                                upper_target=upper_color,
                                                remove_bg=remove_bg,
                                                new_bg_color=new_bg_color))
        elif ret:
            pass
        else:
            break
        counter += 1
        sub_counter += 1
        if counter >= frame_counter:
            break
    cap.release()
    frame0 = FRAMES[0]
    frame0.save(f"out/{out}", save_all=True,append_images=FRAMES,duration=frame_counter, loop=0)
    now_time = time_now()
    tempo_de_exec = now_time - init_time
    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: time elapsed -> {tempo_de_exec}")
    

def make_image_from_fonts(file,
                        font_family: str = "lucidaconsole", 
                        font_size: int = 12,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        font_color: tuple = (255,255,255),
                        text: str = None,
                        remove_bg: bool = False,
                        new_bg_color: tuple = (0,0,0)) :
    '''*make_image_from_fonts -
            Takes a file object or PIL.Image object 
            with argument and some parameters to return a PIL.Image
            overwrite the pixels in range color between lower and
            upper target.
            - font_family: str, default="lucidaconsole".
            - font_size: int, default=12. # thats is perfect
            - font_color: tuple, default=(255,255,255).
            - lower_target: list, default=numpy.array([0,0,0]) # black
            - upper_target: list, default=numpy.array([45,45,45]) # gray
            - text: str, default=["1","0"]
            - remove_bg: bool, default=False.
            - new_bg_color: tuple = (0,0,0).'''
    sprite_group = Group()
    _img = Sprites_(_file=file)
    sprite_group.add(_img)
    size = _img.image.get_rect()[2:]
    arraysurf = Surface((size[0],size[1]), SRCALPHA)
    font.init()
    font_pygame = font.SysFont(font_family, font_size)
    texto = font_pygame.render(text if text else "", True, font_color)
    arraysurf.fill((0,0,0,0))
    sprite_group.draw(arraysurf)
    _tmp = surfarray.array3d(arraysurf)
    chars_ = ["0", "1"] if not text else [letter for letter in text] # ░
    for a in range(1, size[1], 12):
        for x in range(1, size[0],8):
                r,g,b = _tmp[x][a]
                if r in range(lower_target[0], upper_target[0]) and g in range(lower_target[1], upper_target[1]) and b in range(lower_target[2],upper_target[2]):
                    if remove_bg:
                        draw.rect(arraysurf,new_bg_color, Rect(x, a, 12, 12)) 
                    arraysurf.blit(texto, (x,a))
                _text = f"{chars_[randint(0, len(chars_)-1)]}"
                texto = font_pygame.render(_text, True, font_color)
    _tmp = surfarray.array3d(arraysurf)
    imagem_com_texto = Image.fromarray(_tmp)
    view = imagem_com_texto.transpose(Image.Transpose.TRANSPOSE)
    view = view.quantize(method=2,colors=140, dither=Image.Dither.RASTERIZE).convert('RGB')
    del(sprite_group)
    del(_img, arraysurf, font_pygame, texto, _tmp, imagem_com_texto)
    return view
    

def save_as_gif(file, text: str = 'x;', 
                img_count: int = 60, 
                out: str = "teste_rasterized_nobg.gif",
                target: list = None,
                remove_bg: bool = False,
                new_bg_color: tuple = (255,0,0),
                font_color: tuple = (255,255,255),
                font_family: str = 'lucidaconsola'):
    ''' save files from path to save as gif in out '''
    try:
        lower_target = np.array(target[0])
        upper_target = np.array(target[1])
    except IndexError as err:
        print(f'[!] IndexError: target must be a list of two tuple/list.\n{err}')
        lower_target = np.array([0,0,0])
        upper_target = np.array([45,45,45])
    
    frames = [make_image_from_fonts(file=file,
                                    text=text,
                                    lower_target=lower_target,
                                    upper_target=upper_target,
                                    remove_bg=remove_bg,
                                    new_bg_color=new_bg_color,
                                    font_color=font_color,
                                    font_family=font_family) for _ in range(0, img_count)]
    
    frame0 = frames[0]
    frame0.save(f"out/{out}", save_all=True, append_images=frames, duration=90, loop=0)

def main(file_dict: dict):
    if file_dict == "!":
        __help__()
        exit()
  
    if file_dict["GUI"]:
        pass

if __name__ == "__main__":
    make_video_from_video('jamelao.mp4', out="out/jamelao_finaly_mamae.mp4",
                        lower_color=np.array([0,0,0]),
                        upper_color=np.array([120,105,145]),
                        remove_bg=False,frame_counter=600,
                        font_color=(250,0,0))

    print("[*] done.")
    input()
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)

    except IndexError as Err:
        _file_ = return_file_()
   
    app = main(_file_)
    