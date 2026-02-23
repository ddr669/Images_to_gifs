#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-

from src import *
from modules import *

font.init()
print("\n\r\n\r") # just to keep the pygame welcome ^^

class Image_class_module:
    __slots__ = ['old_image', 'is_alpha',
		 'mode', 'matrix', 'image']

    def __init__(self, img: Any, **kwargs):
        self.old_image = None
        self.is_alpha  = False
        self.mode     = None
        if isinstance(img, np.ndarray):
            self.matrix   = img
            self.image    = return_image_from_array(img)
        elif isinstance(img,
            Image.Image) or isinstance(img,
            PngImagePlugin.PngImageFile) or isinstance(img,
            JpegImagePlugin.JpegImageFile):
            self.matrix   = return_array(img)
            self.image    = img
        elif isinstance(img, str):
            self.image    = Image.open(img)
            self.matrix   = return_array(self.image)

    def draw_line_image(self, coords: list[tuple], color: tuple = (255,255,255), width: int = 2, **kwargs) -> Image.Image:
        self.old_image = self.image
        draw_f = ImageDraw.Draw(self.image)
        draw_f.line(coords, fill=color, width=width)
        
    def transform_into_gray(self, gray_matrix: list | tuple = None):
        gray_multiply = (0.299, 0.587, 0.114, 0.0) if not gray_matrix else gray_matrix
        if self.mode:
            if self.mode == 'RGB':
                self.matrix = cv2.cvtColor(self.matrix, cv2.COLOR_RGB2GRAY)
            elif self.mode == 'RGBA':
                self.matrix = cv2.cvtColor(self.matrix, cv2.COLOR_RGBA2GRAY)
            elif self.mode == 'BGRA':
                self.matrix = cv2.cvtColor(self.matrix, cv2.COLOR_BGRA2GRAY)
            else:
                self.matrix = cv2.cvtColor(self.matrix, cv2.COLOR_BGR2GRAY)
        else:
            colors = self.matrix.shape[-1]
            tmp = 0
            for _ in range(0, colors):
                tmp += self.matrix[:,:,_]*gray_multiply[_]
            self.matrix = np.array(tmp/3, dtype=np.uint8)
        self.mode = "GRAY"
        self.image = return_image_from_array(self.matrix)

    def transform_in_alpha(self, matrix: np.ndarray = None, mode: str = 'BGR') -> cv2.Mat:
        
        if not matrix:
            self.old_image = self.image
            try:
                b, g, r, alpha = cv2.split(self.matrix)
            except ValueError:
                new_ = cv2.cvtColor(self.matrix, cv2.COLOR_BGR2BGRA)
                b, g, r, alpha = cv2.split(new_)

            self.matrix, self.mode = (cv2.merge([b,g,r,alpha]), 'BGRA') if mode == 'BGR' else (cv2.merge([r,g,b,alpha]), 'RGBA')

            self.image  = return_image_from_array(self.matrix)
            self.is_alpha = True
            return 0

        else:
            try:
                b, g, r, alpha = cv2.split(matrix)
            except ValueError:
                new_ = cv2.cvtColor(matrix , cv2.COLOR_BGR2BGRA)
                b, g, r, alpha = cv2.split(new_)
            
            if mode == 'BGR':
                self.mode = 'BGRA'
            else:
                self.mode = 'RGBA'
            return cv2.merge([b,g,r,alpha]) if mode == 'BGR' else cv2.merge([r,g,b,alpha])

    def remove_range_color_alpha(self,
                                lower_target: list = np.array([0,0,0,255]),
                                upper_target: list = np.array([45,45,45,255]),
                                )->Image.Image:
        self.transform_in_alpha()
        self.is_alpha = True
        if len(lower_target) <= 3 or len(upper_target) <= 3:
            upper_target.append(255)
            lower_target.append(255)
        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        rgb = cv2.cvtColor(self.matrix, cv2.COLOR_BGRA2RGBA)
        mask = create_mask(rgb, lower_target, upper_target)
        self.matrix = cv2.bitwise_not(rgb,rgb, mask=mask) 
        self.image = return_image_from_array(self.matrix)
        return Image.fromarray(self.matrix, 'RGBA')

    def create_mask(self,
                lower_target: np.array = np.array([0,0,0]),
                upper_target: np.array = np.array([11,11,11])
                ) -> cv2.Mat:
               file_ = self.matrix
        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        mask = cv2.inRange(file_, lower_target, upper_target)
        del file_, lower_target, upper_target
        return mask

    def insert_image_in_mask(self,
                            lower_target: list = np.array([0,0,0]),
                            upper_target: list = np.array([45,45,45]),
                            new_bg_surf: Surface | Image.Image = None
                            )->Image.Image:

        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        rgb = cv2.cvtColor(self.matrix, cv2.COLOR_BGR2RGB)
        mask = create_mask(rgb, lower_target, upper_target)
        new_rgb = cv2.bitwise_and(rgb, rgb, mask=mask)

        if new_bg_surf:
            bg_temp = return_array(new_bg_surf)
            if self.matrix.size < bg_temp.size:    
                _temp = return_image_from_array(self.matrix).convert()
                bg_temp = Image.fromarray(bg_temp).resize(_temp.size)
                
                bg_temp = return_array(bg_temp)
            new_bg = cv2.cvtColor(bg_temp, cv2.COLOR_BGR2RGB)
            new_bg = cv2.bitwise_and(new_bg, new_bg, mask=mask)
            new_rgb = cv2.add(new_bg,rgb - new_rgb)

        self.matrix = new_rgb
        self.image = Image.fromarray(new_rgb).transpose(Image.Transpose.TRANSPOSE)

    def sobel_filter(self) -> cv2.Mat:
        if not self.mode:
            gray_img = cv2.cvtColor(self.matrix, cv2.COLOR_BGR2GRAY)
        else:
            gray_img = cv2.cvtColor(self.matrix, cv2.COLOR_RGB2GRAY) if self.mode == 'RGB' else cv2.cvtColor(self.matrix, cv2.COLOR_BGRA2GRAY)
        laplacian = cv2.Laplacian(gray_img, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        return laplacian
    

    @time_function
    def both_edge_detection(self, weight: int = None):
        tmp_hor = self.convolution(np.array([[0.25, 0, -0.25], [0.50, 0, -0.50], [0.25, 0, -0.25]]))
        tmp_ver = self.convolution(np.array([[0.25, 0.5, 0.25],[0,0,0],[-0.25, -0.5, -0.25]]))
        if not weight:
            self.matrix = cv2.add(tmp_hor, tmp_ver)
            self.image = return_image_from_array(self.matrix)
            return 

        tmp_hor = Image_class_module(tmp_hor)
        w = weight if isinstance(weight, int) else 1
        tmp_hor.remove_range_color_alpha([0,0,0], [w,w,w])
        tmp_ver = Image_class_module(tmp_ver)
        tmp_ver.remove_range_color_alpha([0,0,0], [w,w,w])
        self.matrix = cv2.add(tmp_hor.matrix, tmp_ver.matrix)
        self.image = return_image_from_array(self.matrix)

    @time_function
    def blurr_image(self, strenght: int = 3):

        x_dir: int = 50
        y_dir: int = 50
        blurr = np.zeros((strenght, strenght))
        c = int(strenght / 2)
        blurr = cv2.line(blurr, (c+x_dir, c+y_dir), (c,c), (255,), 1)
#        blurred = self.convolution(blurr)

        mixed   = cv2.cvtColor(cv2.add(self.matrix, blurr), cv2.COLOR_BGR2RGB)
        
        self.update_matrix(mixed)

   # TODO: ftm fourier transformation method on image before
   # convolution 
    @time_function
    def convolution(self, kernel: np.ndarray) -> np.ndarray:
        x_size = self.matrix.shape[1]
        y_size = self.matrix.shape[0]
        z_a = self.matrix.shape[-1]

        z_a = 1 if z_a == x_size else z_a
        k_sizeX, k_sizeY = kernel.shape[0], kernel.shape[1]

        _ = np.zeros((y_size -k_sizeY + 3,
                     x_size -k_sizeX + 3, 3), dtype=np.uint8)

        if self.mode != 'gray' or self.mode == None:
            for y in range(k_sizeY // 2, y_size - k_sizeY // 2 - 1):
                for x in range(k_sizeX // 2, x_size - k_sizeX // 2 - 1):

                    try:
                        values = self.matrix[y-k_sizeY//2:y+k_sizeX//2+1, x-k_sizeX//2:x+k_sizeX//2+1,:]
                        tmp_0 = (np.dot(values[:,:,0], kernel)).sum().astype(np.uint8)
                        tmp_1 = (np.dot(values[:,:,1], kernel)).sum().astype(np.uint8)
                        tmp_2 = (np.dot(values[:,:,2], kernel)).sum().astype(np.uint8)
                        _[y,x,0] = np.floor(tmp_0 / kernel.size + 2)
                        _[y,x,1] = np.floor(tmp_1 / kernel.size + 2)
                        _[y,x,2] = np.floor(tmp_2 / kernel.size + 2)
                        
                    except IndexError:
                        values = self.matrix[y-k_sizeY//2:y+k_sizeX//2+1, x-k_sizeX//2:x+k_sizeX//2+1]
                        tmp_0 = np.dot(values[:,:], kernel).sum().astype(np.uint8)
                        _[y, x] = np.floor(tmp_0 / kernel.size + 2)
        
        return _[:y_size,:x_size,:]
       

    def set_mode(self, mode: str):
        self.mode = mode if len(mode) <= 4 else None

    def update_image(self,new_image: Image.Image = None) -> None:
        self.image = new_image
        self.matrix = return_array(self.image) 

    def update_matrix(self, new_matrix: np.array) -> None:
        self.matrix = new_matrix if isinstance(new_matrix,np.ndarray) else self.matrix

        self.image  = return_image_from_array(self.matrix)

    def save(self, out: str = 'out/new_file.png'):
        self.image.save(out)


def make_gif_with_img_func(file,file_name: str = 'out/new_file.gif',
                           over_img = None,
                           coord: list | tuple = [0,0],
                           function_draw = None,
                           frames_len: int = 90,
                           animation_speed: list = [0,1],
                           effect: bool = False,
                           **kwargs):
    FRAMES = []
    try:
        tmp_file_size = Image.open(file).size
    except AttributeError:
        tmp_file_size = file.size
    direction = 0

    for a in range(0, frames_len):
        if function_draw:
            new_file = function_draw(file, text=kwargs.get('text'))
            
        else:

            new_file = function_draw(file)
        FRAMES.append(new_file)
    frame0 = FRAMES[0]
    frame0.save(file_name, format="GIF", save_all=True, append_images=FRAMES, duration=frames_len, loop=0)

    del frame0, tmp_file_size, direction, function_draw, FRAMES


def main(file_dict: dict):
    print(file_dict) if file_dict != "!" else None
    if file_dict == "!":
        banner_help()
        exit()

    if file_dict["GUI"]:
        pass

if __name__ == "__main__":
    img = Image_class_module('out/car_reduce.png')
    img.update_image(img.image.resize((800, 420)))
    #img.transform_into_gray()
    img2 = Image_class_module(img.sobel_filter())
    img2.save("out/teste2.png")
#    img.both_edge_detection()
    img.update_matrix(img.matrix.__invert__())
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
   


# TODO replace lists to tuples
#
# - 1. COLOR SPACE CONVERSION
# rgb to YCbCr
# y  =  0.299 R + 0.587 G + 0.114 B
# cb =  -0.1687 R - 0.3313 G + 0.5 B + 128 (?)
# cr =  0.5 R  - 0.4187 G - 0.0813 B + 128 

# JPEG TRANSFORM
# 1. COLOR SPACE CONVERSION
# 2. CHROMINANCE DOWNSAMPLE
# 3. DISCRETE COSINE TRANSFORMATION
# 4. QUANTIZATION
# 5. RUN LENGTH AND HUFFMAN ENCODING

