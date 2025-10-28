
from .withpygame import *
from .array_module import * 


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
    junk_number = 0
    actual_text = text[0]
    for _ in range(0, frame_count):
     
        if function:
            file_image = function(file_image, _)
        frames.append(simple_memeHowGen(file_image, text=actual_text))
        interval_counter += 1
        if interval_counter == interval:
            interval_counter = 0
            junk_number =  junk_number + 1 if junk_number < len(text)-1 else 0
            actual_text = text[junk_number]
            file_image = frames[_]
    frame0 = frames[0]
    frame0.save(new_filename, format="GIF", save_all=True, append_images=frames, duration=frame_count, loop=0)


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
