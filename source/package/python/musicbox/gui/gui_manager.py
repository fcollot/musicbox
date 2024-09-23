# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Slot
else:
    from PySide6.QtCore import Slot

from musicbox.core import Singleton


class GuiManager(Singleton):

    def __init__(self):
        super().__init__()

    def _singleton_init(self, first):
        pass

    
