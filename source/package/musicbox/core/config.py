# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib.metadata
import importlib.util
from threading import Lock


_pyside_version = None
_lock = Lock()


def application_name():
    """The display name of the application.

    This is the name used in the GUI, which may differ from the package or
    project names.
    """

    return "MusicBox"


def application_version():
    return importlib.metadata.version('musicbox')


def pyside_version():
    """The PySide version to use in the application.

    Use this function to choose which PySide modules to import.

    The function searches for version 6 and, if not found, falls back to
    version 2.  

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
                    raise ModuleNotFoundError("This packages requires PySide 2 or 6 (perferably 6).")

        return _pyside_version


def gui_enabled():
    """Check if GUI functionality is enabled.

    Calling this function before the application is created will always return False.
    """

    if pyside_version() == 2:
        from PySide2.QtCore import QApplication, QCoreApplication
    else:
        from PySide6.QtCore import QApplication, QCoreApplication

    app = QCoreApplication.instance()
    return app and isinstance(app, QApplication)
