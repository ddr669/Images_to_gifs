#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-

from src import *


class Image_class_module:

    def __init__(self, img: Any, *args,**kwargs):
        self.old_image = None
        self.is_alpha  = False
        self.matrix, self.image = img_instance(img)
        self.mode     = self.image.mode

    def transform_into_gray(self, gray_matrix: list | tuple = None, *args, **kwargs)->Image.Image:
        gray_multiply = (0.299, 0.587, 0.114, 0.0) if not gray_matrix else gray_matrix
        self.matrix = return_gray(self, gray_matrix=gray_multiply)
        self.mode = "GRAY"
        self.image = return_image_from_array(self.matrix)
        return self.image
    def transform_in_alpha(self) -> cv2.Mat:
        if not self.is_alpha:
            new_ = return_alpha(self)
            self.matrix, self.mode = (new_, 'RGBA')
            self.image  = return_image_from_array(self.matrix)
            self.is_alpha = True
        return self.matrix

    def sobel_filter(self, *args, **kwagrs) -> cv2.Mat:
        laplacian = sobel_filter(self)
        laplacian = np.uint8(np.absolute(laplacian))
        self.matrix = laplacian
        self.image  = return_image_from_array(self.matrix)

        return laplacian

    def both_edge_detection(self, weight: int = None, *args, **kwargs)->None:
        self.matrix = both_edge_detection(self, weight=weight, *args, **kwargs)
        self.image = return_image_from_array(self.matrix)

    def blurr_image(self, strenght: int = 3):
        _ = blurr_image(image, strenght=strenght)
        mixed   = _        
        self.update_matrix(mixed)
        return self.image
       
    def update_image(self,new_image: Image.Image = None) -> None:
        self.image = new_image
        self.matrix = np.array(self.image)

    def update_matrix(self, new_matrix: np.array) -> None:
        self.matrix = new_matrix if isinstance(new_matrix,np.ndarray) else self.matrix
        self.image  = return_image_from_array(self.matrix)

    def save(self, out: str = 'out/new_file.png'):
        self.image.save(out)

@time_function
def return_gray(image: Image_class_module,
                gray_matrix: list | tuple = None,
                *args, **kwargs):
    gray_multiply = (0.299, 0.587, 0.114, 0.0) if not gray_matrix else gray_matrix
    colors = image.matrix.shape[-1]
    tmp = 0
    for _ in range(0, colors):
        tmp += image.matrix[:,:,_]*gray_multiply[_]

    return np.array(tmp/3, dtype=np.uint8)

        #image.matrix = np.array(tmp/3, dtype=np.uint8)
    #image.mode = "GRAY"
    #image.image = return_image_from_array(image.matrix)

@time_function
def return_alpha(image: Image_class_module, *args, **kwargs) -> cv2.Mat:
    return cv2.cvtColor(image.matrix, cv2.COLOR_BGR2BGRA)
    

