# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox import config

if config.pyside_version == 2:
    from PySide2.QtCore import Slot, Qt
    from PySide2.QtWidgets import QAction, QDockWidget, QFileDialog, QLabel, QMainWindow, QMenuBar, QToolBar, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Slot, Qt
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QDockWidget, QFileDialog, QLabel, QMainWindow, QMenuBar, QToolBar, QVBoxLayout, QWidget


class Widget(QWidget):
    pass


class MainWindow(QMainWindow):

    def set_title(title):
        self.setWindowTitle(title)
