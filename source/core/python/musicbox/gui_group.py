# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


class GuiGroup():

    _providers = {}

    @classmethod
    def set_provider(cls, category, provider):
        cls._providers[category] = provider

    def __init__(self, specs):
        self._specs = specs
        self._components = {}

    def __getitem__(self, key):
        return self._components.setdefault(key, self._providers[self._specs[key]]())

    def __delitem__(self, key):
        del self._components[key]
