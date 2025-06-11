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
    ############# TEste ###################
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
    
        # FINALY!
    
    sprite_group.draw(arraysurf)
    _tmp = surfarray.array3d(arraysurf)
    IMG_CRU = _tmp
    IMG_CRU_RGB = cv2.cvtColor(IMG_CRU, cv2.COLOR_BGR2RGB)
    #IMG_CRU_RGB = IMG_CRU_RGB.transpose([1, 0, 2])
    _tmp = cv2.imread(file)
    
    #_tmp = cv2.cvtColor(_tmp, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(_tmp, cv2.COLOR_BGR2HSV)
    hsv_img = hsv_img.transpose([1, 0 ,2])
    # LEMBRAR hsv para verificar funciona ao contrario do rgb 
    #                               rgb = rgb 
    #                               hsv = b, g, r
    # Todo [ recv color select and calc the lower and target ]
    lower_target = np.array([20, 32, 170])
    target = np.array([50, 54, 226])
    chars_ = ["x", ";"] # ░
    ########################
    for a in range(1, size[1], 8):
        for x in range(1, size[0],6):
                # r, g, b unpack to pixel in [x][a]
                r,g,b = IMG_CRU_RGB[x][a]
                # if pixel have the color on range of lower to target draw text
                if r in range(lower_target[0], target[0]) and g in range(lower_target[1], target[1]) and b in range(lower_target[2],target[2]):
                    
                    ####### circulos para sobrescrever cor ######## 
                    if _remove_:
                        draw.circle(arraysurf,_new_color, (
                                    x,a
                                ), 4, 0) #IMG_CRU_RGB[x][a] 
                       
                    arraysurf.blit(texto, (x,a))

                _text = f"{chars_[randint(0, 1)]}"#{chars_[randint(0, 1)]}"
                texto = font_pygame.render(_text, True, _color_)
        

    # rotate
    IMG_CRU_RGB = IMG_CRU_RGB.transpose([1, 0, 2])
    # variable temp to save array3d of surface 
    _tmp = surfarray.array3d(arraysurf)
    #_tmp_01 = surfarray.array3d(_OFF_SET_PYGAME)
    #_bolinhas = cv2.cvtColor(_tmp_01, cv2.COLOR_BGR2RGB)
    #_bolinhas = _bolinhas.transpose([1, 0, 2])
    imagem_com_texto = cv2.cvtColor(_tmp, cv2.COLOR_BGR2RGB)
    imagem_com_texto = imagem_com_texto.transpose([1, 0, 2])
    # save the surface and img with text in the color selected 
    #cv2.imshow("image_cru", IMG_CRU_RGB)
    # show the normal image 
    view = imagem_com_texto
    # show the result of sum by two surface 
    #cv2.imshow("view_pygame",view)
    # wait for a key 
    #cv2.waitKey(0)
    if _to:
        cv2.imwrite(_to if _to else "out.jpg", view)
        #cv2.imwrite("bolinhas_01.jpg", _bolinhas)
        return _to
    ############## test End ##################
    else:
        return 1
    #####################################   
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


    #cv2_fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    
    
    # faz varias imagens com ascii random
    #for n in range(0, 120):
    #    _new_file = f"src/out_{n}.jpg"
    make_image_from_fonts("image_vermei.JPG", _to="testes000.jpg") #, _to="bionario.jpg")
    #for file in os_path("src"):
    #_ = os_path("src")
    
    #_ = f"src/{_[0]}"
    #print(_)
    #frame = cv2.imread(_)
    #_size = list(frame.shape)
    #del(_size[2])
    #_size.reverse()
    #video = cv2.VideoWriter("out/video_test001.mp4", cv2_fourcc, 6, _size)
    #for file in os_path("src"):
    #    _ = f"src/{file}"
    #    video.write(cv2.imread(_))
    #video.release()


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
    