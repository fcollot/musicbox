# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Signal
    from PySide2.QtWidgets import QWidget
else:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import QWidget


class 
