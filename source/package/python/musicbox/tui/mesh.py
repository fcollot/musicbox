# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import vtk
from vtk.util import numpy_support


def points(object):
    if isinstance(object, vtk.vtkPolyData):
        vtk_array = object.GetPoints().GetData()
        np_array = numpy_support.vtk_to_numpy(vtk_array)
        np_array.shape = (object.GetPoints().GetNumberOfPoints(), 3)
    else:
        raise TypeError
    return np_array


def mesh(arg_1, arg_2=None):
    pass