@time_function
def sobel_filter(image: Image_class_module, *args, **kwagrs) -> cv2.Mat:
    gray_img = cv2.cvtColor(image.matrix, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray_img, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    return laplacian

@time_function
def both_edge_detection(image: Image_class_module, weight: int = None, *args, **kwargs)->cv2.Mat:
    tmp_hor = convolution(image, np.array([[0.25, 0, -0.25], [0.50, 0, -0.50], [0.25, 0, -0.25]]))
    tmp_ver = convolution(image, np.array([[0.25, 0.5, 0.25],[0,0,0],[-0.25, -0.5, -0.25]]))
    if not weight:
        tmp_mat = cv2.add(tmp_hor, tmp_ver)
        return tmp_mat

    w = weight if isinstance(weight, int) else 1
    tha = remove_range_color_alpha(tmp_hor, [0,0,0],[w,w,w])
    tva = remove_range_color_alpha(tmp_ver, [0,0,0],[w,w,w])
    tmp_mat = cv2.add(tha, tva)
    return tmp_mat

@time_function
def blurr_image(image: Image_class_module, *args, **kwargs)->cv2.Mat:
    x_dir: int = 50
    y_dir: int = 50
    strenght: int = 3

    blurr = np.zeros((strenght, strenght))
    c = int(strenght / 2)
    blurr = cv2.line(blurr, (c+x_dir, c+y_dir), (c,c), (255,), 1)
    blurred = convolution(image,blurr)
    mixed   = cv2.add(image.matrix, blurred)
    return mixed

    #ODO: ftm fourier transformation method on image before
    #convolution 
@time_function
def convolution(image: Image_class_module, kernel: np.ndarray, *args, **kwargs) -> np.ndarray:
    x_size = image.matrix.shape[1]
    y_size = image.matrix.shape[0]
    z_a = image.matrix.shape[-1]
    z_a = 1 if z_a == x_size else z_a
    k_sizeX, k_sizeY = kernel.shape[0], kernel.shape[1]
    _ = np.zeros((y_size -k_sizeY + 3,x_size -k_sizeX + 3, 3), dtype=np.uint8)

    if image.mode != 'gray' or image.mode == None:
        for y in range(k_sizeY // 2, y_size - k_sizeY // 2 - 1):
            for x in range(k_sizeX // 2, x_size - k_sizeX // 2 - 1):
                try:
                    values = image.matrix[y-k_sizeY//2:y+k_sizeX//2+1, x-k_sizeX//2:x+k_sizeX//2+1,:]
                    tmp_0 = (np.dot(values[:,:,0], kernel)).sum().astype(np.uint8)
                    tmp_1 = (np.dot(values[:,:,1], kernel)).sum().astype(np.uint8)
                    tmp_2 = (np.dot(values[:,:,2], kernel)).sum().astype(np.uint8)
                    _[y,x,0] = np.floor(tmp_0 / kernel.size + 2)
                    _[y,x,1] = np.floor(tmp_1 / kernel.size + 2)
                    _[y,x,2] = np.floor(tmp_2 / kernel.size + 2)
                    
                except IndexError:
                    values = image.matrix[y-k_sizeY//2:y+k_sizeX//2+1, x-k_sizeX//2:x+k_sizeX//2+1]
                    tmp_0 = np.dot(values[:,:], kernel).sum().astype(np.uint8)
                    _[y, x] = np.floor(tmp_0 / kernel.size + 2)
    
    return _[:y_size,:x_size,:]
       

@time_function
def blit_text_inrange(image: Image_class_module,
                            lower_target: list = np.array([0,0,0,255]),
                            upper_target: list = np.array([45,45,45,255]),
                            *args,
                            **kwargs)->Image.Image:
    bg_color = (lower_target[0],lower_target[1],lower_target[2], 255)
    text_img = Image.new('RGBA', image.image.size, bg_color)
    old_text = "hello"
    draw = ImageDraw.Draw(text_img)
    
    k_items = kwargs.keys()
    if 'text' in k_items:
        text = kwargs.get('text')
        if 'loop' in k_items and kwargs.get('loop') == True:
            text += "\n"
            if len(text) <= image.image.size[0]:
                for b in range(0, image.image.size[1], 12):
                    for a in range(0, image.image.size[0],8):
                        text += " " + kwargs.get('text') + " "
                    text += "\n"
    else:
        text = ''
        for b in range(0, image.image.size[1], 8):
            for a in range(0, image.image.size[0], 8):
                text += " " + str(chr(randint(33, 122))) + " " # chr range for visual character
            text += '\n'
    #font = ImageFont.truetype("Tests/fonts/FreeMono.ttf", 24)

    draw.text((0,0), text)
    lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
    rgb = cv2.cvtColor(image.matrix, cv2.COLOR_BGRA2RGBA)
    txt = cv2.cvtColor(np.array(text_img), cv2.COLOR_BGRA2RGBA)
    mask = create_mask(rgb, lower_target, upper_target)
    inv_mask  = cv2.bitwise_not(mask)
    fg_masked = cv2.bitwise_and(rgb,rgb,mask=inv_mask)
    bg_masked = cv2.bitwise_and(txt,txt,mask=mask)
    
    tmp2 = cv2.add( fg_masked, bg_masked)
    image.image = return_image_from_array(cv2.cvtColor(tmp2,cv2.COLOR_BGRA2RGBA))
    image.matrix = tmp2
    if not 'new_bg' in k_items or kwargs.get('new_bg') == False:
        remove_range_color_alpha(image)

    return image.image


@time_function
def remove_range_color_alpha(image: Image_class_module,
                            lower_target: list = np.array([0,0,0,255]),
                            upper_target: list = np.array([45,45,45,255]),
                            *args,
                            **kwargs
                            )->Image.Image:
    if not isinstance(image, Image_class_module):
        if isinstance(image, Image):
            image = Image_class_module(image)
        elif isinstance(image, np.ndarray):
            image = Image_class_module(return_image_from_array(image))

    if not image.is_alpha: 
        image.transform_in_alpha()
        image.is_alpha = True

    if len(lower_target) <= 3 or len(upper_target) <= 3:
        try:
            if len(upper_target) != 4:
                upper_target.append(255)
            if len(lower_target) != 4:
                lower_target.append(255)
        except AttributeError:
            if len(upper_target) != 4:
                upper_target = upper_target.add(255)
            if len(lower_target) != 4:
                lower_target = lower_target.add(255)

    lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
    rgba = image.matrix
    mask = create_mask(rgba, lower_target, upper_target)

    image.matrix = cv2.bitwise_not(image.matrix,rgba, mask=mask)

    image.old_image = image.image
    image.image = return_image_from_array(
        cv2.cvtColor(image.matrix, cv2.COLOR_BGRA2RGBA))

    return image.image

@time_function
def draw_line_image(image, coords: list[tuple], color: tuple = (255,255,255), width: int = 2, *args,**kwargs) -> Image.Image:
        draw_f = ImageDraw.Draw(image.image)
        draw_f.line(coords, fill=color, width=width)
        return image.image

@time_function
def make_gif_with_img_func(file,file_name: str = 'out/new_file.gif',
                           over_img = None,
                           coord: list | tuple = [0,0],
                           function_draw = None,
                           frames_len: int = 3,
                           animation_speed: list = [0,1],
                           effect: bool = False,
                           **kwargs):
    frames = []
    direction = 0

    for a in range(0, frames_len):
        new_file = function_draw(file, **kwargs)
        frames.append(new_file)

    try:
        frame0 = frames[0]
        frame0.save(file_name, format="GIF", save_all=True, append_images=frames, duration=frames_len, loop=0)

    except AttributeError:
        frames = [Image.fromarray(_) for _ in frames]
        frame0 = frames[0]
        frame0.save(file_name, format="GIF" ,save_all=True, append_images=frames, duration=frames_len, loop=0)

def main(file_dict: dict):
    print(file_dict) if file_dict != "!" else None
    Config_Variables.SHOW_BANNER = False
    if file_dict == "!":
        if Config_Variables.SHOW_BANNER:
            banner_help()
        exit()

    if file_dict["GUI"]:
        pass

if __name__ == "__main__":
    img = Image_class_module('out/car_reduce.png')
    img.update_image(img.image.resize((800, 420)))
    #blit_text_inrange(img, text="eduardo", loop=1, rm_bg=True)
    new = Image_class_module('out/gato_reduzido.png')
    start = [0, 255]
    end = [800, 255]
    make_gif_with_img_func(img, function_draw=blurr_image,coords=[start,end],color=(255,0,0))
    #img2 = Image_class_module(img.sobel_filter())
    #img2.save("out/teste2.png")

 #  img.blurr_image(9)
    img.image.save('out/teste01.png')
    print('done')
    _file_ = None
    try:
        __ = argv[1]
        _file_ = cmdline_verify(argv)
    except IndexError as Err:
        _file_ = return_file_()
    app = main(_file_)
   

