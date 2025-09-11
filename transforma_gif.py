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

class Sprites_(Sprite):
    def __init__(self, _file: str | Image.Image = None,
                 color=(0,0,0,0),
                 height: int = None,
                 width: int = None
                ):
        super().__init__()
        
        if type(_file) == Image.Image:
            try:
                self.image = image.frombytes(_file.tobytes(), _file.size,  'RGBA')
                self.mode = "RGBA"
            except ValueError:
                self.image = image.frombytes(_file.tobytes(), _file.size, _tmp_img.mode)
                self.mode = _tmp_img.mode
        elif type(_file) == np.ndarray:
            _tmp_img = Image.fromarray(_file).convert()
            self.image = image.frombytes(_tmp_img.tobytes(), _tmp_img.size,_tmp_img.mode)
            self.mode = _tmp_img.mode
        else:
            self.image = image.load(_file)
        if width:
            draw.rect(self.image,color,Rect(0,0,width,height))
        self.rect = self.image.get_rect()    

def return_array(file: str):
    return cv2.imread(file, cv2.IMREAD_UNCHANGED)
    

def create_surface(file: str | Image.Image | Surface, size: list | tuple = None):
    sprite_group = Group()
    if type(file) == Surface:
        file = Image.fromarray(surfarray.array3d(file))
    if type(file) == str:
        file = Image.open(file).convert()
    
    if size:
        file.resize(size)
    _img = Sprites_(_file=file)
    mode = _img.mode
    if mode == 'RGBA':
        file_ = np.array(file)
        _temp = cv2.cvtColor(file_, cv2.COLOR_RGBA2BGRA)

    else:
        sprite_group.add(_img)
        size = _img.image.get_rect()[2:]
        arraysurf = Surface((size[0],size[1]), SRCALPHA)
        sprite_group.draw(arraysurf)
        _temp = surfarray.array3d(arraysurf)
        del _img, sprite_group, size, arraysurf
    return _temp, mode

def create_mask(file: Surface | Image.Image,
                lower_target: np.array = np.array([0,0,0]),
                upper_target: np.array = np.array([0,0,0])
                ):
    file_, mode_ = create_surface(file)
    mask = cv2.inRange(file_, lower_target, upper_target)
    return mask

def return_alpha_image(file: str):
    img_with_alpha = cv2.imread(file)
    try:
        b, g, r, alpha = cv2.split(img_with_alpha)
    except ValueError:
        new_ = cv2.cvtColor(img_with_alpha, cv2.COLOR_BGR2BGRA)
        b, g, r, alpha = cv2.split(new_)

    return cv2.merge([b,g,r,alpha]) 

def remove_range_color(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        
                        )->Image.Image:
    _temp = return_alpha_image(file)
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
    rgb = cv2.cvtColor(_temp, cv2.COLOR_BGRA2RGBA)
    mask = cv2.inRange(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_not(rgb,mask, mask=mask) 
    
    return Image.fromarray(rgb+new_rgb, 'RGBA').transpose(Image.Transpose.TRANSPOSE)
def insert_imageInCoord(file, over_file, coord: list | tuple = [0,0]) -> Image.Image:
    new_file = cv2.imread(over_file, cv2.IMREAD_UNCHANGED)
    file_m, mode_m = create_surface(file)
    kk_, mode_k = create_surface(new_file)
    tmp_ = Image.fromarray(file_m, mode=mode_m)
    new = Image.fromarray(kk_, mode=mode_k)
    tmp_.paste(kk_, coord)
    return tmp_

def insert_imageInCoordDeprecate(file: Surface | Image.Image,
                        new_file: Surface | Image.Image,
                        coord: list | tuple = [0,0],
                        remove_bg: bool = None,
                        lower_target: np.array = None,
                        upper_target: np.array = None
                        ) -> Image.Image:
    file_tmp, modeF = create_surface(file)
    file_= Image.fromarray(file_tmp, mode=modeF)
    new_file_tmp, modeN = create_surface(new_file)
    
    new_file = Image.fromarray(new_file_tmp, mode=modeN)

    if remove_bg:
        mask = create_mask(new_file_tmp, lower_target, upper_target)
        new_file = Image.fromarray(new_file_tmp, mode=modeN)
        layer = Image.new('RGBA', new_file.size, (0,0,0,0))
        layer.paste(new_file, (0,0))
        layer2 = layer.copy()
        layer2.putalpha(128)
        layer.paste(layer2, layer)
        #new_file.apply_transparency()
        layer.alpha_composite(layer,[coord[0], coord[1]], [0,0])
    file_.paste(new_file, coord)
    
    return file_.transpose(Image.Transpose.TRANSPOSE)

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
        print(_temp.size, bg_temp.size)
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
        new_rgb = cv2.add(new_bg,rgb - new_rgb)
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
    new_rgb = cv2.bitwise_not(rgb,mask, mask=mask)
    if not new_bg_surf:
        pass
    else:
        new_bg = cv2.bitwise_and(new_bg, rgb, mask=mask)
        new_rgb = cv2.add(new_rgb, new_bg)
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
    '''
    
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
    # 'out/gato_stealth.jpg'
    
    new_f = Image.fromarray(return_alpha_image('out/eduardo_luz.jpg'), mode="RGBA").transpose(Image.Transpose.TRANSPOSE)
    insert_imageInCoord(new_f, 'out/gato_stealth.jpg', (400,900)).save("out/new_file1.png")
   
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    app = main(_file_)
    
