#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-

from time import sleep, time

import tracemalloc
from sys import stdout, argv as args
from typing import Any

BOLD_HIGH = lambda x: f"\033[1m{x}\033[0m"
DARK_HIGH = lambda x: f"\033[2m{x}\033[0m"
ITALIC_HI = lambda x: f"\033[3m{x}\033[0m"

BLACK_RANGE_COLOR    = {"lower_target"  : [0,0,0],       "upper_target": [55,55,55]}
WHITE_RANGE_COLOR    = {"lower_target"  : [200,200,200], "upper_target": [255,255,255]}
BLUE_RANGE_COLOR     = {"lower_target"  : [50,50,180],   "upper_target": [150,150,255]}
RED_RANGE_COLOR      = {"lower_target"  : [180, 50, 50], "upper_target": [255, 150, 150]}
GREEN_RANGE_COLOR    = {"lower_target"  : [50, 180, 50], "upper_target": [150, 255, 150]}

COLOR_SCHEME_DICT    = {"black": BLACK_RANGE_COLOR,
                        "white": WHITE_RANGE_COLOR,
                        "blue": BLUE_RANGE_COLOR,
                        "red": RED_RANGE_COLOR,
                        "green": GREEN_RANGE_COLOR,
                        }

BOLD_HIGH = lambda x: f"\033[1m{x}\033[0m"
ITALIC_HIGH = lambda x: f"\033[3m{x}\033[0m"
SHADOW_HIGH = lambda x: f"\033[2m{x}\033[0m"

BANNER = [" ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁"]
BANNER.append("▕\033[0;37;41m▒▒▒▒▒▒▒▒▒▒▒▒▒▒\033[0;30;47m░░░░░\033[0;37;41m▒▒▒▒▒▒▒\033[1;37;40m░░░░\033[0;37;41m▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\033[0;31;40m░░░\033[0;0;0m▏")
BANNER.append("▕\033[0;37;42m▒▒▒\033[0;0;0m(‾)\033[0;37;42m▒▒▒▒▒▒▒▒\033[0;30;47m░░░░░\033[0;37;42m▒▒▒▒▒▒▒\033[1;37;40m░░░░\033[0;37;42m▒▒▒▒▒\033[0;0;0m/‾/\033[0;37;42m▒▒▒▒▒▒▒▒\033[0;31;40m░░░░\033[0;0;0m▏")
BANNER.append("▕\033[0;37;44m▒▒\033[0;0;0m/ / ‾_ `__‾\\/‾‾‾ `/‾__‾`/‾_‾\\\033[0;37;44m▒▒\033[0;0;0m/  _ /‾__‾\\\033[0;37;44m▒\033[0;31;40m░░░░░\033[0;0;0m▏")
BANNER.append("▕\033[0;30;47m▒\033[0;0;0m/ / /\033[0;30;47m▒\033[0;0;0m/ /\033[0;30;47m▒\033[0;0;0m/ / /\033[0;30;47m▒\033[0;0;0m/ / /\033[0;30;47m▒\033[0;0;0m/ / /__/\033[0;30;47m▒▒\033[0;0;0m/ /\033[0;30;47m▒\033[0;0;0m/ /\033[0;30;47m▒\033[0;0;0m/ /\033[0;31;40m░░░░░░\033[0;0;0m▏")
BANNER.append("▕\033[0;30;47m\033[0;0;0m/_/_/\033[0;30;47m▒\033[0;0;0m/_/\033[0;30;47m▒\033[0;0;0m/_/\\__,_/\\_ , /\\ __/\033[0;30;47m▒▒▒\033[0;0;0m\\__/\\_ __/\033[0;31;40m░░░░░░░\033[0;0;0m▏")
BANNER.append("▕\033[0;30;47m▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░\033[0;0;0m/___/\033[0;30;47m▒▒░░░░▒▒\033[0;31;40m░░░░░░░░░░░░░░░░░░\033[0;0;0m▏")
BANNER.append("▕▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒▒▒\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏")
BANNER.append("▕▒▒▒▒▒▒▒▒\033[1;37;40m/‾\033[0;0;0m_‾_‾\033[1;37;40m/‾‾‾\033[0;0;0m/‾__‾‾/\033[0;0;0m\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏")
BANNER.append("▕▒▒▒▒▒▒▒\033[1;37;40m/ /\033[0;0;0m __ \033[1;37;40m/ /\033[0;0;0m/ /_\033[0;0;0m\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏")
BANNER.append("▕▒▒▒▒▒▒/ /\033[0;0;0m_\033[1;37;40m/ // // __/\033[0;0;0m\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏")
BANNER.append("▕(‾)\033[0;0;0m▒▒▒\033[1;37;40m\\____/___/_/\033[1;37;40m░░░░░░░░░░░░░\033[0;0;0mBy:__DDr669__\033[1;37;40m░░░░░░\033[0;0;0m▏")
BANNER.append("▕▒▒▒▒▒▒▒▒▒\033[1;37;40m ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏")
BANNER.append(" ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")

