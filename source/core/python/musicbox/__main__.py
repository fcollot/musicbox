# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
from . import config, run

if config.pyside_version  == 2:
    from PySide2.QtWidgets import QApplication
else:
    from PySide6.QtWidgets import QApplication


app = QApplication(sys.argv)
app.setApplicationName("MusicBox")

run()
