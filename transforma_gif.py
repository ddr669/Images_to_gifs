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
        def __init__(self, _file: str | Image.Image = None,
                    color=(0,0,0,0),
                    height: int = None,
                    width: int = None
                    ):
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

class WithPygame:
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
                FRAMES.append(WithPygame.make_image_from_fontsHASH(pil_image,text=text,font_color=font_color,lower_target=lower_color,upper_target=upper_color,
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
                        FRAMES.append(WithPygame.make_image_from_fontsHASH(pil_image,text=text,font_color=font_color,
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
    def return_surface(size, background_image: Sprites_ = None) -> Surface:
        surf =  Surface(size, SRCALPHA)
        sprite_group = Group()
        surf.fill((0,0,0,0))
        if background_image:
            if type(background_image) == Sprites_:
                sprite_group.add(background_image)
                sprite_group.draw(surf)
            else:
                surf.blit(background_image)
            sprite_group.empty()
        del background_image, sprite_group
        return surf
    def type_text_in_img(surface: Surface,
                        text: str = 'Hello,World!',
                        font_size: int = 12,
                        font_familly: str = 'Consola',
                        font_color: tuple | list = [0,0,0],
                        coord: list | tuple = [0,0])->Surface:
        _font = font.SysFont(font_familly, font_size)
        text_inplace = _font.render(text, True, font_color)
        surface.blit(text_inplace, coord)
        del _font, text_inplace
        return surface
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

    def create_surface(file: str | Image.Image | Surface, size: list | tuple = None) -> list[np.ndarray,str]:
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
        del file
        return _temp, mode
    def draw_function_font_and_filepaste(file,
                        over_file = None,
                        coord: list = [0,0],
                        tmp_file_size: list = [1024, 900],
                        speed: list = [0, 1],
                        direction: int = 0,
                        func = None, **kwargs) -> Image.Image:

            if coord[0] >= tmp_file_size[0]:
                direction = 1
            if coord[1] >= tmp_file_size[1]:
                direction = 1
                # down
        
            #print(coord)
            if coord[0] <= 0 and direction == 1:
                direction = 0
            if coord[1] <= 0 and direction == 1:
                direction = 0
            if direction == 1:
                coord[0] -= speed[0]
                coord[1] -= speed[1]
                new_file = insert_imageInCoord(file, over_file, coord[:2])
            else:
                coord[0] += speed[0]
                coord[1] += speed[1]
                new_file = insert_imageInCoord(file, over_file, coord[:2])

            if func:

                new_bg_file = Image.open(over_file).resize(tmp_file_size)
                if kwargs.get('entropy'):
                    
                    if int(kwargs.get('framec')) % int(kwargs.get('entropy')) == 0:
                        new_file = glitchImageMask(new_file, [255,255,255, 255], [255,255,255, 255], new_bg_file).transpose(Image.Transpose.TRANSPOSE).convert("RGB")
                
                if kwargs.get('stroke'):
                    stroke = kwargs.get('stroke')
                else:
                    stroke = None

                spt_sheet = Sprites_(new_file)
                if stroke:
                    text_file = WithPygame.return_surface(tmp_file_size, spt_sheet)
                    text_file2 = WithPygame.type_text_in_img(text_file, 'CUM', 91, 'impact', [0,0,0], [(tmp_file_size[0]/2),(tmp_file_size[1]/2)+stroke])
                    text_file3 = WithPygame.type_text_in_img(text_file, 'CUM', 91, 'impact', [0,0,0], [(tmp_file_size[0]/2),(tmp_file_size[1]/2)-stroke])
                    text_file4 = WithPygame.type_text_in_img(text_file, 'CUM', 91, 'impact', [0,0,0], [(tmp_file_size[0]/2)-stroke,(tmp_file_size[1]/2)])
                    text_file5 = WithPygame.type_text_in_img(text_file, 'CUM', 91, 'impact', [0,0,0], [(tmp_file_size[0]/2)+stroke,(tmp_file_size[1]/2)])
                    text_file = WithPygame.type_text_in_img(text_file, 'CUM', 90, 'impact', [255,255,255], [tmp_file_size[0]/2,tmp_file_size[1]/2])
                    
                    aimeudeu = Image.fromarray(surfarray.array3d(text_file)).transpose(Image.Transpose.TRANSPOSE)
                    aimeudeu2 = Image.fromarray(surfarray.array3d(text_file2)).transpose(Image.Transpose.TRANSPOSE)
                    aimeudeu3 = Image.fromarray(surfarray.array3d(text_file3)).transpose(Image.Transpose.TRANSPOSE)
                    aimeudeu4 = Image.fromarray(surfarray.array3d(text_file4)).transpose(Image.Transpose.TRANSPOSE)
                    aimeudeu5 = Image.fromarray(surfarray.array3d(text_file5)).transpose(Image.Transpose.TRANSPOSE)
                    
                    new_file.paste(aimeudeu4, coord[2:])
                    new_file.paste(aimeudeu5, coord[2:])
                    new_file.paste(aimeudeu2, coord[2:])
                    new_file.paste(aimeudeu3, coord[2:])
                    new_file.paste(aimeudeu, coord[2:])
                    
            del aimeudeu, aimeudeu2, spt_sheet, new_bg_file, coord, tmp_file_size, text_file, text_file2
            return new_file
    



def create_mask(file: Surface | Image.Image,
                lower_target: np.array = np.array([0,0,0]),
                upper_target: np.array = np.array([0,0,0])
                ) -> cv2.Mat:
    file_, mode_ = WithPygame.create_surface(file)
    mask = cv2.inRange(file_, lower_target, upper_target)
    del file_, mode_, lower_target, upper_target, file
    return mask

def return_alpha_image_bgr(file: str) -> cv2.Mat:
    img_with_alpha = return_array(file)
    try:
        b, g, r, alpha = cv2.split(img_with_alpha)
    except ValueError:
        new_ = cv2.cvtColor(img_with_alpha, cv2.COLOR_BGR2BGRA)
        b, g, r, alpha = cv2.split(new_)
    
    new_array = cv2.merge([b,g,r,alpha])
    return new_array

def return_alpha_image_rgb(file: str) -> cv2.Mat:
    img_with_alpha = return_array(file)
    try:
        r, g, b, alpha = cv2.split(img_with_alpha)
    except ValueError:
        new_ = cv2.cvtColor(img_with_alpha, cv2.COLOR_BGR2RGBA)
        r, g, b, alpha = cv2.split(new_)
    
    new_array = cv2.merge([r,g,b,alpha])
    return new_array

def remove_range_color_alpha(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0,255]),
                        upper_target: list = np.array([45,45,45,255]),
                        )->Image.Image:
    _temp = return_alpha_image_bgr(file)
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
    rgb = cv2.cvtColor(_temp, cv2.COLOR_BGRA2RGBA)
    mask = cv2.inRange(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_not(rgb,rgb, mask=mask) 
    return Image.fromarray(new_rgb, 'RGBA')

def insert_imageInCoord(file, over_file, coord: list | tuple = [0,0]) -> Image.Image:
    new_file = return_alpha_image_rgb(over_file)
    tmp_ = return_alpha_image_rgb(file)
    new_file_pil = Image.fromarray(new_file, 'RGBA')
    mask = new_file_pil.split()[3]
    tmp_pil = Image.fromarray(tmp_, 'RGBA')
    tmp_pil.paste(new_file_pil, coord, mask=mask)
    del tmp_, mask, new_file_pil, new_file
    return tmp_pil


def insert_imageBitwiseNot(file: Surface | Image.Image,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([45,45,45]),
                        remove_bg: bool = True,
                        new_bg_surf: Surface | Image.Image = None
                        )->Image.Image:
    _temp = WithPygame.create_surface(file)
    if new_bg_surf:
        bg_temp = WithPygame.create_surface(new_bg_surf)
        if _temp.size < bg_temp.size:
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp = WithPygame.create_surface(_temp)
            bg_temp = WithPygame.create_surface(bg_temp)
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
    _temp, mode_tmp = WithPygame.create_surface(file)
    if new_bg_surf:
        bg_temp, mode_new = WithPygame.create_surface(new_bg_surf)
        if _temp.size < bg_temp.size:
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp, mode_tmp = WithPygame.create_surface(_temp)
            bg_temp, mode_new = WithPygame.create_surface(bg_temp)
        if mode_new == 'RGB':
            new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGR2RGB)
        elif mode_new == 'RGBA':
            new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGRA2RGBA)

    if mode_tmp == 'RGB':
         rgb = cv2.cvtColor(_temp, cv2.COLOR_BGR2RGB)
    elif mode_tmp == 'RGBA':
        rgb = cv2.cvtColor(_temp, cv2.COLOR_BGRA2RGBA)

    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
   
    mask = cv2.inRange(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_and(rgb, new_bg, mask=mask)
    if not new_bg_surf:
        pass
    else:
        new_bg = cv2.bitwise_and(new_bg, rgb)
        new_rgb = cv2.add(new_rgb, rgb+new_bg)
    del new_bg, mask, rgb, lower_target, upper_target, bg_temp, mode_new, mode_tmp, _temp
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
    _temp = WithPygame.create_surface(file)
    if new_bg_surf:
        bg_temp = WithPygame.create_surface(new_bg_surf)
        
        if _temp.size < bg_temp.size:    
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp = WithPygame.create_surface(_temp)
            bg_temp = WithPygame.create_surface(bg_temp)
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
    
    _temp = WithPygame.create_surface(file)
    if new_bg_surf:
        bg_temp = WithPygame.create_surface(new_bg_surf)
        if _temp.size < bg_temp.size:
            _temp = Image.open(file).convert()
            bg_temp = Image.open(new_bg_surf).convert()
            bg_temp = bg_temp.resize(_temp.size)
            _temp = WithPygame.create_surface(_temp)
            bg_temp = WithPygame.create_surface(bg_temp)
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
def return_array(file: str):
    return cv2.imread(file, cv2.IMREAD_UNCHANGED)
   


def make_gif_with_img_func(file,file_name: str = 'out/new_file.gif',
                           over_img = None,
                           coord: list | tuple = [0,0],
                           function_draw = None,
                           frames_len: int = 90,
                           animation_speed: list = [0,1],
                           effect: bool = False,
                           **kwargs):
    FRAMES = []
    tmp_file_size = Image.open(file).size
    direction = 0
    for a in range(0, frames_len):
        if function_draw:
            new_file = function_draw(file,
                                     over_img,
                                     coord,
                                     tmp_file_size,
                                     animation_speed,
                                     direction,
                                     effect, entropy=kwargs.get('entropy'), framec=a, stroke=kwargs.get('stroke'))
        else:
            new_file = function_draw(file, over_img, coord, tmp_file_size, animation_speed, direction, effect)
        FRAMES.append(new_file)
       
    frame0 = FRAMES[0]
    frame0.save(file_name, format="GIF", save_all=True, append_images=FRAMES, duration=frames_len, loop=0)
    del frame0, tmp_file_size, direction, function_draw, FRAMES

def main(file_dict: dict):
    if file_dict == "!":
        __help__()
        
        exit()
  
    if file_dict["GUI"]:
        pass

if __name__ == "__main__":
    #remove_range_color_alpha('out/new_file_alpha.png', [0,0,0,255], [10,10,10,255]).save('out/removido.png')
    #insert_imageInCoord('out/eduardo_luz.jpg', 'out/removido.png', [950,400]).save('out/new_file2.png')
    Image.open('out/eduardo_luz.jpg').convert('RGB').resize([1200, 900]).save('out/resize_img.jpg')
    Image.open('out/removido.png').convert('RGBA').resize([400, 180]).save("out/gato_reduzido.png")
    
    make_gif_with_img_func('out/resize_img.jpg', 'out/porfavor_funfa.gif', 'out/gato_reduzido.png', [0,0,0,0], WithPygame.draw_function_font_and_filepaste, 90, [25,20], True, entropy=24, stroke=10)

    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    app = main(_file_)
    
