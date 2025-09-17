#!/bin/python3
#-*-encode: utf-8-*-
#
from time import sleep
from sys import stdout
from shutil import get_terminal_size


BOLD_HIGH = lambda x: f"\033[1m{x}\033[0m"
DARK_HIGH = lambda x: f"\033[2m{x}\033[0m"
ITALIC_HI = lambda x: f"\033[3m{x}\033[0m"


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


def animation_cmd(text: str):
    WIDTH = get_terminal_size().columns
    HEIGHT = get_terminal_size().lines
    for h in range(0, HEIGHT):
        for w in range(0, WIDTH):
            # caution with the invisible emoji
            if h in range(0, len(BANNER)):
                if w in range(0, len(BANNER[0])):
                    stdout.write("‍*")
                    stdout.flush()
        stdout.write('\n')
        stdout.flush()

    stdout.write('\033[f')
    stdout.flush()
    for _ in range(0, len(BANNER)):
        sleep(0.05)
        stdout.write(BANNER[_]+'\n')
        stdout.flush()

def anima_options(options: list[str]):
    for _ in options:
        sleep(0.00003)
        stdout.write(_+'\n')
        stdout.flush()

def animation_banner():
    animation_cmd(BANNER)
    anima_options(OPTIONS)

if __name__ == '__main__':
    app = animation_cmd(BANNER)
    
