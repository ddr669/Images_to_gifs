#!/bin/venv python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-
###################
from PIL import Image

from sys import argv
from cmdline_verify import cmdline_verify
from cmdline_verify import __help__, return_file_

def main(file_dict: dict):
    print(file_dict)
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