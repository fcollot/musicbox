# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys

from @MBOX_PYSIDE_PACKAGE@.QtCore import Qt
from @MBOX_PYSIDE_PACKAGE@.QtWidgets import QDockWidget, QFileDialog, QLabel, QMainWindow, QMenuBar, QWidget

if '@MBOX_PYSIDE_PACKAGE@' == 'PySide2':
    from @MBOX_PYSIDE_PACKAGE@.QtWidgets import QAction
else:
    from @MBOX_PYSIDE_PACKAGE@.QtGui import QAction


from musicbox.library.console import Console


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._init_console()
        self.setWindowTitle("MusicBox")

    def _init_console(self):
        console_dock = QDockWidget("Python console")
        console_dock.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)
        self.console = Console()
        console_dock.setWidget(self.console)
        self.setCentralWidget(QWidget())

    def showEvent(self, event):
        if self.console:
            self.console.run()
