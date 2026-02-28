from PIL import Image, PngImagePlugin, JpegImagePlugin
import cv2
import numpy as np

def return_array(file: str | Image.Image) -> np.ndarray:
    if isinstance(file, np.ndarray):
        return file
    
    if type(file) == Image.Image or type(file) == PngImagePlugin.PngImageFile or type(file) == JpegImagePlugin.JpegImageFile:
        new_file = np.array(file)
        _ = cv2.cvtColor(new_file, verify_mode2rgb(file))
    if type(file) == str:
        _ = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    else:
        _ = file.matrix

    return _

def sanitize_ranges(lower_target: list | tuple,
                    upper_target: list | tuple)->list[np.array,np.array]:
    lower_target = np.array(lower_target)
    upper_target = np.array(upper_target)
    return lower_target, upper_target

def verify_mode2rgb(image):
    match image.mode:
        case "RGB" | "BGR":
            # cv2.COLOR_BGR2RGB
            return 4
        case "BGRA" | "RGBA":
            return 2
        case _:
            return None
def verify_mode2rgba(image):
    match image.mode:
        case "RGB" | "BGR":
            # cv2.COLOR_BGR2RGBA
            return 0
        case "BGRA" | "RGBA":
            return None
        case _:
            return None
        
def verify_mode2gray(image):
    match image.mode:
        case "RGB":
            return 7
        case "BGR":
            return 6
        case "BGRA":
            return 10
        case "RGBA":
            return 11
        case _:
            return None

def return_image_from_array(array: cv2.Mat | np.ndarray) -> Image.Image:
    _ = Image.fromarray(array)
    return _

def create_mask(file_,
                lower_target: np.array = [0, 0,0],
                upper_target: np.array = [45,45,45]): 
        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        mask = cv2.inRange(file_, lower_target, upper_target)
        return mask

def img_instance(img):
    matrix, image = None, None
    if isinstance(img, np.ndarray):
        matrix   = img
        image    = return_image_from_array(img)
    elif isinstance(img,
        Image.Image) or isinstance(img,
        PngImagePlugin.PngImageFile) or isinstance(img,
        JpegImagePlugin.JpegImageFile):
        matrix   = np.array(img)
        image    = img
    elif isinstance(img, str):
        image    = Image.open(img)
        matrix   = np.array(image)
    
    return matrix, image