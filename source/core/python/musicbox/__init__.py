# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
from . import config
from .main_window import MainWindow

if config.pyside_version == 2:
    from PySide2.QtWidgets import QApplication
else:
    from PySide6.QtWidgets import QApplication


def run():
    app = QApplication.instance()
    if app is None:
        app : QApplication(sys.argv)

    main_window = MainWindow()
    main_window.showMaximized()

    if config.pyside_version == 2:
        return app.exec_()
    else:
        return app.exec()