OPTIONS = []
OPTIONS.append(f"{BOLD_HIGH('GUI OPTIONS')}")
OPTIONS.append("-"*len('GUI_OPTIONS'))
OPTIONS.append(f"{DARK_HIGH('These options work alone in GUI mode')}")
OPTIONS.append(f"{DARK_HIGH('but with other options like --out or -o')}")
OPTIONS.append(f"{DARK_HIGH('run in CD/CLI mode and save. <DEFAULT new_filename=new_file.png>')}")
OPTIONS.append(f"\t{DARK_HIGH('-g or --gui')} - entry in GUI mode.")
OPTIONS.append(f"\n{BOLD_HIGH('edit-functions')}\n{str('*'*len('edit-functions'))}")
OPTIONS.append(f"\t{BOLD_HIGH('--remove-color')} - remove a color in range between. {DARK_HIGH('<DEFAULT COLOR_RANGE=black>')}")
OPTIONS.append(f"\t\t{DARK_HIGH('use with options --color-range=[10,10,10],[25,25,25]')}")
OPTIONS.append(f"\t\t{DARK_HIGH('default new_background_color=(0,255,0)')} # {BOLD_HIGH('green')}")
OPTIONS.append(f"\t{BOLD_HIGH('--apply-alpha')} - apply transparency to a image. {DARK_HIGH('<DEFAULT COLOR_REMOVE=white>')}")
OPTIONS.append(f"\t\t{DARK_HIGH('quick-mode:')} transforma_gif.py file.png --save new_file.png --apply-alpha black")
OPTIONS.append(f"\t\t\t{DARK_HIGH('HINT: look for another color range in cmdline_verify.py')}")

black_color_rgb = (0,0,0)
white_color_rgb = (255,255,255)
gray_color_rgb = (75,75,75)

default_font_path = str("c:\\WINDOWS\\Fonts\\CHARLEMAGNESTD-BOLD.OTF")


KWARGS_DICT = {
    
    'save_as':'new_file01',     # save_as: str = 'new_file01' ( takes orig. extension or function method. )
    'framecounter': 0,          # int = 0 ( video lenght if not given will take all the lenght of orig. )
    'framerate': 0,               # int = 0 ( in video or gif automatic select 24 frameper seconds. )
    'remove_bg': False,         # bool | int = False
    'new_bgcolor': (0,0,0,0),   # np.ndarray(3 or 4) | list = [0,0,0]
    'lower_target': None,       # np.ndarray(3) | list = [0,0,0]
    'upper_target': None,       # np.ndarray(3) | list = [0,0,0]
    'coord': None,              # coord behave aways as txt_pos, coord
    'resize': False,            # tuple | list = (40,40)
    'effect': False,            # somethimes a draw_function ask for effects bool ( true or false )
    'animation_speed': None,    # * goes with draw_function ( animation through video )
    'function_draw': None,      # animation function ( module pre made function or handmade )
    'text': None,
    'interval': None,           # * goes with draw_function ( animation through video )
    'font-color': black_color_rgb,
    'font-size': 28,            #   
    'font-familly': default_font_path,  # 
    'size': None,               # 
    'width': None,              # same as size but sometimes goes different
}

def animation_cmd(banner: list[str]):
    """
    just a ascii animation before ascii main banner.
    * invisible ascii char, unknown behavor.
    >>> animation_cmd()
    ... 
    """
    width = len(banner[0])
    height = len(banner)
    print()
    # draw (*) verticaly upside down 
    for h in range(0, height):
        for w in range(0, width):
            # caution with the invisible emoji
            sleep(0.000000001)
            stdout.write("‍*")
            stdout.flush()
        sleep(0.0000001)
        stdout.write('\n')
        stdout.flush()
    # draw (banner) verticaly downside up
    for _ in range(h, -1, -1):
        sleep(0.0000005)
        stdout.write('\033[F'*2)
        stdout.flush()
        sleep(0.05)
        stdout.write(banner[_]+'\n')
        stdout.flush()
    stdout.write('\n\r' * (h + 2))
    stdout.flush()

