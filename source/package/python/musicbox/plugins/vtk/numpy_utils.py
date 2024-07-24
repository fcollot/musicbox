# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy as np
import vtk
from vtk.util import numpy_support


type_correspondance = {
    np.int8: vtk.VTK_TYPE_INT8,
    np.int16: vtk.VTK_TYPE_INT16,
    np.int32: vtk.VTK_TYPE_INT32,
    np.int64: vtk.VTK_TYPE_INT64,
    np.int8: vtk.VTK_TYPE_UINT8,
    np.uint16: vtk.VTK_TYPE_UINT16,
    np.uint32: vtk.VTK_TYPE_UINT32,
    np.uint64: vtk.VTK_TYPE_UINT64,
    np.float32: vtk.VTK_TYPE_FLOAT32,
    np.float64: vtk.VTK_TYPE_FLOAT64,
}


def voxel_set_to_vtk_image(data_set):
    np_array = data_set.voxels
    
    vtk_type = type_correspondance[np_array.dtype.type]
    vtk_array = numpy_support.numpy_to_vtk(num_array=np_array.ravel(), deep=False, array_type=vtk_type)

    shape = np_array.shape
    spacing = data_set.spacing
    origin = data_set.origin

    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(shape[2], shape[1], shape[0])
    vtk_image.SetSpacing(spacing[0], spacing[1], spacing[2])
    vtk_image.SetOrigin(origin[0], origin[1], origin[2])
    vtk_image.GetPointData().SetScalars(vtk_array)

    return vtk_image


