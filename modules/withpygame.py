
from PIL import Image, PngImagePlugin, JpegImagePlugin, ImageDraw, ImageFont
import cv2
import numpy as np
from sys import argv
from time import time
#from ..src.config_variables import *
from pygame import Surface, surfarray, SRCALPHA, font, draw, Rect, image
from pygame.transform import scale
from pygame.sprite import Sprite, Group

from random import randint
from moviepy import AudioFileClip, ImageSequenceClip
PIXEL_READ_DICT = {'1': (6,4), '2': (8,6),      # more accurate between pixel read but worst in speed (takes a lot of time)
                   '3': (8,4), '4': (12,8),     # I recommend something between 3 and 4
                   '5': (16, 8), '6': (14,8),   # this is for perfomace and less accurace
                   '7': (16, 12), '8': (24, 8), # NO ACCURACE
                   '9': (24, 16), '10': (64, 24)}
REDUCE_PIXEL_GIF:int = 0
PIXEL_READ_COUNTER:int   = 4        # Default 4
QUANTIZE_IN_SURFACES:int = None     # Warning!
QUANTIZE_IMAGES_GIF:int  = 126      # Default 186 (0 -> 255): from lower bitmap to better 
QUANTIZE_IMAGES_VIDEO:int= None     # Default None
FRAMES_LENGTH_VIDEO_INFO = 0        # Default 0 -> change as a file is set
#
REDUCE_PIXEL_GIF:int     = None    # Recommended but not need, 2 is fine to gif
REDUCE_PIXEL_VIDEO:int   = None     # Not recommended
FRAME_TO_SKIP = 188 # cannot be 1
#                
QUANTIZE_IMAGES_GIF:int  = 126  

