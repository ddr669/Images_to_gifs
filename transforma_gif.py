#!/bin/venv python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
###################
from PIL import Image
import cv2
import numpy as np
from sys import argv
from pygame import Surface, surfarray, SRCALPHA, font, draw, Rect, image
from pygame.transform import scale
from pygame.sprite import Sprite, Group
from cmdline_verify import cmdline_verify
from cmdline_verify import __help__, return_file_

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
def make_image_from_fonts(file, _font: str = "lucidaconsole", 
                        _size: int = 6, _from = None,
                        _to = None, size: tuple = None, 
                        repeat: bool = True, _text: str = "▒",
                        _test_: bool = False,
                        _color_: tuple = (0,0,0), _colorkey_: tuple = (0,0,0) ) :
    ############# TEste ###################
    sprite_group = Group()
    _img = Sprites_(_file=file)
    sprite_group.add(_img)
    size = _img.image.get_rect()[2:]
    
    arraysurf = Surface((size[0],size[1]), SRCALPHA)

    font.init()
    font_pygame = font.SysFont(_font, _size)
    texto = font_pygame.render(_text, True, _color_)
    arraysurf.fill((0,0,0,0))
    
        # FINALY!
    sprite_group.draw(arraysurf)
    _tmp = surfarray.array3d(arraysurf)
    IMG_CRU = _tmp
    IMG_CRU_RGB = cv2.cvtColor(IMG_CRU, cv2.COLOR_BGR2RGB)
    #IMG_CRU_RGB = IMG_CRU_RGB.transpose([1, 0, 2])

    hsv_img = cv2.cvtColor(_tmp, cv2.COLOR_BGR2HSV)
    hsv_img = hsv_img.transpose([1, 0 ,2])
    # LEMBRAR hsv para verificar funciona ao contrario do rgb 
    #                               rgb = rgb 
    #                               hsv = b, g, r
    lower_target = np.array([20, 32, 170])
    target = np.array([50, 54, 226])
    
  
    for a in range(1, size[1], 4):
        for x in range(1, size[0], 5):
                r,g,b = IMG_CRU_RGB[x][a]
                #print(r,g,b)
                if r in range(lower_target[0], target[0]) and g in range(lower_target[1], target[1]) and b in range(lower_target[2],target[2]):
                    arraysurf.blit(texto, (x,a))
    IMG_CRU_RGB = IMG_CRU_RGB.transpose([1, 0, 2])
    _tmp = surfarray.array3d(arraysurf)
    imagem_com_texto = cv2.cvtColor(_tmp, cv2.COLOR_BGR2RGB)
    imagem_com_texto = imagem_com_texto.transpose([1, 0, 2])

    cv2.imshow("image_cru", IMG_CRU_RGB)

    view = imagem_com_texto
    cv2.imshow("view_pygame",view)

    cv2.waitKey(0)
    #cv2.imwrite(_to if _to else "out.jpg", img_bgr)
    ############## test End ##################
    return 1
    #####################################
def read_dir_(path: str, ext: str = None):
    # to make the things izi, if you named the pics files with * img_0001.jpg * 
    # ( Optional : if you dont choose extension, will be necessary!)
    if ext:
        print("search for files with extension: ", ext)
        
    else:   
        try:
            file = open(path, "r")
        except FileNotFoundError as Err:
            __help__()
            print("[!] path or file not Found!")
            exit()
    

def main(file_dict: dict):
    
    if file_dict == "!":
        __help__()
        exit()
    # INI 
    print(file_dict)
    if file_dict["extension"]:
        read_dir_(_file_["path"], ext=file_dict["extension"])

    read_dir_(_file_["path"])
    return 0
    # END
if __name__ == "__main__":
    #  TRY ARGS
    make_image_from_fonts("image_vermei.JPG", _to="tmp_9919.jpg")
    input()
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    # END;RUN
   
    app = main(_file_) if _file_["path"] else main("!")
    