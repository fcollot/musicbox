# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import SimpleITK as sitk
import vtk
from vtk.util import numpy_support


def pixels(object):
    if isinstance(object, sitk.Image):
        np_array = sitk.GetArrayViewFromImage(object)
    elif isinstance(object, vtk.vtkImageData):
        vtk_array = object.GetPointData().GetScalars()
        np_array = numpy_support.vtk_to_numpy(vtk_array)
        np_array.shape = object.GetDimensions()
    else:
        raise TypeError
    return np_array


voxels = pixels


def new_image(arg_1, *, type='sitk', data_type=float, spacing=None, origin=None, direction=None):
    if isinstance(arg_1, numpy.ndarray):
        np_array = arg_1
    elif isinstance(arg_1, sitk.Image):
        if type == 'sitk':
            image = sitk.Image(arg_1)
        else:
            np_array = pixels(arg_1)
    elif isinstance(arg_1, vtk.vtkImageData):
        if type == 'vtk':
            image = vtk.vtkImageData()
            image.DeepCopy(arg_1)
        else:
            np_array = pixels(arg_1)
    else:
        try:
            np_array = numpy.zeros(arg_1, dtype=data_type)
        except TypeError:
            raise TypeError(f'Object of type \'{arg_1.__class__}\' is not a suitable image initializer')

    if np_array is not None:
        if type == 'sitk':
            image = sitk.GetImageFromArray(np_array)
        elif type == 'vtk':
            vtk_array = numpy_support.numpy_to_vtk(num_array=np_array.ravel(), deep=True)
            image = vtk.vtkImageData()
            image.SetDimensions(np_array.shape)
            image.GetPointData().SetScalars(vtk_array)
        else:
            raise TypeError(f'Image type \'{type}\' not handled')

    if isinstance(arg_1, sitk.Image) or isinstance(arg_1, vtk.vtkImageData):
        globals().update({
            'spacing': arg_1.GetSpacing(),
            'origin': arg_1.GetOrigin(),
            'direction': arg_1.GetDirection(),
        })

    for property in ('spacing', 'origin', 'direction'):
        value = globals()[property]
        if value is not None:
            getattr(image, f'Set{property.title()}')(value)

    return image