def time_function(func):
    #_mem = tracemalloc.start()
    #mem_calc = lambda x, y: (x / (1024*1024), y / (1024*1024))
    def wrapper(*args, **kwargs):
        start = time()


        print(f"[started func: {func.__qualname__}].") #current memory {curr:8.f}MB; peak: {peak:8.f}MB.")
        
        try:
            return func(*args, **kwargs)
        finally:
            dt_ms = time() - start
            #curr, peak = mem_calc(tracemalloc.get_traced_memory())

            print(f"[func: {func.__qualname__}]: {dt_ms:.8f} ms.")
            #print(f"[func usage memory]: current: {curr:8.f}MB; peak: {peak:8.f}MB.")
    
    #tracemalloc.clear_traces()
    return wrapper

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
                try:
                    self.image = image.load(_file)
                except TypeError:
                    #_tmp_img = Image.fromarray(_file).convert()
                    self.image = image.frombytes(_file.image.tobytes(), _file.image.size, _file.image.mode)


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
        
        cap = cv2.VideoCapture(file)
       # if path_exist(file):
       #     pass
       # else:
       #     raise FileNotFoundError(f"\n\rFile {file} doesn't exist in actual path: \n\r{GETPWD()}")
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

        
    def make_video_from_video_blitText(
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
                            new_bg_color: tuple = None,
                            ):
        '''
        Takes a file and make another using cv2.VideoCapture() ND moviepy and passing through
        editing az asked in make_image_from_font() until frames equals frame_counter or video_size
        nd save az mp4|AMV|avi file format.
        '''
        global FRAMES_LENGTH_VIDEO_INFO
        global DEBUG_INFO, FRAME_TO_SKIP
        
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
    
        if type(FRAMES) == dict:
            frames = [np.array(_) for _ in FRAMES.values()]
        else:
            frames = [np.array(_) for _ in FRAMES]
        scene = ImageSequenceClip(frames, fps=video_framerateps)
        audioclip = AudioFileClip(file)
        audioclip.duration = scene.duration
        scene.audio = audioclip
        scene.write_videofile(out)
        
        del(FRAMES, scene, frames, audioclip, cap, counter, sub_counter)
        return 0
    
    def return_surface(size, background_image: Sprites_ = None) -> Surface:
        '''
        Using pygame to return a surface with a Sprite loaded in background.
        Args:
            size: tuple | list,
            background_image: Sprites_ = None
        Returns:
            pygame.Surface
        '''
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
        '''
        Using pygame to blit text in coords
        Args:
            surface (pygame.Surface): pygame surface.
            text (str) = "Hello,World!": text to blit.
            font_size (int) = 12: font size.
            font_familly (str) = 'Consola': font familly.
            font_color ( tuple | list ) = [0,0,0]: font color.
            coord ( list | tuple ) = [0,0]: coordinate to blit text in image.
        Returns:
            pygame.Surface
        '''
        _font = font.SysFont(font_familly, font_size)
        text_inplace = _font.render(text, True, font_color)
        surface.blit(text_inplace, coord)
        del _font, text_inplace
        return surface
    @time_function
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
        
        '''
                Takes a file object or PIL.Image object 
                with argument and some parameters to return a PIL.Image
                overwrite the pixels in range color between lower and
                upper target. ( DEPRECATE ) 
        '''
        
        global PIXEL_READ_COUNTER, PIXEL_READ_DICT, FRAMES_LENGTH_VIDEO_INFO
        PIXEL_READ_DICT = PIXEL_READ_DICT
        PIXEL_READ_COUNTER = PIXEL_READ_COUNTER
        sprite_group = Group()
        
        _img = Sprites_(_file=file)
        sprite_group.add(_img)
        size = file.image.size
        arraysurf = Surface((size[0],size[1]), SRCALPHA)
        font_pygame = font.SysFont(font_family, font_size)
        texto = font_pygame.render(text if text else "", True, font_color)
        arraysurf.fill((0,0,0,0))
        sprite_group.draw(arraysurf)
        _tmp = surfarray.array3d(arraysurf)
        
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
        chars_ = "" if not text else [letter for letter in text] 
        for a in hashmap.keys():
            for x in hashmap[a].keys():
                if remove_bg:
                    draw.rect(arraysurf,new_bg_color, Rect(int(x), int(a), PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][1], PIXEL_READ_DICT[str(PIXEL_READ_COUNTER)][0])) 
                if text:
                    _text = f"{chars_[randint(0, len(chars_)-1)]}"
                    texto = font_pygame.render(_text, True, font_color)
                    arraysurf.blit(texto, (int(x),int(a)))
        _tmp = surfarray.array3d(arraysurf)
       
        imagem_com_texto = Image.fromarray(_tmp)
        view = imagem_com_texto.transpose(Image.Transpose.TRANSPOSE)
        _img.kill()
        view = view.reduce(reduce) if reduce != None else view
        view = view.quantize(method=2,colors=QUANTIZE_IMAGES_VIDEO,dither=Image.Dither.RASTERIZE).convert('RGB') if QUANTIZE_IMAGES_VIDEO else view
        del(sprite_group)
        del(_img, arraysurf, font_pygame, texto, _tmp, imagem_com_texto, x, chars_, hashmap)
        return view
    
    def create_surface(file: str | Image.Image | Surface, size: list | tuple = None) -> list[np.ndarray,str]:
        '''
        Take a file like str | Image.Image or Surface and return a array
        like list[surface: np.ndarray, mode: str] 
        Mode is if the image is RGB or RGBA
        Args:
            file ( str | PIL.Image.Image | pygame.Surface): Image file.
            size ( list | tuple ) = None: Surface size.
        Returns:
            list[np.ndarray, str]: list[0] -> Image array, list[1] -> Image mode.

        '''
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
   
    def insert_imageBitwiseAnd(file: Surface | Image.Image,
                            lower_target: list = np.array([0,0,0]),
                            upper_target: list = np.array([45,45,45]),
                            remove_bg: bool = True,
                            new_bg_surf: Surface | Image.Image = None
                            )->Image.Image:
        
        _temp,mode = WithPygame.create_surface(file)
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
    

