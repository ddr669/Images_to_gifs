#!/bin/python3
#-*-encode: utf-8-*-
#
from sys import argv as args


BLACK_RANGE_COLOR    = {"lower_target"  : [0,0,0],       "upper_target": [55,55,55]}
WHITE_RANGE_COLOR    = {"lower_target"  : [200,200,200], "upper_target": [255,255,255]}
BLUE_RANGE_COLOR     = {"lower_target"  : [50,50,180],   "upper_target": [150,150,255]}
RED_RANGE_COLOR      = {"lower_target"  : [180, 50, 50], "upper_target": [255, 150, 150]}
GREEN_RANGE_COLOR    = {"lower_target"  : [50, 180, 50], "upper_target": [150, 255, 150]}
#BLUE_RANGE_COLOR     = {"lower_target"  : [50, 50, 180], "upper_target": [150, 150, 255]}
COLOR_SCHEME_DICT    = {"black": BLACK_RANGE_COLOR,
                        "white": WHITE_RANGE_COLOR,
                        "blue": BLUE_RANGE_COLOR,
                        "red": RED_RANGE_COLOR,
                        "green": GREEN_RANGE_COLOR,
                        }



def __help__(_baner_: bool = True):
    ''' BANNER '''
    if _baner_:
        print(""" ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
▕\033[0;37;41m▒▒▒▒▒▒▒▒▒▒▒▒▒▒\033[0;30;47m░░░░░\033[0;37;41m▒▒▒▒▒▒▒\033[1;37;40m░░░░\033[0;37;41m▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\033[0;31;40m░░░\033[0;0;0m▏
▕\033[0;37;42m▒▒▒\033[0;0;0m(‾)\033[0;37;42m▒▒▒▒▒▒▒▒\033[0;30;47m░░░░░\033[0;37;42m▒▒▒▒▒▒▒\033[1;37;40m░░░░\033[0;37;42m▒▒▒▒▒\033[0;0;0m/‾/\033[0;37;42m▒▒▒▒▒▒▒▒\033[0;31;40m░░░░\033[0;0;0m▏
▕\033[0;37;44m▒▒\033[0;0;0m/ / ‾_ `__‾\\/‾‾‾ `/‾__‾`/‾_‾\\\033[0;37;44m▒▒\033[0;0;0m/  _ /‾__‾\\\033[0;37;44m▒\033[0;31;40m░░░░░\033[0;0;0m▏
▕\033[0;30;47m▒\033[0;0;0m/ / /\033[0;30;47m▒\033[0;0;0m/ /\033[0;30;47m▒\033[0;0;0m/ / /\033[0;30;47m▒\033[0;0;0m/ / /\033[0;30;47m▒\033[0;0;0m/ / /__/\033[0;30;47m▒▒\033[0;0;0m/ /\033[0;30;47m▒\033[0;0;0m/ /\033[0;30;47m▒\033[0;0;0m/ /\033[0;31;40m░░░░░░\033[0;0;0m▏
▕\033[0;30;47m\033[0;0;0m/_/_/\033[0;30;47m▒\033[0;0;0m/_/\033[0;30;47m▒\033[0;0;0m/_/\\__,_/\\_ , /\\ __/\033[0;30;47m▒▒▒\033[0;0;0m\\__/\\_ __/\033[0;31;40m░░░░░░░\033[0;0;0m▏
▕\033[0;30;47m▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░\033[0;0;0m/___/\033[0;30;47m▒▒░░░░▒▒\033[0;31;40m░░░░░░░░░░░░░░░░░░\033[0;0;0m▏
▕▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒▒▒\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏""")
        print("""▕▒▒▒▒▒▒▒▒\033[1;37;40m/‾\033[0;0;0m_‾_‾\033[1;37;40m/‾‾‾\033[0;0;0m/‾__‾‾/\033[0;0;0m\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏
▕▒▒▒▒▒▒▒\033[1;37;40m/ /\033[0;0;0m __ \033[1;37;40m/ /\033[0;0;0m/ /_\033[0;0;0m\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏
▕▒▒▒▒▒▒/ /\033[0;0;0m_\033[1;37;40m/ // // __/\033[0;0;0m\033[0;31;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏
▕(‾)\033[0;0;0m▒▒▒\033[1;37;40m\\____/___/_/\033[1;37;40m░░░░░░░░░░░░░\033[0;0;0mBy:__DDr669__\033[1;37;40m░░░░░░\033[0;0;0m▏
▕▒▒▒▒▒▒▒▒▒\033[1;37;40m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\033[0;0;0m▏
 ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔""")
    
    print("usage transforma_gif.py")

#༺
# ― 
# ‾ ⁄ ▰ ▒ ░
def return_file_() -> dict:
    _ = {   "framerate": None, 
            "out_path": "out/",
            "GUI": True}      
    # ⬊ ☞
    #_["path"] = input("Path to find files/or file.mp4 ☞\t")
    #print(_["path"][:-3]) 
    return _ 


def cmdline_verify(array: list) -> dict:
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

if __name__ == "__main__":
    print(args)
    _ = cmdline_verify(args)
    print(_)
    #app = __help__()
