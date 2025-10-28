from PIL import Image, PngImagePlugin, JpegImagePlugin
import cv2
import numpy as np

def return_array(file: str | Image.Image) -> np.ndarray:
    if isinstance(file, np.ndarray):
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


def sanitize_ranges(lower_target: list | tuple,
                    upper_target: list | tuple)->list[np.array,np.array]:
    
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
    return lower_target, upper_target

def sanitize_unsigned_int(array: np.array): 
    c1, c2 = 0, 0
    _ = np.zeros(array.shape, dtype=np.uint8)
    for x in array:
        c2 = 0
        for b in x:
            if b >= 0 and b <= 255:
                _[c1, c2] = b
            c2 += 1
        c1 += 1
    return _


def return_image_from_array(array: cv2.Mat | np.ndarray) -> Image.Image:

    _ = Image.fromarray(array) 
  
    return _


def create_mask(file_,
                lower_target: np.array = np.array([0,0,0]),
                upper_target: np.array = np.array([11,11,11])
                ):
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
        
        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        mask = cv2.inRange(file_, lower_target, upper_target)
        del file_, lower_target, upper_target
        return mask

