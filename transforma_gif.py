#!/bin/venv python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
###################
from PIL import Image
import cv2
from sys import argv
from pygame import Surface, surfarray, SRCALPHA, font, draw, Rect
from cmdline_verify import cmdline_verify
from cmdline_verify import __help__, return_file_

# xxxxxxxxxxxxxxxxx
# make a texture to image with pygame.Surface
# from the given args (_font, _size, _from, _to, size:tuple=(20,20) repeat: bool=False, text: str= "xxx")
def make_image_from_fonts(_font: str = "lucidaconsole", 
                        _size: int = 12, _from = None,
                        _to = None, size: tuple = (600,600), 
                        repeat: bool = True, _text: str = "Vocês são gays!",
                        _test_: bool = True,
                        _color_: tuple = (0,0,0) ) :
    
    if _test_:
        arraysurf = Surface(size, SRCALPHA)
        font.init()
        font_pygame = font.SysFont(_font, _size)
        texto = font_pygame.render(_text, True, _color_)
        arraysurf.fill((0,0,0))
        for a in range(0, 600, 25):
            draw.line(arraysurf, (255,255,255), (a, 0), (a, 1200))
            
        re = [((0,400),(600, 200)), ((0,0),(600, 200)), ((0,200),(600, 200))]
        co = [(255,0,0), (0,255,0), (0,0,255)]
        for a in range(0, 3):
            draw.rect(arraysurf, co[a], re[a], 0)
        if repeat:
            for y in range(0, size[1], _size):
                for x in range(0, size[0], len(_text)*7):
                    arraysurf.blit(texto, (x, y))
        # FINALY!
        
        view = surfarray.array3d(arraysurf)

        view = view.transpose([1, 0 , 2])
        img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
        cv2.imshow("image",img_bgr)

        cv2.waitKey(0)
        cv2.imwrite("out.jpg", img_bgr)
    return 1

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
    make_image_from_fonts()
   
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    # END;RUN
   
    app = main(_file_) if _file_["path"] else main("!")
    