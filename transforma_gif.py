#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
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
from moviepy import AudioFileClip, ImageSequenceClip
from os import listdir as os_path
from os.path import exists as path_exist
from os import getcwd as GETPWD
from time import time as time_now

from src.config_variables import * 
font.init()

class Sprites_(Sprite):
    def __init__(self, _file: str = None, color=(0,0,0,0), height: int = None, width: int = None
                ):
        super().__init__()
        if type(_file) == Image.Image:
            try:
                self.image = image.frombytes(_file.tobytes(), _file.size,  'RGB')
                self.mode = "RGB"
            except ValueError:
                
                self.image = image.frombytes(_file.tobytes(), _file.size, 'RGBA')
                self.mode = "RGBA"
        else:
            self.image = image.load(_file) if _file else Surface([width, height])
        if width:
            draw.rect(self.image,color,Rect(0,0,width,height))
        
        self.rect = self.image.get_rect()    
#


def create_surface(file: str | Image.Image | Surface, size: list | tuple = None):
    sprite_group = Group()
    if type(file) == Surface:
        file = Image.fromarray(surfarray.array3d(file))
    if type(file) == str:
        file = Image.open(file).convert()

    if size:
        file.resize(size)

    _img = Sprites_(_file=file)
    sprite_group.add(_img)
    size = _img.image.get_rect()[2:]
    arraysurf = Surface((size[0],size[1]), SRCALPHA)
    sprite_group.draw(arraysurf)
    _temp = surfarray.array3d(arraysurf)
    del _img, sprite_group, size, arraysurf

    return _temp 


def make_video_from_video(
                        file,
                        out: str = "video_as_mp4.mp4",
                        frame_counter: int = None,
                        text: str = "10",
                        font_color: tuple = (0,0,0),
                        lower_color: list = np.array([140,140,140]),
                        upper_color: list = np.array([220,220,220]),
                        start_clip: int = None,
                        end_clip: int = None,
                        remove_bg: bool = False,
                        new_bg_color: tuple = (),
                        ) -> int:
    '''
    Takes a file and make another using <code>cv2.VideoCapture()</code> ND moviepy and passing through
    editing az asked in <code>make_image_from_font()</code> until frames equals frame_counter or video_size
    nd save az <code>mp4|AMV|avi</code> file format.
    <ul>
    <h2>Parameters</h2>
    <li><h3>file </h3></li>
    <li><h3>out </h3></li>
    <li><h3>frame_counter </h3></li>
    <li><h3>text</h3></li>
    <li><h3>font_color</h3></li>
    <li><h3>lower_color</h3></li>
    <li><h3>upper_color</h3></li>
    <li><h3>remove_bg</h3></li>
    <li><h3>new_bg_color</h3></li>
    <li><h3>resize_new_file</h3></li>
    </ul>
    '''
    global FRAMES_LENGTH_VIDEO_INFO
    global DEBUG_INFO, FRAME_TO_SKIP
    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: Ini")
        init_time = time_now()
    cap = cv2.VideoCapture(file)
    counter = 0
    if end_clip:
        frame_counter = end_clip
    video_framerateps = cap.get(cv2.CAP_PROP_FPS)
    video_size_ori = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    if not frame_counter or frame_counter >= video_size_ori:
        frame_counter = video_size_ori
    high_framerate = 0
    FRAMES_LENGTH_VIDEO_INFO = frame_counter
    if video_framerateps > 25:
        high_framerate = 1
    if video_framerateps > 50:
        high_framerate = 2
    if high_framerate == 2:
        print(WARNING_FRAMERATE_LOSS)
        try:
            answer = input("Run video in 60 FPS ? [DEFAULT: N/y] (S->KILL)").strip()[0]
            if answer == "s" or answer == "S":
                cap.release() 
                return -1
            if answer == "Y" or answer == "y":
                pass
            else:
                print(answer[999])
        except IndexError:
            cap.set(cv2.CAP_PROP_FPS, 24.0)
            video_framerateps = cap.get(cv2.CAP_PROP_FPS)
            video_size_ori = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    if video_size_ori > 4000 or frame_counter > video_size_ori:
        print(WARNING_RAM_OVERFLOW)
        try:
            answer = input("Run even so [Default: N/y]: ").strip()[0]
        except IndexError:
            cap.release() 
            return -1
        if answer == "N":
            cap.release() 
            return -1
        else:
            pass
    sub_counter = 0 
    FRAMES = []
    while cap.isOpened():
        ret, cv2_frame = cap.read()
        if ret:
            converted = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(converted)
            FRAME_TO_SKIP = 24 if FRAME_TO_SKIP == 0 else FRAME_TO_SKIP
            if counter % FRAME_TO_SKIP == 0:
                if MODE_LOADED_IN_MEMORY:
                    reduces = None if not REDUCE_PIXEL_VIDEO else REDUCE_PIXEL_VIDEO
                    FRAMES.append(pil_image.reduce(reduces) if reduces else pil_image)
                else:
                    pass
            else:
                reduces = None if not REDUCE_PIXEL_VIDEO else REDUCE_PIXEL_VIDEO
                if MODE_LOADED_IN_MEMORY:
                   FRAMES.append(make_image_from_fonts(pil_image,text=text,font_color=font_color,
                                                    lower_target=lower_color,upper_target=upper_color,remove_bg=remove_bg,
                                                    new_bg_color=new_bg_color, frame_count=counter, reduce=reduces))
                else:
                    pass
        elif ret:
            pass
        else:
            break
        counter += 1
        sub_counter += 1
        if counter >= frame_counter:
            break
    cap.release() 
    if DEBUG_INFO:
        print("[!done load array in heap]")
    if type(FRAMES) == dict:
        frames = [np.array(_) for _ in FRAMES.values()]
    else:
        frames = [np.array(_) for _ in FRAMES]
    scene = ImageSequenceClip(frames, fps=video_framerateps)
    audioclip = AudioFileClip(file)
    audioclip.duration = scene.duration
    scene.audio = audioclip
    scene.write_videofile(out)
    now_time = time_now()
    tempo_de_exec = now_time - init_time
    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: time elapsed -> {tempo_de_exec}")
    del(FRAMES, scene, frames, audioclip, cap, counter, sub_counter)
    return 0

