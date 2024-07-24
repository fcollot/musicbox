# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib.util


_pyside_version = None


def pyside_version():
    global _pyside_version
    if _pyside_version is None:
        pyside2_spec = importlib.util.find_spec('PySide2')
        pyside6_spec = importlib.util.find_spec('PySide6')
        
        if pyside6_spec is not None:
            pyside_version = 6
        elif pyside2_spec is not None:
            pyside_version = 2
    return _pyside_version
