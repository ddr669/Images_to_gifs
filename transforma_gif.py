#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-

from src import *
from modules import *

font.init()
print("\n\r\n\r") # just to keep the pygame welcome ^^

class Image_class_module:
    def __init__(self, img: Any, **kwargs):

        self.old_image = None
        self.is_alpha  = False
        if isinstance(img, np.ndarray):
            self.matrix   = img
            self.image    = return_image_from_array(img)

        elif isinstance(img, Image.Image) or isinstance(img, PngImagePlugin.PngImageFile) or isinstance(img, JpegImagePlugin.JpegImageFile):
            self.matrix   = return_array(img)
            self.image    = img

        elif isinstance(img, str):
            self.image    = Image.open(img)
            self.matrix   = return_array(self.image)



    def draw_line_image(self, coords: list[tuple], color: tuple = (255,255,255), width: int = 2, **kwargs) -> Image.Image:
        self.old_image = self.image
        draw_f = ImageDraw.Draw(self.image)
        draw_f.line(coords, fill=color, width=width)

    def transform_in_alpha(self, matrix: np.ndarray = None, mode: str = 'BGR') -> cv2.Mat:
        ''' 
        Transform a image into a alpha image using cv2.split
        to add a new channel alpha or get in cv2.Mat BGRA mode  
        if Image dont have alpha channel, convert it using  
        cv2.cvtColor.  
        Parameters
        ----------
            mode ( str ): mode to merge channels in matrix.
        '''
        if not matrix:
            self.old_image = self.image
            try:
                b, g, r, alpha = cv2.split(self.matrix)
            except ValueError:
                new_ = cv2.cvtColor(self.matrix, cv2.COLOR_BGR2BGRA)
                b, g, r, alpha = cv2.split(new_)

            self.matrix = cv2.merge([b,g,r,alpha]) if mode == 'BGR' else cv2.merge([r,g,b,alpha])
            self.image  = return_image_from_array(self.matrix)
            self.is_alpha = True
            return 0
        else:
            try:
                b, g, r, alpha = cv2.split(matrix)
            except ValueError:
                new_ = cv2.cvtColor(matrix , cv2.COLOR_BGR2BGRA)
                b, g, r, alpha = cv2.split(new_)
            
            return cv2.merge([b,g,r,alpha]) if mode == 'BGR' else cv2.merge([r,g,b,alpha])
    def remove_range_color_alpha(self,
                                lower_target: list = np.array([0,0,0,255]),
                                upper_target: list = np.array([45,45,45,255]),
                                )->Image.Image:
        '''   Remove range color and return    '''

        self.transform_in_alpha()
        self.is_alpha = True
        if len(lower_target) <= 3 or len(upper_target) <= 3:
            upper_target.append(255)
            lower_target.append(255)

        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        rgb = cv2.cvtColor(_temp, cv2.COLOR_BGRA2RGBA)

        mask = create_mask(rgb, lower_target, upper_target)
        self.matrix = cv2.bitwise_not(rgb,rgb, mask=mask) 
        self.image = return_image_from_array(self.matrix)
        return Image.fromarray(self.matrix, 'RGBA')

    def create_mask(self,
                lower_target: np.array = np.array([0,0,0]),
                upper_target: np.array = np.array([11,11,11])
                ) -> cv2.Mat:
        ''' 
        Using cv2 to select a mask inRange  
        from a image file or frame.  

        Parameters
        ----------
            #file (PIL.Image.Image | str | cv2.Mat): File Image.
            lower_target (np.array) = np.array([0,0,0]): lower color range.
            upper_target (np.array) = np.array([11,11,11]): upper color range.
        Returns:
            cv2.Mat: Image array like
        '''
        file_ = self.matrix
        
        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        mask = cv2.inRange(file_, lower_target, upper_target)
        del file_, lower_target, upper_target, file
        return mask

    def insert_imageInCoord(self, over_file: cv2.Mat | np.ndarray, coord: list | tuple = [0,0]) -> Image.Image:
        new_file = self.transform_in_alpha(over_file)
        tmp_ = self.transform_in_alpha(self.image)
        new_file_pil = return_image_from_array(new_file)
        mask = new_file_pil.split()[3]
        tmp_pil = Image.fromarray(tmp_, 'RGBA')
        tmp_pil.paste(new_file_pil, coord, mask=mask)

        self.image = tmp_pil
        self.matrix = return_array(self.image)

        del tmp_, mask, new_file_pil, new_file
        return tmp_pil

    def merge_array(
                    self,
                    to_merge: list[np.ndarray] | tuple[np.ndarray] | cv2.Mat | np.ndarray
                    ):
        ''' '''
        self.old_image = self.image 
        if isinstance(to_merge, np.ndarray):
            new_ = cv2.merge(to_merge, dst=self.matrix)
        elif isinstance(to_merge, list) or isinstance(to_merge, tuple):
            tmp = []
            for _ in to_merge:
                tmp.append(_)
            new_ = cv2.merge(tmp, dst=self.matrix)
        elif type(to_merge) == cv2.Mat:
            r,g,b,a = cv2.split(to_merge)
            new_ = cv2.merge([r,g,b,a], self.matrix)
        else:
            new_ =  cv2.merge([self.matrix, to_merge])   
        self.matrix = new_
        self.image  = return_image_from_array(self.matrix)

    def insert_image_in_mask(self,
                            lower_target: list = np.array([0,0,0]),
                            upper_target: list = np.array([45,45,45]),
                            new_bg_surf: Surface | Image.Image = None
                            )->Image.Image:
        """
        Insert a image in another by a mask choose by range color.

        Parameters.
        ----------
            file ( pygame.Surface | PIL.Image.Image ): base file to insert a bg.
            lower_target ( list | numpy.array ): lower color range to pick.
            upper_targe ( list | numpy.array ): upper color range to pick.
            new_bg_surf ( pygame.Surface | PIL.Image.Image ): file to insert.

        Returns:
            PIL.Image.Image: Image 
        """
        #_temp = WithPygame.create_surface(file)

        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        rgb = cv2.cvtColor(self.matrix, cv2.COLOR_BGR2RGB)
        mask = create_mask(rgb, lower_target, upper_target)
        new_rgb = cv2.bitwise_and(rgb, rgb, mask=mask)

        if new_bg_surf:
            bg_temp = return_array(new_bg_surf)

            if self.matrix.size < bg_temp.size:    
                _temp = Image.open(file).convert()
                bg_temp = Image.fromarray(bg_temp).resize(_temp.size)
                #bg_temp = bg_temp.resize(_temp.size)
                bg_temp = return_array(bg_temp)
            new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGR2RGB)
        
            new_bg = cv2.bitwise_and(new_bg, new_bg, mask=mask)
            new_rgb = cv2.add(new_bg,rgb - new_rgb)


        self.matrix = new_rgb
        self.image = Image.fromarray(new_rgb).transpose(Image.Transpose.TRANSPOSE)


