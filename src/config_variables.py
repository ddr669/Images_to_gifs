# mode to load new frame files in memory
MODE_LOADED_IN_MEMORY = True
FRAME_TO_SKIP = 188 # cannot be 1
#                          y,x      y,x to text weight
PIXEL_READ_DICT = {'1': (6,4), '2': (8,6),      # more accurate between pixel read but worst in speed (takes a lot of time)
                   '3': (8,4), '4': (12,8),     # I recommend something between 3 and 4
                   '5': (16, 8), '6': (14,8),   # this is for perfomace and less accurace
                   '7': (16, 12), '8': (24, 8), # NO ACCURACE
                   '9': (24, 16), '10': (64, 24)}
DEBUG_INFO:int|bool      = 1
PIXEL_READ_COUNTER:int   = 4        # Default 4
QUANTIZE_IN_SURFACES:int = None     # Warning!
QUANTIZE_IMAGES_GIF:int  = 126      # Default 186 (0 -> 255): from lower bitmap to better 
QUANTIZE_IMAGES_VIDEO:int= None     # Default None
FRAMES_LENGTH_VIDEO_INFO = 0        # Default 0 -> change as a file is set
#
REDUCE_PIXEL_GIF:int     = None    # Recommended but not need, 2 is fine to gif
REDUCE_PIXEL_VIDEO:int   = None     # Not recommended
#
GREEN_COLOR     = '\033[32m'
RED_COLOR       = '\033[31m'
DEFAULT_COLOR   = '\033[0m'
RED_BG          = "\033[0;41;31m"
YELLOW_BG       = '\033[43m'
YELLOW_COLOR    = '\033[33m'
#
WARNING_RAM_OVERFLOW    = f"""{RED_BG}\t\t! WARNING !\t\t{DEFAULT_COLOR}\n
{RED_COLOR}This application is on tests and has to become better\n
This warning is to guarantee and prevent to load {RED_BG}larges files{DEFAULT_COLOR}
\n{RED_COLOR}That function uses a lot of RAM and if you do not have that much could affect your workflow
\nor even nd worst, can fuck your computer.\n
please cut that big file and make with parts of them{DEFAULT_COLOR}"""
WARNING_FRAMERATE_LOSS  = f"""{YELLOW_BG}\t\t ADVICE \t\t{DEFAULT_COLOR}\n
{YELLOW_COLOR}THIS FILE HAS SO MUCH FPS THAT IS HIGHER THAN A NORMAL FILE\n
I MADE THIS PROGRAM LOOKING FOR SMALL FILES AND CLIPPEDS FILES\n
BUT IF YOU CAN WAIT FOR IT, I can't longer help if it break.\n
if you already clip the file and want to proceed with\n
a file of 60@fps or want to change to 24@fps?{DEFAULT_COLOR}\n"""
#
KWARGS_DICT = {'':''}