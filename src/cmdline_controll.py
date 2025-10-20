#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-

from time import sleep
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
OPTIONS.append(f"{DARK_HIGH(f'These options work alone in GUI mode')}")
OPTIONS.append(f"{DARK_HIGH(f'but with other options like {BOLD_HIGH('--save')}')}")
OPTIONS.append(f"{DARK_HIGH(f'run in CD/CLI mode and save.\t {BOLD_HIGH('<DEFAULT new_filename=new_file.png|gif|jpg>')}')}")
OPTIONS.append(f"\t{BOLD_HIGH('--remove-color')} - remove a color in range between. {DARK_HIGH('<DEFAULT COLOR_RANGE=black>')}")
OPTIONS.append(f"\t\t{DARK_HIGH(f'use with options {BOLD_HIGH('--color-range=[10,10,10],[25,25,25]')}')}")
OPTIONS.append(f"\t\t{DARK_HIGH(f'default new_background_color=(0,255,0)')} # {BOLD_HIGH('green')}")
OPTIONS.append(f"\t{BOLD_HIGH('--apply-alpha')} - apply transparency to a image. {DARK_HIGH('<DEFAULT COLOR_REMOVE=white>')}")
OPTIONS.append(f"\t\t{DARK_HIGH('quick-mode:')} transforma_gif.py file.png --save new_file.png --apply-alpha black")
OPTIONS.append(f"\t\t\t{DARK_HIGH('HINT: look for another color range in cmdline_verify.py')}")


def animation_cmd(banner: list[str]):
    """
    just a ascii animation before ascii main banner.
    * invisible ascii char, unknown behavor
    
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
    """ 
        help 
                
    """
    animation_cmd(BANNER)
    anima_options(OPTIONS)

def kwargs_getAndSet(params: dict[Any, Any], *kwargs)->dict[str, Any]:
    return kwargs

def banner_help(_baner_: bool = True) -> int:
    """ 
    BANNNER
    usage before anima_options.

    >>> banner_help()
    ... 0
    """

    animation_banner()
    print("usage transforma_gif.py")
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

    counter = 0
    _ =     {   "file": None,
                "framerate": None,
                "out_path": "out/",
                "GUI": False,
                "color_scheme": None}
    
    for ITEM in array:
        if "=" in ITEM:
            if ITEM[:len("--frame")].lower() == "--frame": 
                _["framerate"] = array[counter].rstrip("=").rsplit("=")[-1]
            if ITEM[:len("-o")].lower() == "-o" or ITEM[:len("--out")].lower() == "--out":
                _["out_path"] = array[counter].rstrip("=").rsplit("=")[-1]
            if ITEM[:len("-f")].lower() == "-f" or ITEM[:len("--file")].lower() == "--file":
                _["file"] = array[counter].rstrip("=").rsplit("=")[-1]
            if ITEM[:len("-g")].lower() == "-g" or ITEM[:len("--gui")].lower() == "--gui":
                _["GUI"] = True
            if ITEM[:len("-c")].lower() == "-c" or ITEM[:len("--color")].lower() == "--color":
                _["color_scheme"] = COLOR_SCHEME_DICT[array[counter].rstrip("=").rsplit("=")[-1].lower()]

    # TODO 
        match ITEM:
            case "--frame" | "--framerate":
                try: 
                    _["framerate"] = array[counter + 1]
                except IndexError as Err:
                    return -1
            case "-o" | "--out":
                try:
                    _["out_path"] = array[counter + 1]
                except IndexError as Err:
                    return -1
            case "-g" | "--gui" | "--GUI":
                _["GUI"] = True

            case "-f" | "--file":
                try:
                    _["file"] = array[counter + 1]
                except IndexError:
                    return -1
            case "-c" | "--color":
                try:
                    _["color_scheme"] = COLOR_SCHEME_DICT[array[counter+1].lower()]
                except IndexError:
                    return -1

        if counter < len(array):
            counter += 1

    return _

if __name__ == '__main__':
    app = banner_help()
    
