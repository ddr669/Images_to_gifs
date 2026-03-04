#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
from src import *

@time_function
def make_gif_with_img_func(file,file_name: str = 'out/new_file.gif',
                           over_img = None,
                           coord: list | tuple = [0,0],
                           function_draw = None,
                           frames_len: int = 60,
                           animation_speed: list = [0,1],
                           effect: bool = False,
                           **kwargs):
    frames = []
    direction = 0

    for a in range(0, frames_len):
        new_file = function_draw(file, **kwargs)
        frames.append(new_file)
    try:
        frame0 = frames[0]
        frame0.save(file_name, format="GIF", save_all=True, append_images=frames, duration=frames_len, loop=0)

    except AttributeError:
        print("Error")
        frames = [Image.fromarray(_) for _ in frames]
        frame0 = frames[0]
        frame0.save(file_name, format="GIF" ,save_all=True, append_images=frames, duration=frames_len, loop=0)

def main(file_dict: dict):
    Config_Variables.SHOW_BANNER = False
    if file_dict == "!":
        if Config_Variables.SHOW_BANNER:
            banner_help()
        exit()

    if file_dict["GUI"]:
        # TODO
        pass

if __name__ == "__main__":
    img = Image_class_module('out/car_reduce.png')
    img.update_image(img.image.resize((800, 420)))
    #blit_text_inrange(img, text="eduardo", loop=1, rm_bg=True)
    new = Image_class_module('out/gato_reduzido.png')
    start = [0, 255]
    end = [800, 255]
    make_gif_with_img_func(img, function_draw=blit_text_inrange)
    #img2 = Image_class_module(img.sobel_filter())
    #img2.save("out/teste2.png")

 #  img.blurr_image(9)
    img.image.save('out/teste01.png')
    print('done')
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    app = main(_file_)
   