def make_gif_from_video( 
                        file, out: str = "video_as_gif.gif",
                        frame_counter: int = 90, text: str = "10",
                        font_color: tuple = (0,0,0),
                        lower_color: list = np.array([140,140,140]),
                        upper_color: list = np.array([220,220,220]),
                        remove_bg: bool = False,
                        new_bg_color: tuple = (),
                        resize_new_file: bool = False) -> None:
    '''
    Takes a file and make another using cv2.VideoCapture ND moviepy and passing through
    editing az asked in make_image_from_font() until frames equals frame_counter
    nd save az gif file format.
    <ul>
    <h2>Parameters</h2>
    <li><h3>file </h3></li>
    <li><h3>out </h3></li>
    <li><h3>frame_counter </h3></li>
    <li><h3>text</h3></li>
    <li><h3>font_color</h3></li>
    <li><h3>lower_color</h3></li>
    <li><h3>upper_color</h3></li>
    <li><h3>remove_bg</h3></li>
    <li><h3>new_bg_color</h3></li>
    <li><h3>resize_new_file</h3></li>
    </ul>
    '''
    global DEBUG_INFO, FRAMES_LENGTH_VIDEO_INFO, QUANTIZE_IMAGES_GIF, QUANTIZE_IMAGES_VIDEO
    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: Ini")
    init_time = time_now()
    cap = cv2.VideoCapture(file)
    if path_exist(file):
        pass
    else:
        raise FileNotFoundError(f"\n\rFile {file} doesn't exist in actual path: \n\r{GETPWD()}")
        
    counter = 0
    sub_counter = 0
    fps_seconds = cap.get(cv2.CAP_PROP_FPS)
    fps_size_video = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_counter = fps_size_video if frame_counter == None else frame_counter 
    FRAMES_LENGTH_VIDEO_INFO = frame_counter
    QUANTIZE_IMAGES_VIDEO = QUANTIZE_IMAGES_GIF
    FRAMES = []
    while cap.isOpened():
        ret, cv2_frame = cap.read()
        if ret:
            converted = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
            frame_width, frame_height = converted.shape[1], converted.shape[0]
            if frame_width > 720 and frame_height > 415:
                n_x, n_y = int(frame_width / 1.5), int(frame_height / 1.5)
                frame_width = n_x
                frame_height = n_y
            else:
                n_x, n_y = frame_width-50,frame_height-50
                frame_width = n_x
                frame_height = n_y
            pil_image = Image.fromarray(converted)
            
            FRAMES.append(make_image_from_fonts(pil_image,text=text,font_color=font_color,lower_target=lower_color,upper_target=upper_color,
                        remove_bg=remove_bg,new_bg_color=new_bg_color,frame_count=counter,reduce=REDUCE_PIXEL_GIF))
        elif ret:
            pass
        else:
            break
        counter += 1
        sub_counter += 1
        if counter >= frame_counter:
            break
    cap.release()
    if resize_new_file:
        FRAMES = [_.resize((frame_width-50, frame_height-50), Image.Resampling.NEAREST) for _ in FRAMES]
    else:
        FRAMES = [_ for _ in FRAMES]

    frame0 = FRAMES[0]
    frame0.save(f"{out}",format="GIF",save_all=True,append_images=FRAMES,duration=fps_seconds,loop=0)
    now_time = time_now()
    tempo_de_exec = now_time - init_time
    if DEBUG_INFO:
        print(f"[VideoReader with open-cv2]: time elapsed -> {tempo_de_exec}")
