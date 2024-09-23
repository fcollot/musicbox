# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import vtk
from vtk.util import numpy_support

from .data_base import ImageBase


class VTKImage(ImageBase, vtk.vtkImageData):

    @classmethod
    def _deep_copy(cls, object):
        if isinstance(object, vtk.vtkImageData):
            image = cls()
            image.DeepCopy(object)
        else:
            if isinstance(object, ImageBase):
                image = cls()
                image.DeepCopy(object.as_vtk())
            elif isinstance(object, numpy.ndarray):
                vtk_array = numpy_support.numpy_to_vtk(num_array=object.ravel(), deep=True)
                image = cls()
                image.SetDimensions(object.shape)
                image.GetPointData().SetScalars(vtk_array)
            else:
                raise TypeError
        return image

    @classmethod
    def create_from_numpy(cls, np_array):
        vtk_array = numpy_support.numpy_to_vtk(num_array=np_array.ravel(), deep=False)
        image = cls()
        image._np_array = np_array
        image.SetDimensions(np_array.shape)
        image.GetPointData().SetScalars(vtk_array)
        return image

    def __init__(self):
        ImageBase.__init__()
        vtk.vtkImageData.__init__()
        self._np_array = None

    def as_vtk(self):
        return self

    def as_numpy(self):
        if self._np_array is None:
            self._np_array = numpy_support.vtk_to_numpy(self.GetPointData().GetScalars())
            self._np_array.shape = self.dimensions()
        
        return self._np_array

    def _spacing(self):
        return self.GetSpacing()

    def _set_spacing(self, value):
        self.SetSpacing(value)

    def _origin(self):
        return self.GetOrigin()

    def _set_origin(self, value):
        self.SetOrigin(value)

    def _direction(self):
        return self.GetDirection()

    def _set_direction(self, value):
        self.SetDirection(value)
