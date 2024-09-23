# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import vtk
from vtk.util import numpy_support

from .data_base import ImageBase





class NumpyImage(ImageBase, numpy.ndarray):

    @classmethod
    def _deep_copy(cls, object):
        if isinstance(object, ImageBase):
            np_array = object.as_numpy()
            spacing = object.spacing
            origin = object.origin
            direction = object.direction
        elif isinstance(object, numpy.ndarray):
            np_array = object
            spacing = None
            origin = None
            direction = None
        elif isinstance(object, vtk.vtkImageData):
            np_array = numpy_support.vtk_to_numpy(object.GetPointData().GetScalars())
            np_array.shape = object.dimensions()
            spacing = object.GetSpacing()
            origin = object.GetOrigin()
            direction = object.GetDirection()
        else:
            raise TypeError
        if spacing is not None:
            image.SetSpacing(spacing)
        if origin is not None:
            image.SetOrigin(origin)
        if direction is not None:
            image.SetDirection(direction)
        return image

    @classmethod
    def create_from_numpy(cls, np_array):
        image = cls(np_array.shape, dtype=np_array.dtype, buffer=np_array.data)
        return image

    def __init__(self, *args, **kwargs):
        ImageBase.__init__()
        numpy.ndarray.__init__(*args, **kwargs)

    def as_numpy(self):
        return self

    def _create_vtk_view(self):
        view = VTKImage.from_object(self, deep_copy=False)
        view._numpy_view = self
        return view

    def _spacing(self):
        return self.as_vtk().GetSpacing()

    def _set_spacing(self, value):
        self.as_vtk().SetSpacing(value)

    def _origin(self):
        return self.as_vtk().GetOrigin()

    def _set_origin(self, value):
        self.as_vtk().SetOrigin(value)

    def _direction(self):
        return self.as_vtk().GetDirection()

    def _set_direction(self, value):
        self.as_vtk().SetDirection(value)