def remove_range_colorBitwiseNot(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        
                        )->Image.Image:

    _temp = create_surface(file)
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
    rgb = cv2.cvtColor(_temp, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_not(rgb, rgb, mask=mask) 

    return Image.fromarray(new_rgb, 'RGB').transpose(Image.Transpose.TRANSPOSE)

def insert_imageBitwiseNot(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        remove_bg: bool = True,
                        new_bg_surf: Surface | Image.Image = None
                        )->Image.Image:
    
    _temp = create_surface(file)
    if new_bg_surf:
        bg_temp = create_surface(new_bg_surf)
        if _temp.size < bg_temp.size:
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp = create_surface(_temp)
            bg_temp = create_surface(bg_temp)
        new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGR2RGB)
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)

    rgb = cv2.cvtColor(_temp, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_not(rgb, rgb, mask=mask)
    if not new_bg_surf:
        pass
    else:
        new_rgb = cv2.add(new_rgb, cv2.bitwise_not(new_bg,mask, mask=mask))
    return Image.fromarray(new_rgb).transpose(Image.Transpose.TRANSPOSE)

def glitchImageMask(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        new_bg_surf: Surface | Image.Image = None
                        )->Image.Image:
    """ Make a image with file image or surface, and a
        new_bg image to create a mask to glitch at all.
        Args:
            file ( pygame.Surface | PIL.Image.Image ): base file to insert a bg.
            lower_target ( list | numpy.array ): lower color range to pick.
            upper_targe ( list | numpy.array ): upper color range to pick.
            new_bg_surf ( pygame.Surface | PIL.Image.Image ): file to insert.
        Returns:
            PIL.Image.Image: Image 
    """
    _temp = create_surface(file)
    if new_bg_surf:
        bg_temp = create_surface(new_bg_surf)
        if _temp.size < bg_temp.size:
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp = create_surface(_temp)
            bg_temp = create_surface(bg_temp)
        new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGR2RGB)
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
    rgb = cv2.cvtColor(_temp, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_and(rgb, new_bg, mask=mask)
    if not new_bg_surf:
        pass
    else:
        new_bg = cv2.bitwise_and(new_bg, rgb)
        new_rgb = cv2.add(new_rgb, rgb+new_bg)
    return Image.fromarray(new_rgb).transpose(Image.Transpose.TRANSPOSE)
def insert_image_in_mask(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        new_bg_surf: Surface | Image.Image = None
                        )->Image.Image:
    """
    Insert a image in another by a mask choose by range color.
    Args:
        file ( pygame.Surface | PIL.Image.Image ): base file to insert a bg.
        lower_target ( list | numpy.array ): lower color range to pick.
        upper_targe ( list | numpy.array ): upper color range to pick.
        new_bg_surf ( pygame.Surface | PIL.Image.Image ): file to insert.

    Returns:
        PIL.Image.Image: Image 
    """
    _temp = create_surface(file)
    if new_bg_surf:
        bg_temp = create_surface(new_bg_surf)
        if _temp.size < bg_temp.size:
            
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp = create_surface(_temp)
            bg_temp = create_surface(bg_temp)
        new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGR2RGB)
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
    rgb = cv2.cvtColor(_temp, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_and(rgb, rgb, mask=mask)
    if not new_bg_surf:
        pass
    else:
        new_bg = cv2.bitwise_and(new_bg, new_bg, mask=mask)
        new_rgb = cv2.add(new_bg,rgb-new_rgb)
    return Image.fromarray(new_rgb).transpose(Image.Transpose.TRANSPOSE)


def insert_imageBitwiseAnd(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        remove_bg: bool = True,
                        new_bg_surf: Surface | Image.Image = None
                        )->Image.Image:
    
    _temp = create_surface(file)

    if new_bg_surf:
        bg_temp = create_surface(new_bg_surf)
        if _temp.size < bg_temp.size:
            
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp = create_surface(_temp)
            bg_temp = create_surface(bg_temp)

        new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGR2RGB)
    
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)

    rgb = cv2.cvtColor(_temp, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(rgb, lower_target, upper_target)
    #unmas = cv2.bitwise_not(mask)
    new_rgb = cv2.bitwise_not(rgb, rgb, mask=mask) if not new_bg_surf else cv2.bitwise_and(rgb, new_bg, mask=mask)
    #remove_range_colorBitwiseNot(file, lower_target, upper_target, True, mask).save("novo.png")
    return Image.fromarray(new_rgb).transpose(Image.Transpose.TRANSPOSE)


def make_image_from_fontsHASH(file,
                        font_family: str = "lucidaconsole", 
                        font_size: int = 12,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        font_color: tuple = (255,255,255),
                        text: str = "",
                        remove_bg: bool = False,
                        new_bg_color: tuple = (0,0,0),
                        frame_count: int = None,
                        reduce: int = None)->Image.Image:
    
    '''*make_image_from_fonts
            Takes a file object or PIL.Image object 
            with argument and some parameters to return a PIL.Image
            overwrite the pixels in range color between lower and
            upper target. 
            # Parameters
            
            \n\t( 
            - font_family: str, default="lucidaconsole".
            \n
            - font_size: int, default=12. 
            \n
            - font_color: tuple, default=(255,255,255).
            \n
            - lower_target: list, default=numpy.array([0,0,0]).
            \n
            - upper_target: list, default=numpy.array([45,45,45]).
            \n
            - text: str, default="10".
            \n
            - remove_bg: bool, default=False.
            \n
            - new_bg_color: tuple = (0,0,0).
            \n\t)->PIL.Image.Image'''
    
    global PIXEL_READ_COUNTER, PIXEL_READ_DICT, FRAMES_LENGTH_VIDEO_INFO
    PIXEL_READ_DICT = PIXEL_READ_DICT
    PIXEL_READ_COUNTER = PIXEL_READ_COUNTER
    sprite_group = Group()
    if type(file) == Image.Image:
        file = file.quantize(colors=QUANTIZE_IN_SURFACES).convert("RGB") if QUANTIZE_IN_SURFACES else file
    _img = Sprites_(_file=file)
    sprite_group.add(_img)
    size = _img.image.get_rect()[2:]
    arraysurf = Surface((size[0],size[1]), SRCALPHA)
    font_pygame = font.SysFont(font_family, font_size)
    texto = font_pygame.render(text if text else "", True, font_color)
    arraysurf.fill((0,0,0,0))
    sprite_group.draw(arraysurf)
    _tmp = surfarray.array3d(arraysurf)
    if DEBUG_INFO:
        print(f"[image:{file}] loaded in memory")
        init_time = time_now()
    hashmap = {}
    for y in range(1, int(size[1] / 2), PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][0]):
        hashmap[str(y)] = {}
        eixo_x_counter = 0
        for x in range(1, int(size[0] / 2), PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][1]):
            if _tmp[x][y][0] in range(lower_target[0],upper_target[0]) and _tmp[x][y][1] in range(lower_target[1],upper_target[1]) and _tmp[x][y][2] in range(lower_target[2],upper_target[2]):
                hashmap[str(y)][str(x)] = 1
                eixo_x_counter = 0
            elif eixo_x_counter == 0 and x >= int((size[0] / 2)/2):
                break
        eixo_x_counter = 0
        for x in range(int(size[0]/2), size[0], PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][1]):
            if _tmp[x][y][0] in range(lower_target[0],upper_target[0]) and _tmp[x][y][1] in range(lower_target[1],upper_target[1]) and _tmp[x][y][2] in range(lower_target[2],upper_target[2]):
                hashmap[str(y)][str(x)] = 1
                eixo_x_counter = 1
            elif eixo_x_counter == 0 and x >= int((size[0] / 2)*1.5):
                break
        if len(hashmap[str(y)]) > 1:
            pass
        else:
            hashmap.pop(str(y))
    for y in range(int(size[1]/2), size[1], PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][0]):
        hashmap[str(y)] = {}
        eixo_x_counter = 0 
        for x in range(1, int(size[0] / 2), PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][1]):
            if _tmp[x][y][0] in range(lower_target[0],upper_target[0]) and _tmp[x][y][1] in range(lower_target[1],upper_target[1]) and _tmp[x][y][2] in range(lower_target[2],upper_target[2]):
                hashmap[str(y)][str(x)] = 1
                eixo_x_counter = 1
            elif eixo_x_counter == 0 and x >= int((size[0] / 2)/2):
                break
        eixo_x_counter = 0
        for x in range(int(size[0]/2), size[0], PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][1]):
            if _tmp[x][y][0] in range(lower_target[0],upper_target[0]) and _tmp[x][y][1] in range(lower_target[1],upper_target[1]) and _tmp[x][y][2] in range(lower_target[2],upper_target[2]):
                hashmap[str(y)][str(x)] = 1
                eixo_x_counter = 1
            elif eixo_x_counter == 0 and x >= int((size[0] / 2) * 1.5):
                break
        if len(hashmap[str(y)]) > 1:
            pass
        else:
            hashmap.pop(str(y)) 
    chars_ = "" if not text else [letter for letter in text] # ░
    for a in hashmap.keys():
        for x in hashmap[a].keys():
            if remove_bg:
                draw.rect(arraysurf,new_bg_color, Rect(int(x), int(a), PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][1], PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][0])) 
            if text:
                _text = f"{chars_[randint(0, len(chars_)-1)]}"
                texto = font_pygame.render(_text, True, font_color)
                arraysurf.blit(texto, (int(x),int(a)))
    _tmp = surfarray.array3d(arraysurf)
    if DEBUG_INFO:
        end_time = time_now()
        if frame_count:
            print(f"{RED_COLOR}[frame: {frame_count} of {FRAMES_LENGTH_VIDEO_INFO}]{DEFAULT_COLOR}", end="")
        print(f"{GREEN_COLOR}[IMAGE READ AND OVERWRITED]{DEFAULT_COLOR} {end_time-init_time}")
    imagem_com_texto = Image.fromarray(_tmp)
    view = imagem_com_texto.transpose(Image.Transpose.TRANSPOSE)
    _img.kill()
    view = view.reduce(reduce) if reduce != None else view
    view = view.quantize(method=2,colors=QUANTIZE_IMAGES_VIDEO,dither=Image.Dither.RASTERIZE).convert('RGB') if QUANTIZE_IMAGES_VIDEO else view
    del(sprite_group)
    del(_img, arraysurf, font_pygame, texto, _tmp, imagem_com_texto, x, chars_, hashmap)
    return view

def main(file_dict: dict):
    if file_dict == "!":
        __help__()
        exit()
  
    if file_dict["GUI"]:
        pass

if __name__ == "__main__":
 
    insert_imageMaskWithMask('out/mapa_.png', [200,200,200], [255,255,255], new_bg_surf='out/gato_stealth.jpg').save("out/new_file.jpg")
    #glitchImageMask('out/mapa_.png', [200,200,200], [255,255,255], new_bg_surf='out/gato_stealth.jpg').save("out/new_file.jpg")
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    app = main(_file_)
    