def anima_options(options: list[str]):
    """
        draw text module options and functions.
        >>> anima_options(OPTIONS) 
        ... 
    """
    for _ in options:
        sleep(0.00003)
        stdout.write(_+'\n')
        stdout.flush()

def animation_banner():
    """ help """
    animation_cmd(BANNER)
    anima_options(OPTIONS)

def kwargs_getAndSet(params: dict[Any, Any], **kwargs)->dict[str, Any]:
    
    for _ in KWARGS_DICT.keys():
        value = None
        if isinstance(params, dict):
            value = params.fromkeys(_)

        kwargs[_] = KWARGS_DICT[_] if not value else value


    return kwargs

def banner_help(_baner_: bool = True) -> int:
    """ 
    BANNNER
    usage before anima_options.
    >>> banner_help()
    ... 0
    """
    animation_banner()
    print("\n")
    print("usage transforma_gif.py -f image_file.png --transform_func={PARAMS} -o new_file.gif")
    return 0

def return_file_() -> dict:
    """
    first run at call in cmdline.
    :return: <dict[Any, Any]> *kwargs
    """

    _ = {   "framerate": None, 
            "out_path": "out/",
            "GUI": False}       
    return '!'

def cmdline_verify(array: list) -> dict:
    """
    sanitalize options given in the call
    and return the wait array <dict>
    to run with options and automatizate.

    :params array: list
    :return: dict
    """
    files   = []
    counter = 0
    _ =     {   "file": None,
                "framerate": None,
                "out_path": "out/",
                "GUI": False,
                "color_scheme": None,}
 
    for ITEM in array:
        if "=" in ITEM:
            # --framerate
            if ITEM[:len("--framerate")].lower() == "--framerate": 
                _["framerate"] = array[counter].rstrip("=").rsplit("=")[-1]

            # -o --out
            if ITEM[:len("-o")].lower() == "-o" or ITEM[:len("--out")].lower() == "--out":
                _["out_path"] = array[counter].rstrip("=").rsplit("=")[-1]

            # --file    
            if ITEM[:len("-f")].lower() == "-f" or ITEM[:len("--file")].lower() == "--file":
                _["file"] = array[counter].rstrip("=").rsplit("=")[-1]
                files.append({_['file']:kwargs_getAndSet(_['file'])})


            # -g --gui
            if ITEM[:len("-g")].lower() == "-g" or ITEM[:len("--gui")].lower() == "--gui":
                _["GUI"] = True

            # --color=[]
            if ITEM[:len("--color")].lower() == "--color":
                _["color_scheme"] = COLOR_SCHEME_DICT[array[counter].rstrip("=").rsplit("=")[-1].lower()]

    # TODO 
        match ITEM:
            case "--framerate" | "-framerate":
                try: 
                    _["framerate"] = array[counter + 1]
                except IndexError as Err:
                    return -1
            case "-o" | "--out" | "--save-as":
                try:
                    _["save_as"] = array[counter + 1]
                except IndexError as Err:
                    return -1
                
                
                if _["save_as"].rstrip('.').rsplit('.')[-1] == 'gif':
                    print("gif")
                
            case "-g" | "--gui" | "--GUI":
                _["GUI"] = True

            case "-f" | "--file":
                try:
                    _["file"] = array[counter + 1]
                    files.append({_['file']:kwargs_getAndSet(_['file'])})
                except IndexError:
                    return -1
            case "-c" | "--color":
                try:
                    _["color_scheme"] = COLOR_SCHEME_DICT[array[counter+1].lower()]
                except IndexError:
                    return -1
            
        if counter < len(array):
            counter += 1

    _['edits_files'] = files
    
    return _

def time_function(func):
    #_mem = tracemalloc.start()
    #mem_calc = lambda x, y: (x / (1024*1024), y / (1024*1024))
    def wrapper(*args, **kwargs):
        start = time()
        #curr, peak = mem_calc(tracemalloc.get_traced_memory())
        
        print(f"[started func: {func.__qualname__}].") #current memory {curr:8.f}MB; peak: {peak:8.f}MB.")
        
        try:
            return func(*args, **kwargs)
        finally:
            dt_ms = time() - start
            #curr, peak = mem_calc(tracemalloc.get_traced_memory())

            print(f"[func: {func.__qualname__}]: {dt_ms:.f} ms.")
            #print(f"[func usage memory]: current: {curr:8.f}MB; peak: {peak:8.f}MB.")
    
    #tracemalloc.clear_traces()
    return wrapper

if __name__ == '__main__':
    app = banner_help()
    
