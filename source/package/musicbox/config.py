# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib.util
from threading import RLock

from .core import dev


dev.add_loaded_module(__name__)


_pyside_version = None
_lock = RLock()


def pyside_version():
    """Return the PySide version to use in the application.

    Use this function to choose which PySide modules to import.
    """
    with _lock:
        global _pyside_version
        if _pyside_version is None:
            pyside6_spec = importlib.util.find_spec('PySide6')
            if pyside6_spec is not None:
                pyside_version = 6
            else:
                pyside2_spec = importlib.util.find_spec('PySide2')
                if pyside2_spec is not None:
                    pyside_version = 2
                else:
                    raise ModuleNotFoundError("PySide 2 or 6 is required")
        return _pyside_version
