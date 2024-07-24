# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import abc

import numpy
import SimpleITK as sitk
import vtk
from vtk.util import numpy_support


class Image(abc.ABC):

    @classmethod
    def from_object(cls, object, *, deep_copy=True):
        try:
            image = cls._from_object(object, deep_copy=deep_copy)
            if isinstance(object, Image):
                image.spacing = object.spacing
                image.origin = object.origin
                image.direction = object.direction
            return image
        except TypeError:
            if isinstance(object, Image) and not isinstance(object, NumpyImage):
                return cls.from_object(object.as_numpy(), deep_copy=deep_copy)
            else:
                raise TypeError(f'Object of type \'{object.__class__}\' is not handled by {cls}.from_object')

    @classmethod
    @abc.abstractmethod
    def _from_object(cls, object, *, deep_copy=True):
        return

    def __init__(self, *args, **kwargs):
        self.native_type().__init__(*args, **kwargs)

    @property
    def spacing(self):
        return self._spacing()

    @spacing.setter
    def spacing(self, value):
        self._set_spacing(value)

    @property
    def origin(self):
        return self._origin()

    @origin.setter
    def origin(self, value):
        self._set_origin(value)

    @property
    def direction(self):
        return self._direction()

    @direction.setter
    def direction(self, value):
        self._set_direction(value)

    @abc.abstractmethod
    def _spacing(self):
        return

    @abc.abstractmethod
    def _set_spacing(self, value):
        pass

    @abc.abstractmethod
    def _origin(self):
        return

    @abc.abstractmethod
    def _set_origin(self, value):
        pass

    @abc.abstractmethod
    def _direction(self):
        return

    @abc.abstractmethod
    def _set_direction(self, value):
        pass

    def as_numpy(self):
        view = None
        try:
            view  = self._numpy_view
        except AttributeError:
            view = self._create_numpy_view()
            self._numpy_view = view
        return view

    def as_vtk(self):
        view = None
        try:
            view  = self._vtk_view
        except AttributeError:
            view = self._create_vtk_view()
            self._vtk_view = view
        return view

    @abc.abstractmethod
    def _create_numpy_view(self):
        return

    @abc.abstractmethod
    def _create_vtk_view(self):
        return


class NumpyImage(Image, numpy.ndarray):

    @classmethod
    def _from_object(cls, object, *, deep_copy=True):
        if isinstance(object, numpy.ndarray):
            if deep_copy:
                object = object.copy()
            image = cls(object.shape, dtype=object.dtype, buffer=object.data)
            if deep_copy and isinstance(object, cls) and hasattr(object, '_vtk_view'):
                image._vtk_view = object._vtk_view
        elif isinstance(object, vtk.vtkImageData):
            if isinstance(object, VTKImage):
                image = cls._from_object(object.as_numpy(), deep_copy=deep_copy)
            else:
                image = VTKImage.from_object(object, deep_copy=deep_copy).as_numpy()
        return image

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


class VTKImage(Image, vtk.vtkImageData):

    @classmethod
    def _from_object(cls, object, *, deep_copy=True):
        if isinstance(object, numpy.ndarray):
            if isinstance(object, NumpyImage):
                image = cls._from_object(object.as_vtk(), deep_copy=deep_copy)
            else:
                vtk_array = numpy_support.numpy_to_vtk(num_array=object.ravel(), deep=deep_copy)
                image = cls()
                image.SetDimensions(object.shape)
                image.GetPointData().SetScalars(vtk_array)
        elif isinstance(object, vtk.vtkImageData):
            image = cls()
            if deep_copy:
                image.DeepCopy(object)
            else:
                image.ShallowCopy(object)
                if isinstance(object, cls) and hasattr(object, '_numpy_view'):
                    image._numpy_view = object._numpy_view
        else:
            raise TypeError
        return image

    def as_vtk(self):
        return self

    def _create_numpy_view(self):
        np_array = numpy_support.vtk_to_numpy(self.GetPointData().GetScalars())
        np_array.shape = self.dimensions()
        view = NumpyImage.from_object(np_array, deep_copy=False)
        view._vtk_view = self
        return view

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


class SITKImage(Image, sitk.Image):

    @classmethod
    def _from_object(cls, object, *, deep_copy=True):
        if isinstance(object, numpy.ndarray):
            if not deep_copy:
                raise ValueError(f'{cls}.from_object method cannot deep copy numpy arrays')
            image = sitk.GetImageFromArray(object)
            image.__class__ = cls
        elif isinstance(object, sitk.Image):
            if deep_copy:
                image = cls(sitkImage)
            else:
                image = object
                image.__class__ = cls
                if isinstance(object, cls) and hasattr(object, '_vtk_view'):
                    image._vtk_view = object._vtk_view
        else:
            raise TypeError
        return image

    def _create_vtk_view(self):
        return VTKImage.from_object(sitk.GetArrayViewFromImage(self), deep_copy=False)

    def _create_numpy_view(self):
        return self.as_vtk().as_numpy()

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


_typename2class = {
    'numpy': NumpyImage,
    'sitk': SITKImage,
    'vtk': VTKImage,
}


def image(arg_1, *, type='numpy', data_type=float, spacing=None, origin=None, direction=None):
    try:
        image_class = _typename2class[type]
    except KeyError:
        raise ValueError(f'Unknown image type \'{type}\'')
    properties = {}
    new_image = None
    try:
        new_image = image_class.from_object(arg_1)
    except TypeError:
        try:
            np_array = numpy.zeros(arg_1, dtype=data_type)
            new_image = getattr(image_class, 'from_object')(np_array)
        except TypeError:
            raise TypeError(f'Argument of type \'{arg_1.__class__}\' is not handled')
    if spacing is not None:
        properties['spacing'] = spacing
    if origin is not None:
        properties['origin'] = origin
    if direction is not None:
        properties['direction'] = direction
    for property, value in properties.items():
        setattr(new_image, property, value)
    return new_image
