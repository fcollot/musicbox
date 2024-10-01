# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from threading import Lock

from musicbox.core import dev
from .view import View


dev.add_loaded_module(__name__)


if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, Signal, SLot
else:
    from PySide6.QtCore import QObject, Signal, Slot


_lock = Lock()
_instance = None


def instance():
    with _lock:
        if not _instance:
            global _instance
            _instance = GUIProxy()
        return _instance


class GUIProxy(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(parent)
    def create_view(self, parent=None):
        
