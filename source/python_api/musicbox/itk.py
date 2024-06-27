# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import SimpleITK as sitk
import vtk
from vtk.util import numpy_support
from . import image


def init():
    image.readers.append(read_from_file)


def read_from_file(filename, output_image = None):
    itk_image = sitk.ReadImage(filename)
    image = None

    if itk_image:
        image = output_image or image.Image()

        np_image = sitk.GetArrayFromImage(itk_image)

        vtk_type = vtk.VTK_FLOAT if np_image.dtype == 'float32' else vtk.VTK_UNSIGNED_CHAR
        vtk_array = numpy_support.numpy_to_vtk(num_array=np_image.ravel(), deep=True, array_type=vtk_type)

        shape = np_image.shape
        spacing = itk_image.GetSpacing()
        origin = itk_image.GetOrigin()

        vtk_image = vtk.vtkImageData()
        vtk_image.SetDimensions(shape[2], shape[1], shape[0])
        vtk_image.SetSpacing(spacing[0], spacing[1], spacing[2])
        vtk_image.SetOrigin(origin[0], origin[1], origin[2])

        vtk_image.GetPointData().SetScalars(vtk_array)

        image.vtk_image = vtk_image

    return image
