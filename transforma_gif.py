#!/bin/venv python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
###################
from PIL import Image

from sys import argv
from cmdline_verify import cmdline_verify
from cmdline_verify import __help__, return_file_

def read_dir_(path: str):
    # to make the things izi, if you named the pics files with * img_0001.jpg * 
    # ( Optional : if you dont choose extension, will be necessary!)
    try:
        file = open(path, "r")
    except FileNotFoundError as Err:
        __help__()
        print("[!] path or file not Found!")
        exit()
    

def main(file_dict: dict):
    print(file_dict)
    read_dir_(_file_["path"])
    return 0

if __name__ == "__main__":
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()

    app = main(_file_) if _file_ else main("!")
    input()