def simple_memeGen(file_image: Image.Image | cv2.Mat,
                   text: str = "Me when",
                   bg_color: tuple = (255,255,255),
                   font_familly: str = 'Times New Roman',
                   font_color: tuple = (0,0,0),
                   font_size: int = 28,
                   txt_pos: tuple = (0,0),
                   **kwargs)-> Image.Image:
    
    bg_color = tuple(bg_color)
    font_color = tuple(font_color)
    diff = int(file_image.size[1] / 4)
    bg_image = Image.new('RGB',(file_image.size[0], file_image.size[1]+diff), bg_color)
    draw_f = ImageDraw.Draw(bg_image)
    font_path = str(f"c:\\WINDOWS\\Fonts\\IMPACT.TTF") # IMPACT REGULAR
    font_f = ImageFont.truetype(font_path, size=font_size)
    draw_f.text(tuple(txt_pos), fill=font_color, font=font_f, text=text)
    bg_image.paste(file_image, (0, 0+diff))
    return bg_image
    # c WINDOWS Fonts TIMES.TTF c WINDOWS Fonts TIMESBD.TTF c WINDOWS Fonts TIMESBI.TTF 

def simple_memeHowGen(file_image: Image.Image | cv2.Mat,
                      text: str = "How",
                      bg_color: tuple = (0,0,0),
                      font_color: tuple = (255,255,255),
                      font_size: int = 28,
                      txt_pos: tuple | None = None) -> Image.Image:
    new_file = file_image.reduce(2)
    bg_color = tuple(bg_color)
    font_color = tuple(font_color)
    
    diffy = int(new_file.size[1] / 4)
    text_y = int(diffy + (diffy /2))
    diffx = int(new_file.size[0] / 2 )
    center_x = file_image.size[0] / 2
    center_y = file_image.size[1] / 2
    if not txt_pos:
        txt_pos = (center_x - len(text) * 2, center_y+ text_y)

    bg_image = Image.new('RGB', (file_image.size[0], file_image.size[1]), bg_color)
    draw_f = ImageDraw.Draw(bg_image)
    font_path = str("c:\\WINDOWS\\Fonts\\CHARLEMAGNESTD-BOLD.OTF") 
    font_f = ImageFont.truetype(font_path, size=font_size)
    draw_f.text(txt_pos, fill=font_color, font=font_f, text=text)

    bg_image.paste(new_file, (diffx+1, diffy+1))
    diffx = diffx - 4
    diffy = diffy - 4
    square_sizex = new_file.size[0] + 8
    square_sizey = new_file.size[1] + 8
    left = [(diffx, diffy), (diffx, diffy+square_sizey)]
    right = [(diffx+square_sizex, diffy), (diffx+square_sizex, diffy+square_sizey)]
    top =  [(diffx, diffy), (diffx+square_sizex, diffy)]
    down = [(diffx, square_sizey+diffy), (square_sizex+diffx, square_sizey+diffy)]

    coords = [left, right, top, down]
    for _ in coords:
        bg_image = draw_line_image(bg_image, _)


    return bg_image

