from .array_module import * 
from .config_variables import *


class IMAGE_CLASS_MODULE:

    def __init__(self, img, *args,**kwargs):
        self.old_image = None
        self.is_alpha  = False
        self.matrix, self.image = img_instance(img)
        self.mode     = self.image.mode
    
    def update_image(self,new_image: Image.Image = None) -> None:
        self.image = new_image
        self.matrix = np.array(self.image)

    def update_matrix(self, new_matrix: np.array) -> None:
        self.matrix = new_matrix if isinstance(new_matrix,np.ndarray) else self.matrix
        self.image  = return_image_from_array(self.matrix)

    def save(self, out: str = 'out/new_file.png') -> None:
        self.image.save(out)

