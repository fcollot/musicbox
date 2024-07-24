# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import SimpleITK as sitk
from musicbox.data_set import DataSet


class Reader():

    @staticmethod
    def file_filters():
        return {'ITK image': ['*.mha']}

    def read(self, filename):
        sitk_image = sitk.ReadImage(filename)
        np_array = sitk.GetArrayFromImage(sitk_image)
        return DataSet(
            voxels=np_array,
            spacing=numpy.array(sitk_image.GetSpacing()),
            origin=numpy.array(sitk_image.GetOrigin()),
        )
