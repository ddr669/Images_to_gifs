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
from os import listdir as os_path
###### Sprites #######
class Sprites_(Sprite):
    def __init__(self, color=(0,0,0,0), height: int = None, width: int = None,
                 _file: str = None):
        super().__init__()
        self.image = image.load(_file) if _file else Surface([width, height])
        
        if width:
            draw.rect(self.image,color,Rect(0,0,width,height))

        self.rect = self.image.get_rect()
        if self.rect[-1] >= 720 or self.rect[-2] >= 1024:
            self.image = scale(self.image, (720, 500))
            self.rect = self.image.get_rect()

# xxxxxxxxxxxxxxxxx
# make a texture to image with pygame.Surface
# from the given args (_font, _size, _from, _to, size:tuple=(20,20) repeat: bool=False, text: str= "xxx")
def make_image_from_fonts(file,
                        _font: str = "lucidaconsole", 
                        _size: int = 12,
                        _to: str = None,
                        size: tuple = None, 
                        _text: str = None,
                        _color_: tuple = (20,20,20),
                        _remove_: bool = False,
                        _new_color: tuple = (0,0,0)) :
    """
        file - file to edit
        _font - font-family 
        _size - font-size
        _to - !
        size - !
        _text - if a _text will type the text a lot of times
        _color_ - !
        _remore_ - to overwrite the color range to _color_

    """
    
    sprite_group = Group()
    _img = Sprites_(_file=file)
    sprite_group.add(_img)
    size = _img.image.get_rect()[2:]
    
    arraysurf = Surface((size[0],size[1]), SRCALPHA)
    _OFF_SET_PYGAME = Surface((size[0], size[1]), SRCALPHA)

    font.init()
    font_pygame = font.SysFont(_font, _size)
    texto = font_pygame.render(_text, True, _color_)
    arraysurf.fill((0,0,0,0))
    
        
    
    sprite_group.draw(arraysurf)
    _tmp = surfarray.array3d(arraysurf)
    IMG_CRU = _tmp
    IMG_CRU_RGB = cv2.cvtColor(IMG_CRU, cv2.COLOR_BGR2RGB)
    #IMG_CRU_RGB = IMG_CRU_RGB.transpose([1, 0, 2])
    _tmp = cv2.imread(file)
    
    
    hsv_img = cv2.cvtColor(_tmp, cv2.COLOR_BGR2HSV)
    hsv_img = hsv_img.transpose([1, 0 ,2])
    # LEMBRAR hsv para verificar funciona ao contrario do rgb 
    #                               rgb = rgb 
    #                               hsv = b, g, r
    # Todo [ recv color select and calc the lower and target ]

     
    lower_target = np.array([145, 130, 125]) # pra pegar o fundo do gato # grey 
    target = np.array([252, 239, 226]) # pra pegar o fundo do gato  # white

    #lower_target = np.array([20, 32, 170]) # vermelho # red
    #target = np.array([50, 54, 226]) # vermelho    # red

    chars_ = ["0", "1"] # ░
    # todo: 
    #   algorithm to separate 1/4 of frame and multithread to process it
    #

    for a in range(1, size[1], 8):
        for x in range(1, size[0],6):
                r,g,b = IMG_CRU_RGB[x][a]
                # if pixel have the color on range of lower to target draw text
                if r in range(lower_target[0], target[0]) and g in range(lower_target[1], target[1]) and b in range(lower_target[2],target[2]):
                    # circulos para sobrescrever cor - circle to overwrite the background color range
                    if _remove_:
                        draw.circle(arraysurf,_new_color, (x,a), 4, 0) 

                    arraysurf.blit(texto, (x,a))
                # todo: a way to indentify the size of _text_ 
                # and resize the buffersize or spaces between
                _text = f"{chars_[randint(0, 1)]}"
                texto = font_pygame.render(_text, True, _color_)
        

    # rotate
    IMG_CRU_RGB = IMG_CRU_RGB.transpose([1, 0, 2])
    # variable temp to save array3d of surface 
    _tmp = surfarray.array3d(arraysurf)
    
    imagem_com_texto = cv2.cvtColor(_tmp, cv2.COLOR_BGR2RGB)
    imagem_com_texto = imagem_com_texto.transpose([1, 0, 2])
    
    view = imagem_com_texto
    
    
    cv2.imwrite(_to if _to else "out.jpg", view)
    return _to
    
      
def read_dir_(path: str, ext: str = None):
    # to make the things izi, if you named the pics files with * img_0001.jpg * 
    # ( Optional : if you dont choose extension, will be necessary!)
    if ext and ext not in ["avi", "gif", "mp4", "mkv"]:
        print("search for files with extension: ", ext)
        
    else:   
        try:
            files = os_path(path)
            if len(files) == 1:
                print(files)
        except FileNotFoundError as Err:
            __help__()
            print("[!] path or file not Found!")
            return -1 
        except NotADirectoryError:
            print("[*] using file ", files)
            return files if len(files) > 1 else 0 
        
def save_as_video_():
    pass
def save_as_gif(path: str = "src", out: str = "teste_01.gif"):
    ''' save files from path to save as gif in out '''
    files = os_path(path)
    frames = [Image.open(path+"/"+n) for n in files]
    frame0 = frames[0]
    frame0.save(f"out/{out}", save_all=True, append_images=frames, duration=90, loop=0)
    
def floppy_images(path: str = "src",
                  count: int = 60,
                  file: str = "out_0.jpg"):
    ''' make a lot of images with edit config '''
    for n in range(0, count):
        _new_file = f"{path}/out_{n}.jpg"
        make_image_from_fonts(file, _to=_new_file)

def main(file_dict: dict):
    
    if file_dict == "!":
        __help__()
        exit()
    # INI 
    #print("file: ", file_dict)
    if file_dict["GUI"]:
        pass
    if file_dict["extension"]:
        read_dir_(_file_["path"], ext=file_dict["extension"])

    read_dir_(_file_["path"])
    return 0
    # END
if __name__ == "__main__":
    floppy_images(file="files/_image.jpeg")
    save_as_gif()
    print("[*] done.")

    input()
    _file_ = None
    #  TRY ARGS
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)

    except IndexError as Err:
        _file_ = return_file_()
        
    # END;RUN
   
    app = main(_file_) #  if _file_["path"] else main("!")
    