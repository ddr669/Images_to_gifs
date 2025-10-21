
from .withpygame import *


def sanitize_ranges(lower_target: list | tuple,
                    upper_target: list | tuple)->list[np.array,np.array]:
    
    if type(lower_target) == list or type(lower_target) == tuple:
        lower_target = np.array(lower_target)
        upper_target = np.array(upper_target)
    return lower_target, upper_target


def return_image_from_array(array: cv2.Mat | np.ndarray) -> Image.Image:
    return Image.fromarray(array)

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
        #file_ = self.matrix
        lower_target, upper_target = sanitize_ranges(lower_target, upper_target)
        mask = cv2.inRange(file_, lower_target, upper_target)
        del file_, lower_target, upper_target, file
        return mask