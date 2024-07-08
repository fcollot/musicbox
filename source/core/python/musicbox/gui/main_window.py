# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
from . import config, layers, plugins
from .context_toolbar import ContextToolBar
from .file_load import LoadFileAction
from .gui_group import GuiGroup
from .project import Project


if config.pyside_version == 2:
    from PySide2.QtCore import Slot, Qt
    from PySide2.QtWidgets import QAction, QDockWidget, QFileDialog, QLabel, QMainWindow, QMenuBar, QToolBar, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Slot, Qt
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QDockWidget, QFileDialog, QLabel, QMainWindow, QMenuBar, QToolBar, QVBoxLayout, QWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._init_toolbars()
        self._init_console()
        self._init_menu_bar()
        self.setWindowTitle("MusicBox")
        self.setCentralWidget(QWidget())
        GuiGroup.set_provider('main_view', self._add_main_view)

    def _init_toolbars(self):
        self.context_tool_bar = ContextToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.context_tool_bar)

    def _init_console(self):
        self.console_dock = QDockWidget("Python console")
 #       console_dock.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.console_dock)
        self.console = plugins.load_plugin('console')()
        self.console_dock.setWidget(self.console)

    def _init_menu_bar(self):
        menu_bar = self.menuBar()
        self._init_file_menu(menu_bar)

    def _init_file_menu(self, menu_bar):
        file_menu = menu_bar.addMenu("&File")
        load_file_action = LoadFileAction(self)
        load_file_action.output_ready.connect(self.open_project)
        file_menu.addAction(load_file_action)

    def showEvent(self, event):
        super().showEvent(event)
        self.resizeDocks([self.console_dock], [400], Qt.Horizontal)
        if self.console:
            self.console.run()

    def _add_main_view(self):
        return self.centralWidget()

    @Slot(object)
    def open_project(self, initial_data=None):
        project = Project()
        if initial_data is not None:
            project._scene.set_entity(initial_data)
        project.open()
        
        #sys.modules['__main__'].__dict__['layers'] = [image]
        #viewer = plugins.load_plugin('viewer')(image.to_vtk())
        #self.setCentralWidget(viewer)
        #viewer.show()
        
