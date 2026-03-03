
from PIL import Image, PngImagePlugin, JpegImagePlugin, ImageDraw, ImageFont, ImageText
import cv2
import numpy as np
from sys import argv
from time import time
from pygame import Surface, surfarray, SRCALPHA, draw, Rect, image

from pygame.transform import scale
from pygame.sprite import Sprite, Group

class Sprites_(Sprite):
        def __init__(self, _file: str | Image.Image = None):
            super().__init__()
            
            if type(_file) == Image.Image:
                try:
                    self.image = image.frombytes(_file.tobytes(), _file.size,  _file.mode)
                    self.mode = _file.mode
                except ValueError:
                    self.image = image.frombytes(_file.tobytes(), _file.size, 'RGB')
                    self.mode = 'RGB'
            elif type(_file) == np.ndarray:
                _tmp_img = Image.fromarray(_file).convert()
                self.image = image.frombytes(_tmp_img.tobytes(), _tmp_img.size,_tmp_img.mode)
                self.mode = _tmp_img.mode
            else:
                try:
                    self.image = image.load(_file)
                except TypeError:
                    #_tmp_img = Image.fromarray(_file).convert()
                    self.image = image.frombytes(_file.image.tobytes(), _file.image.size, _file.image.mode)


            self.rect = self.image.get_rect()    


class WithPygame:
    def make_gif_from_video( 
                        file, out: str = "video_as_gif.gif",
                        frame_counter: int = 90, text: str = "10",
                        font_color: tuple = (0,0,0),
                        lower_color: list = np.array([140,140,140]),
                        upper_color: list = np.array([220,220,220]),
                        remove_bg: bool = False,
                        new_bg_color: tuple = (),
                        resize_new_file: bool = False) -> None:

        cap = cv2.VideoCapture(file)
        counter = 0
        sub_counter = 0
        fps_seconds = cap.get(cv2.CAP_PROP_FPS)
        fps_size_video = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_counter = fps_size_video if frame_counter == None else frame_counter 
        FRAMES_LENGTH_VIDEO_INFO = frame_counter
        #QUANTIZE_IMAGES_VIDEO = QUANTIZE_IMAGES_GIF
        FRAMES = []
        while cap.isOpened():
            ret, cv2_frame = cap.read()
            if ret:
                converted = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
                frame_width, frame_height = converted.shape[1], converted.shape[0]
                if frame_width > 720 and frame_height > 415:
                    n_x, n_y = int(frame_width / 1.5), int(frame_height / 1.5)
                    frame_width = n_x
                    frame_height = n_y
                else:
                    n_x, n_y = frame_width-50,frame_height-50
                    frame_width = n_x
                    frame_height = n_y
                pil_image = Image.fromarray(converted)
                #FRAMES.append(WithPygame.make_image_from_fontsHASH(pil_image,text=text,font_color=font_color,lower_target=lower_color,upper_target=upper_color,
                #            remove_bg=remove_bg,new_bg_color=new_bg_color,frame_count=counter,reduce=REDUCE_PIXEL_GIF))
            elif ret:
                pass
            else:
                break
            counter += 1
            sub_counter += 1
            if counter >= frame_counter:
                break
        cap.release()

        FRAMES = [_ for _ in FRAMES]
        frame0 = FRAMES[0]
        frame0.save(f"{out}",format="GIF",save_all=True,append_images=FRAMES,duration=fps_seconds,loop=0)
