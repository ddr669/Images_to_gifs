#!/usr/env python3
#-*-encode: utf-8-*-
#-*-By:__DDr669__-*-
#-*-Date:__/__/__-*-

from src import *
from modules import *


font.init()
print("\n\r\n\r") # just to keep the pygame welcome ^^

class Image_class_module:

    def __init__(self, img: Any, *args,**kwargs):
        self.old_image = None
        self.is_alpha  = False
        self.matrix, self.image = img_instance(img)
        self.mode     = self.image.mode

    @time_function
    def draw_line_image(self, coords: list[tuple], color: tuple = (255,255,255), width: int = 2, **kwargs) -> Image.Image:
        self.old_image = self.image
        draw_f = ImageDraw.Draw(self.image)
        draw_f.line(coords, fill=color, width=width)
    @time_function
    def transform_into_gray(self, gray_matrix: list | tuple = None):
        gray_multiply = (0.299, 0.587, 0.114, 0.0) if not gray_matrix else gray_matrix
        if self.mode:
            color_cc = verify_mode2gray(self.image)
            self.matrix = cv2.cvtColor(self.matrix, color_cc)
            
        else:
            colors = self.matrix.shape[-1]
            tmp = 0
            for _ in range(0, colors):
                tmp += self.matrix[:,:,_]*gray_multiply[_]
            self.matrix = np.array(tmp/3, dtype=np.uint8)
        self.mode = "GRAY"
        self.image = return_image_from_array(self.matrix)

    @time_function
    def transform_in_alpha(self) -> cv2.Mat:
    
        self.old_image = self.image
        new_ = cv2.cvtColor(self.matrix, verify_mode2rgba(self.image))
         
        self.matrix, self.mode = (new_, 'RGBA')
        self.image  = return_image_from_array(self.matrix)
        self.is_alpha = True

            
    @time_function
    def remove_range_color_alpha(self,
                                lower_target: list = np.array([0,0,0,255]),
                                upper_target: list = np.array([45,45,45,255]),
                                )->Image.Image:
        self.transform_in_alpha()        
        if len(lower_target) <= 3 or len(upper_target) <= 3:
            upper_target.append(255)
            lower_target.append(255)

        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        rgb = cv2.cvtColor(self.matrix, cv2.COLOR_BGRA2RGBA)
        mask = create_mask(rgb, lower_target, upper_target)
        #self.matrix = cv2.bitwise_not(rgb,rgb, mask=mask) 
        self.matrix = cv2.absdiff(rgb, mask)
        self.image = return_image_from_array(self.matrix)

        return self.image

    @time_function
    def sobel_filter(self, *args, **kwagrs) -> cv2.Mat:
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
        self.matrix = np.array(self.image)

    def update_matrix(self, new_matrix: np.array) -> None:
        self.matrix = new_matrix if isinstance(new_matrix,np.ndarray) else self.matrix
        self.image  = return_image_from_array(self.matrix)

    def save(self, out: str = 'out/new_file.png'):
        self.image.save(out)

@time_function
def remove_range_color_alpha(image: Image_class_module,
                            lower_target: list = np.array([0,0,0,255]),
                            upper_target: list = np.array([45,45,45,255]),
                            **kwargs
                            )->Image.Image:
    
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
    rgb = cv2.cvtColor(image.matrix, cv2.COLOR_BGRA2RGBA)
    mask = create_mask(rgb, lower_target, upper_target)
    image.matrix = cv2.bitwise_not(image.matrix,rgb, mask=mask)
    image.old_image = image.image
    image.image = return_image_from_array(image.matrix)

    return image.image

@time_function
def draw_line_image(image, coords: list[tuple], color: tuple = (255,255,255), width: int = 2, **kwargs) -> Image.Image:
        #self.old_image = self.image
        draw_f = ImageDraw.Draw(image.image)
        draw_f.line(coords, fill=color, width=width)
        return image.image

@time_function
def make_gif_with_img_func(file,file_name: str = 'out/new_file.gif',
                           over_img = None,
                           coord: list | tuple = [0,0],
                           function_draw = None,
                           frames_len: int = 90,
                           animation_speed: list = [0,1],
                           effect: bool = False,
                           **kwargs):
    frames = [0 for a in range(0, frames_len)]
    direction = 0

    for a in range(0, frames_len):
        new_file = function_draw(file, **kwargs)
        frames[a] = new_file

    try:
        frame0 = frames[0]
        frame0.save(file_name, format="GIF", save_all=True, append_images=frames, duration=frames_len, loop=0)

    except AttributeError:
        frames = [Image.fromarray(frames[_]) for _ in range(0, len(frames))]
        frame0 = frames[0]
        frame0.save(file_name, format="GIF", save_all=True, append_images=frames, duration=frames_len, loop=0)




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
    new = Image_class_module('out/gato_reduzido.png')
   # img2 = WithPygame.make_image_from_fontsHASH(img, text="oi")
    start = [0, 0]
    end = [255, 255]
    make_gif_with_img_func(img, function_draw=draw_line_image, coords=[start,end])
    #img2 = Image_class_module(img.sobel_filter())
    #img2.save("out/teste2.png")

    #img.update_matrix(img.matrix.__invert__())
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