def recursion_memeHowAuto(file_image: Image.Image | cv2.Mat,
                          text: list | str = ['How', '???', 'No way'],
                          new_filename: str = "out/new_file_recursion_meme.gif",
                          frame_count: int = 90,
                          interval: int = 20,
                          function: None = None, **kwargs):
    interval_counter = 0
    frames = []
    if DEBUG_INFO:
        first_ini_time = time_now()
        print(f"{GREEN_COLOR}[Ini recursion_memeHowAuto]{DEFAULT_COLOR}")

    junk_number = 0
    actual_text = text[0]
    for _ in range(0, frame_count):
        if DEBUG_INFO:
            #print(f"{RED_COLOR}[Loading frame{a} in RAM]{DEFAULT_COLOR}")
            ini_time = time_now()
        if function:
            file_image = function(file_image, _)
        frames.append(simple_memeHowGen(file_image, text=actual_text))
        interval_counter += 1
        if interval_counter == interval:
            interval_counter = 0
            junk_number =  junk_number + 1 if junk_number < len(text)-1 else 0
            actual_text = text[junk_number]
            file_image = frames[_]

        if DEBUG_INFO:
            print(f"{GREEN_COLOR}[Load Image on memory]{DEFAULT_COLOR} time:{time_now() - ini_time}")

    frame0 = frames[0]
    frame0.save(new_filename, format="GIF", save_all=True, append_images=frames, duration=frame_count, loop=0)
    if DEBUG_INFO:
        print(f"{GREEN_COLOR}[Process terminated]{DEFAULT_COLOR} time:{time_now() - first_ini_time}")


def paste_array_in_array():
    pass

def simulate3DOverFlow(file_image: Image.Image | cv2    .Mat,
                       out: str = 'out/merged_image.png') -> Image.Image:
    array = return_array(file_image)
    # redpos, greepos, blupos = ((-2, -2), (2,2), (2,-2))
    red, green, blue = (array[:,:,0], array[:,:,1], array[:,:,2])
    _tmp_file_size = Image.open(file_image).size
    
    bg = Image.new('RGB', _tmp_file_size, (0,0,0))
    new_file = merge_array(bg, [blue, green, red])

    bg.paste(Image.fromarray(new_file), (0,0))
    

    bg.paste(Image.fromarray(cv2.Canny(new_file, 0, 100)), (0,0))

    if out:
        bg.save(out)
    return new_file



#


