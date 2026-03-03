
from PIL import Image, PngImagePlugin, JpegImagePlugin, ImageDraw, ImageFont
import cv2
import numpy as np
from sys import argv
from time import time
from pygame import Surface, surfarray, SRCALPHA, draw, Rect, image
from pygame import font as pyfont
from pygame.transform import scale
from pygame.sprite import Sprite, Group

from random import randint
from moviepy import AudioFileClip, ImageSequenceClip
PIXEL_READ_DICT = {'1': (6,4), '2': (8,6),     
                   '3': (8,4), '4': (12,8),     
                   '5': (16, 8), '6': (14,8),   
                   '7': (16, 12), '8': (24, 8), 
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

        global DEBUG_INFO, FRAMES_LENGTH_VIDEO_INFO, QUANTIZE_IMAGES_GIF, QUANTIZE_IMAGES_VIDEO
        
        cap = cv2.VideoCapture(file)
      
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
        
       
        global PIXEL_READ_COUNTER, PIXEL_READ_DICT, FRAMES_LENGTH_VIDEO_INFO
        PIXEL_READ_DICT = PIXEL_READ_DICT
        PIXEL_READ_COUNTER = PIXEL_READ_COUNTER
        sprite_group = Group()
        
        _img = Sprites_(_file=file)
        sprite_group.add(_img)
        size = file.image.size
        arraysurf = Surface((size[0],size[1]), SRCALPHA)
        font_pygame = pyfont.SysFont(font_family, font_size)
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
   

