# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import abc

import numpy


class ImageBase(abc.ABC):

    @classmethod
    def deep_copy(cls, object):
    try:
        image = cls._deep_copy(object)
        return image
    except TypeError:
        raise TypeError(f'Object of type \'{object.__class__}\' is not handled')

    @classmethod
    @abc.abstractmethod
    def _deep_copy(cls, object):
        return

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

    @abc.abstractmethod
    def as_numpy(self):
        return

    @abc.abstractmethod
    def as_vtk(self):
         return
