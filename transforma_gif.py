#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
from src import *

Config_Variables.SHOW_BANNER = 1 # use this to *SHOW* the banner and help after terminate
Config_Variables.SHOW_BANNER = 0 # use this to avoid banner and help 
Debug.DEBUG_MODE = 0 # Use this to remove debug mode
Debug.DEBUG_MODE = 1 # use this to debug the program

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
    new = Image_class_module('out/gato_reduzido.png')
    start = [0, 255]
    end = [800, 255]
    make_gif_with_img_func(img, function_draw=blit_text_inrange)
    img.image.save('out/teste01.png')
    print('done')
    file = None
    try:
        test_args = argv[1]
        file = cmdline_verify(argv)
    except IndexError as Err:
        file = return_file_()
    app = main(file)
   

