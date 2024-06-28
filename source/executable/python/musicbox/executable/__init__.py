# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from @MBOX_PYSIDE_PACKAGE@.QtCore import Qt
from @MBOX_PYSIDE_PACKAGE@.QtWidgets import QApplication

from .main_window import MainWindow


main_window = None


def init():
    global main_window
    main_window = MainWindow()
    main_window.showMaximized()


def run():
    app = QApplication()
    app.setApplicationName("MusicBox")
    init()
    if '@MBOX_PYSIDE_PACKAGE@' == 'PySide2':
        return app.exec_()
    else:
        return app.exec()
