# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import SimpleITK as sitk

from .file import FileReader
from .image_base import ImageBase
from .vtk import VTKImage


class SITKImage(ImageBase, sitk.Image):

    @classmethod
    def _deep_copy(cls, object):
        if isinstance(object, sitk.Image):
            image = cls(object)
        else:
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
            else:
                raise TypeError
            image = sitk.GetImageFromArray(np_array)
            image.__class__ = cls
            if spacing is not None:
                image.SetSpacing(spacing)
            if origin is not None:
                image.SetOrigin(origin)
            if direction is not None:
                image.SetDirection(direction)
        return image

    @classmethod
    def _from_object(cls, object, *, deep_copy=True):
        if isinstance(object, numpy.ndarray):
            if not deep_copy:
                raise ValueError(f'{cls}.from_object method cannot deep copy numpy arrays')
            image = sitk.GetImageFromArray(object)
            image.__class__ = cls
        elif isinstance(object, sitk.Image):
            if deep_copy:
                image = cls(object)
            else:
                image = object
                image.__class__ = cls
        else:
            raise TypeError
        return image

    def __init__(self, *args, **kwargs):
        vtk_view = self._create_vtk_view()
        numpy_view = self._create_numpy_view()
        ImageBase.__init__(vtk_view=vtk_view, numpy_view=numpy_view)
        sitk.Image.__init__(*args, **kwargs)

    def _create_vtk_view(self):
        view = VTKImage.from_object(sitk.GetArrayViewFromImage(self), deep_copy=False)
        view.spacing = self.spacing
        view.origin = self.origin
        view.direction = self.direction
        return view

    def _create_numpy_view(self):
        return self.as_vtk().as_numpy()

    def _spacing(self):
        return self.GetSpacing()

    def _set_spacing(self, value):
        self.SetSpacing(value)
        self.as_vtk().SetSpacing(value)

    def _origin(self):
        return self.GetOrigin()

    def _set_origin(self, value):
        self.SetOrigin(value)
        self.as_vtk().SetOrigin(value)

    def _direction(self):
        return self.GetDirection()

    def _set_direction(self, value):
        self.SetDirection(value)
        self.as_vtk().SetDirection(value)


class SITKImageReader():

    @staticmethod
    def filters():
        return {'ITK image': ['*.mha']}

    def read(self, path):
        sitk_image = sitk.ReadImage(path)
