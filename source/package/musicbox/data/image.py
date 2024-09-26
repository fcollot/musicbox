# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import SimpleITK as sitk
import vtk
from vtk.util import numpy_support

from musicbox.core import dev


dev.add_loaded_module(__name__)


sitk_type_map = {
    numpy.int8: sitk.sitkInt8,
    numpy.int16: sitk.sitkInt16,
    numpy.int32: sitk.sitkInt32,
    numpy.int64: sitk.sitkInt64,
    numpy.uint8: sitk.sitkUInt8,
    numpy.uint16: sitk.sitkUInt16,
    numpy.uint32: sitk.sitkUInt32,
    numpy.uint64: sitk.sitkUInt64,
    numpy.float32: sitk.sitkFloat32,
    numpy.float64: sitk.sitkFloat64,
}



vtk_type_map = {
    numpy.int8: vtk.VTK_TYPE_INT8,
    numpy.int16: vtk.VTK_TYPE_INT16,
    numpy.int32: vtk.VTK_TYPE_INT32,
    numpy.int64: vtk.VTK_TYPE_INT64,
    numpy.uint8: vtk.VTK_TYPE_UINT8,
    numpy.uint16: vtk.VTK_TYPE_UINT16,
    numpy.uint32: vtk.VTK_TYPE_UINT32,
    numpy.uint64: vtk.VTK_TYPE_UINT64,
    numpy.float32: vtk.VTK_TYPE_FLOAT32,
    numpy.float64: vtk.VTK_TYPE_FLOAT64,
}


def create_sitk_image(arg_1, data_type=None, *, spacing=None, origin=None, direction=None):
    if isinstance(arg_1, sitk.Image):
        if data_type:
            _raise_no_second_argument_needed_error(arg_1)
        image = sitk.Image(arg_1)
    elif isinstance(arg_1, numpy.ndarray):
        if data_type:
            _raise_no_second_argument_needed_error(arg_1)
        image = sitk.GetImageFromArray(arg_1)
    elif isinstance(arg_1, vtk.vtkImageData):
        if data_type:
            _raise_no_second_argument_needed_error(arg_1)
        vtk_array = arg_1.GetPointData().GetScalars()
        np_array = numpy_support.vtk_to_numpy(vtk_array)
        np_array.shape = arg_1.GetDimensions()
        image = sitk.GetImageFromArray(np_array)
    else:
        shape = arg_1
        data_type = data_type or sitk.sitkUInt8
        if data_type in sitk_type_map:
            data_type = sitk_type_map[data_type]
        image = sitk.Image(*shape, data_type)
    _set_image_attributes(image, spacing=spacing, origin=origin, direction=direction)
    return image


def create_vtk_image(arg_1, data_type=None, *, spacing=None, origin=None, direction=None):
    image = vtk.vtkImageData()
    if isinstance(arg_1, vtk.vtkImageData):
        if data_type:
            _raise_no_second_argument_needed_error(arg_1)
        image.DeepCopy(arg_1)
    else:
        if isinstance(arg_1, numpy.ndarray):
            if data_type:
                _raise_no_second_argument_needed_error(arg_1)
            np_array = arg_1
        elif isinstance(arg_1, sitk.Image):
            if data_type:
                _raise_no_second_argument_needed_error(arg_1)
            np_array = sitk.GetArrayViewFromImage(arg_1)
        else:
            shape = arg_1
            data_type = data_type or numpy.uint8
            np_array = numpy.zeros(shape, dtype=data_type)
        if np_array.ndim != 3:
            raise TypeError('VTK images must have 3 dimensions (use SimpleITK images for other dimensions).')
        vtk_array = numpy_support.numpy_to_vtk(num_array=np_array.reshape(-1), deep=True)
        image.SetDimensions(np_array.shape)
        image.GetPointData().SetScalars(vtk_array)
    _set_image_attributes(image, spacing=spacing, origin=origin, direction=direction)
    return image


def _set_image_attributes(image, *, spacing=None, origin=None, direction=None):
    if spacing:
        image.SetSpacing(spacing)
    if origin:
        image.SetOrigin(origin)
    if direction:
        image.SetDirection(direction)


def pixels(image):
    if isinstance(image, sitk.Image):
        np_array = sitk.GetArrayViewFromImage(image)
    elif isinstance(image, vtk.vtkImageData):
        vtk_array = image.GetPointData().GetScalars()
        np_array = numpy_support.vtk_to_numpy(vtk_array)
        np_array.shape = image.GetDimensions()
    elif isinstance(image, numpy.ndarray):
        np_array = image
    else:
        raise TypeError(f'Argument type not handled: {type(image)}.')
    return np_array
