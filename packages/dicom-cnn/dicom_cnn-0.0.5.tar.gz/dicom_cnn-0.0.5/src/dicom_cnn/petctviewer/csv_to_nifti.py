from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dicom_cnn.petctviewer.mask_builder import MaskBuilder
    
import SimpleITK as sitk

#SK A revoir pas clair
class CSVToNifti():

    def __init__(self, path:str, csv_path:str) -> None:
        self.path= path
        self.csv_path= csv_path

    def reader(self):
        sitk_img= sitk.ReadImage(self.path)
        array= sitk.GetArrayFromImage(sitk_img)
        origin= sitk_img.GetOrigin()
        spacing = sitk_img.GetSpacing()
        size= sitk_img.GetSize()
        direction = sitk_img.GetDirection()
        return origin, spacing, size, direction, array 

    def mask_from_array(self, matrix_size):
        mask_array= MaskBuilder(self.csv_path, matrix_size).build_mask()
        [origin, spacing, size, direction, array ] = self.reader()
        new_img= sitk.GetImageFromArray(mask_array, isVector=True)
        new_img.SetOrigin(origin)
        new_img.SetDirection(direction)
        new_img.SetSpacing(spacing)
        sitk.WriteImage(new_img,'mask_nifti.nii')  




