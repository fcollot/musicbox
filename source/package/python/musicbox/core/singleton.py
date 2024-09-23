# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import abc


class Singleton(abc.ABC):

    def __init__(self, *args, **kwargs):
        cls = type(self)
        try:
            first_instance = cls._first_instance
        except AttributeError:
            cls._first_instance = self
            first_instance = None
        finally:
            self._singleton_init(first_instance, *args, **kwargs)

    @abc.abstractmethod
    def _singleton_init(self, first_instance):
        pass