def glitchImageMask(file: Surface | Image.Image,
                        lower_target: list | tuple | np.ndarray = np.array([0,0,0]),
                        upper_target: list | tuple | np.ndarray = np.array([45,45,45]),
                        new_bg_surf: Surface | Image.Image = None
                        )->Image.Image:
    """ Make a image with file image or surface, and a
        new_bg image to create a mask to glitch at all.

        Parameters.
        ----------
            file ( pygame.Surface | PIL.Image.Image ): base file to insert a bg.
            lower_target ( list | numpy.array ): lower color range to pick.
            upper_targe ( list | numpy.array ): upper color range to pick.
            new_bg_surf ( pygame.Surface | PIL.Image.Image ): file to insert.
        Returns:
            PIL.Image.Image 
    """
    _temp = return_array(file)
    if new_bg_surf:
        bg_temp = return_array(new_bg_surf)
        if _temp.size < bg_temp.size:
          
            bg_temp = Image.open(new_bg_surf)
            bg_temp = bg_temp.resize(Image.fromarray(_temp).size)
          
            bg_temp = return_array(bg_temp)

    new_bg = bg_temp
    rgb = _temp
    lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
    mask = create_mask(rgb, lower_target, upper_target)
    new_rgb = cv2.bitwise_and(rgb, new_bg, mask=mask) if new_bg_surf else cv2.bitwise_and(rgb, rgb, mask=mask)
    if not new_bg_surf:
        pass
    else:
        new_bg = cv2.bitwise_and(new_bg, rgb)
        new_rgb = cv2.add(new_rgb, rgb+new_bg)
    del new_bg, mask, rgb, lower_target, upper_target, bg_temp, _temp
    return Image.fromarray(new_rgb).transpose(Image.Transpose.TRANSPOSE)


def return_array(file: str | Image.Image) -> np.ndarray:
    if isinstance(file, np.array) or isinstance(file, np.ndarray):
        return file
    if type(file) == Image.Image or type(file) == PngImagePlugin.PngImageFile or type(file) == JpegImagePlugin.JpegImageFile:
        file = np.array(file)
        try:
            _ = cv2.cvtColor(file, cv2.COLOR_BGR2RGB) # look at this sometime !
        except cv2.error as err:
            _ = cv2.cvtColor(file, cv2.COLOR_BGRA2RGBA)
    else:
        _ = cv2.imread(file, cv2.IMREAD_UNCHANGED) 
    return _
   


def make_gif_with_img_func(file,file_name: str = 'out/new_file.gif',
                           over_img = None,
                           coord: list | tuple = [0,0],
                           function_draw = None,
                           frames_len: int = 90,
                           animation_speed: list = [0,1],
                           effect: bool = False,
                           **kwargs):
    FRAMES = []
    if DEBUG_INFO:
        first_ini_time = time_now()
        print(f"{GREEN_COLOR}[Ini Make_gif_with_img_func]{DEFAULT_COLOR}")

    try:
        tmp_file_size = Image.open(file).size
    except AttributeError:
        tmp_file_size = file.size
    direction = 0
    file_tmp_name = []
    # TODO
    #   kwargs.get function with args in a dict to
    #   run all functions without break nd ways 
    #   work
    #
    for a in range(0, frames_len):
        if DEBUG_INFO:
            ini_time = time_now()

        if function_draw:
            new_file = function_draw(file, text=kwargs.get('text'))
            #new_file = function_draw(file,
            #                         over_img,
            #                         coord,
            #                         tmp_file_size,
            #                         animation_speed,
            #                         direction,
            #                         effect, entropy=kwargs.get('entropy'), framec=a,rotate=a,stroke=kwargs.get('stroke'))
        else:

            new_file = function_draw(file)

        FRAMES.append(new_file)
       
        if DEBUG_INFO:
            print(f"{RED_COLOR}[Loading frame{a} in RAM]{DEFAULT_COLOR}time: { time_now() - ini_time}")

    frame0 = FRAMES[0]
    frame0.save(file_name, format="GIF", save_all=True, append_images=FRAMES, duration=frames_len, loop=0)
    if DEBUG_INFO:
        print(f"{GREEN_COLOR}[Process terminated]{DEFAULT_COLOR} time:{time_now() - first_ini_time}")

    del frame0, tmp_file_size, direction, function_draw, FRAMES


def make_a_gray_video(frame,
                      file_name: str = 'out/new_file_gray.gif',
                      frames_len: int = 90):
    new_frames = []
    for a in range(0, frames_len):
        new_frames.append(return_grayscale_videoLoaded(frame))
    
    frame0 = Image.fromarray(new_frames[0])
    frames = [Image.fromarray(_) for _ in new_frames]
    frame0.save(file_name, format="GIF", save_all=True, append_images=frames, duration=frames_len, loop=0)

def main(file_dict: dict):
    print(file_dict) if file_dict != "!" else None
    if file_dict == "!":
        banner_help()
        exit()
    if file_dict["GUI"]:
        pass

if __name__ == "__main__":
    #img_de_fundo = Image.open('out/resize_img.jpg')

    #WithPygame.insert_imageBitwiseAnd('out/gato_reduzido.png').save('out/kadabra.png')
    #simulate3DOverFlow('out/gato_reduzido.png')


    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    app = main(_file_)
    
