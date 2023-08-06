import numpy as np 
import scipy.ndimage
import imageio
from multiprocessing import Pool, cpu_count
import imageio.core.util
from PIL import Image
import io

def silence_imageio_warning(*args, **kwargs):
    pass

class MIPGeneratorSingleThread: 
    """a class to generate MIP"""

    def __init__(self, numpy_array: np.ndarray, frames: int, delay :float, projection :int) -> None:
        """constructor

        Args:
            numpy_array (np.ndarray): [3D np.ndarray of shape (z,y,x) or 4D np.ndarray of shape (z,y,x,c)]
        """
        self.numpy_array = numpy_array
        self.mask_array = None
        self.frames = frames
        self.delay = delay / 1000
        self.projection = projection
        imageio.core.util._precision_warn = silence_imageio_warning

    def project(self, angle:int) -> np.ndarray:
        """function to generate 2D MIP of a 3D (or 4D) ndarray of shape (z,y,x) (or shape (z,y,x,C)) 

        Args:
            angle (int): [angle of rotation of the MIP, 0 for coronal, 90 saggital ]

        Returns:
            [np.ndarray]: [return the MIP np.ndarray]
        """
        vol_angle = scipy.ndimage.rotate(
            self.numpy_array, angle=angle, reshape=False, axes=(1, 2))
        MIP = np.amax(vol_angle, axis=1)
        MIP = np.flip(MIP, axis=0)
        return MIP

    def _create_projection_list(self) -> list:
        """Function to create a list of 2D MIP

        Returns:
            list: [list of 2D MIP]
        """
        angles = np.linspace(0, self.projection, self.frames)
        """nbCores = cpu_count() - 2
        pool = Pool(nbCores)
        projection_list = pool.map(self.project, angles)
        """
        projection_list = []
        for angle in angles:
            projection_list.append(self.project(angle))
        return projection_list

    def create_gif(self, output) -> None:
        """Function to create a gif from a 3D Array

        Args:
            output : [Where to save the gif]

        Returns:
            [None]: [None]
        """
        projection_list = self._create_projection_list()
        imageio.mimwrite(output, projection_list, format='.gif', duration=self.delay)

    def save_projection_two_modality(self, angle:int) -> np.ndarray:
        """function to generate a MIP of PET/MASK and save it as png image

        Args:
            pet_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
            mask_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
            angle (int): [angle of the MIP rotation]
            
        Returns:
            [np.ndarray]: [return the MIP np.ndarray]
        """
        mip_pet = MIPGeneratorSingleThread(self.numpy_array, None, 10, None)._project(angle)
        mip_mask = MIPGeneratorSingleThread(self.mask_array, None, 10, None)._project(angle)
        mip_mask[mip_mask < 5] = np.NaN

        virtualStreamPET = io.BytesIO()
        virtualStreamMASK = io.BytesIO()
        
        imageio.imwrite(virtualStreamPET, mip_pet, format='png')
        imageio.imwrite(virtualStreamMASK, mip_mask, format='png')

        virtualStreamPET.seek(0)
        virtualStreamMASK.seek(0)

        imagePET = Image.open(virtualStreamPET)
        imageMASK = Image.open(virtualStreamMASK)

        imagePET = imagePET.convert("RGBA")
        imageMASK = imageMASK.convert("RGBA")

        datas = imageMASK.getdata()
        newData = []
        for item in datas:
            # If the pixel is black (0,0,0), make it transparent
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                # Ajouter un pixel transparent
                newData.append((255, 255, 255, 0))
            else:
                # Rendre le pixel rouge et transparent
                newData.append((255, 0, 0, 100))

        imageMASK.putdata(newData)

        imagePET.paste(imageMASK, (0, 0), imageMASK)
        return np.array(imagePET)

    def create_gif_two_modality(self, mask_array:np.ndarray, output):
        """function to generate a gif MIP of PET/MASK and save it as .gif

        Args:
            pet_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
            mask_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
            output : [Where to save the gif]

        """
        self.mask_array = mask_array 
        angles = np.linspace(0, self.projection, self.frames)
        projections = []
        for angle in angles:
            projections.append(self.save_projection_two_modality(angle))
        imageio.mimwrite(output, projections, format='.gif', duration=self.delay)

class MIPGeneratorMultiThread(MIPGeneratorSingleThread):
    """a class to generate MIP"""

    def __init__(self, numpy_array: np.ndarray, frames: int, delay :float, projection :int) -> None:
        """constructor

        Args:
            numpy_array (np.ndarray): [3D np.ndarray of shape (z,y,x) or 4D np.ndarray of shape (z,y,x,c)]
        """
        super().__init__(numpy_array, frames, delay, projection)

    def _create_projection_list(self) -> list:
        """Function to create a list of 2D MIP

        Returns:
            list: [list of 2D MIP]
        """
        angles = np.linspace(0, self.projection, self.frames)
        nbCores = cpu_count() - 2
        pool = Pool(nbCores)
        projection_list = pool.map(self.project, angles)
        return projection_list    

    def create_gif_two_modality(self, mask_array:np.ndarray, output):
        """function to generate a gif MIP of PET/MASK and save it as .gif

        Args:
            pet_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
            mask_array (np.ndarray): [3D np.ndarray of shape (z,y,x)]
            output : [Where to save the gif]

        """
        self.mask_array = mask_array 
        angles = np.linspace(0, self.projection, self.frames)
        pool = Pool(self.nbCores)
        projections = pool.map(self.save_projection_two_modality, angles)
        imageio.mimwrite(output, projections, format='.gif', duration=self.delay)
    
    def create_gif(self, output) -> None:
        """Function to create a gif from a 3D Array

        Args:
            output : [Where to save the gif]

        Returns:
            [None]: [None]
        """
        projection_list = self._create_projection_list()
        imageio.mimwrite(output, projection_list, format='.gif', duration=self.delay)

