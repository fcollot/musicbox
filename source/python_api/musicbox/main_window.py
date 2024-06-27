# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
from PySide@MBOX_PYSIDE_VERSION_MAJOR@.QtCore import Qt
from PySide@MBOX_PYSIDE_VERSION_MAJOR@.QtGui import QAction
from PySide@MBOX_PYSIDE_VERSION_MAJOR@.QtWidgets import QDockWidget, QFileDialog, QLabel, QMainWindow, QMenuBar, QWidget
from .console import Console
from .image import Image
from .itk import init as init_itk
from .viewer import Viewer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.showMaximized()
        self._init_menu_bar()
        init_itk()
        self._init_console()

    def _init_console(self):
        console_dock = QDockWidget("Python console")
        #console_dock.setTitleBarWidget(QWidget())
        dock_arrow = QLabel("⌄")
        #console_dock.titleBarWidget().layout().addWidget(dock_arrow)
        #dockWidget->setAllowedAreas(Qt::LeftDockWidgetArea | Qt::RightDockWidgetArea);
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock);
        console = Console()
        console_dock.setWidget(console)
        console.run()
        self.setCentralWidget(QWidget())

    def _init_menu_bar(self):
        if sys.platform == 'darwin':
            pass
            #self.setMenuBar(QMenuBar())
        else:
            pass
            #self.menuBar().setNativeMenuBar(False)

        menu_bar = self.menuBar()
        self._init_file_menu(menu_bar)

    def _init_file_menu(self, menu_bar):
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("Open image...", self.open_image)

    def open_image(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.mha);;All Files (*)", options=options)
        if filename:
            image = Image(filename)
            viewer = Viewer(image)
            self.setCentralWidget(viewer)
            viewer.show()
