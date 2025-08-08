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
        #self.image = scale(self.image, (320, 180))

        


# xxxxxxxxxxxxxxxxx
# make a texture to image with pygame.Surface
# from the given args (_font, _size, _from, _to, size:tuple=(20,20) repeat: bool=False, text: str= "xxx")
def make_image_from_fonts(file,
                        font_family: str = "lucidaconsole", 
                        font_size: int = 12,
                        lower_target: list = np.array([0,0,0]),
                        upper_target: list = np.array([25,25,25]),
                        save_to: str = None,
                        font_color: tuple = (255,255,255),
                        text: str = None,
                        remove_bg: bool = False,
                        new_bg_color: tuple = (0,0,0)) :
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

    font.init()
    font_pygame = font.SysFont(font_family, font_size)

    texto = font_pygame.render(text if text else "", True, font_color)
    arraysurf.fill((0,0,0,0))
    
        
    sprite_group.draw(arraysurf)
    _tmp = surfarray.array3d(arraysurf)
    IMG_CRU = _tmp
    IMG_CRU_RGB = cv2.cvtColor(IMG_CRU, cv2.COLOR_BGR2RGB)

    _tmp = cv2.imread(file)
    
    lower_target = lower_target#np.array([145, 130, 125]) if not lower_target.all() else lower_target # pra pegar o fundo do gato # grey 
    upper_target = upper_target#np.array([252, 239, 226]) if not upper_target.all() else upper_target # pra pegar o fundo do gato  # white

    chars_ = ["0", "1"] if not text else [letter for letter in text] # ░
    # todo: 
    #   algorithm to separate 1/4 of frame and multithread to process it
    #

    for a in range(1, size[1], 12):
        for x in range(1, size[0],8):
                r,g,b = IMG_CRU_RGB[x][a]
                if r in range(lower_target[0], upper_target[0]) and g in range(lower_target[1], upper_target[1]) and b in range(lower_target[2],upper_target[2]):
                    if remove_bg:
                        draw.circle(arraysurf,new_bg_color, (x,a), 4, 0) 

                    arraysurf.blit(texto, (x,a))
                # todo: a way to indentify the size of _text_ 
                # and resize the buffersize or spaces between
                _text = f"{chars_[randint(0, len(chars_)-1)]}"
                texto = font_pygame.render(_text, True, font_color)
        
    # rotate
    IMG_CRU_RGB = IMG_CRU_RGB.transpose([1, 0, 2])
    # variable temp to save array3d of surface 
    _tmp = surfarray.array3d(arraysurf)
    imagem_com_texto = cv2.cvtColor(_tmp, cv2.COLOR_BGR2RGB)
    imagem_com_texto = imagem_com_texto.transpose([1, 0, 2])
    
    view = imagem_com_texto
    
    cv2.imwrite(save_to if save_to else "out.jpg", view)
    return save_to
    

def save_as_gif(path: str = "src", out: str = "teste_01.gif"):
    ''' save files from path to save as gif in out '''
    files = os_path(path)
    frames = [Image.open(path+"/"+n) for n in files]
    frame0 = frames[0]
    frame0.save(f"out/{out}", save_all=True, append_images=frames, duration=90, loop=0, )
    
def floppy_images(path: str = "src",
                  count: int = 60,
                  file: str = "out_0.jpg"):
    ''' make a lot of images with edit config '''
    for n in range(0, count):
        _new_file = f"{path}/out_{n}.jpg"
        make_image_from_fonts(file, text="$#",save_to=_new_file)

def main(file_dict: dict):
    
    if file_dict == "!":
        __help__()
        exit()
  
    if file_dict["GUI"]:
        pass
 
    # END
if __name__ == "__main__":
    floppy_images(file="files/out_0.jpg")
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
    