# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from traceback import print_exception

from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Slot
    from PySide2.QtWidgets import QMainWindow, QTabWidget
else:
    from PySide6.QtCore import Qt, Slot
    from PySide6.QtWidgets import QMainWindow, QTabWidget

from musicbox.core import Messenger
from musicbox.gui import CodeEditor

from .actions import create_main_actions
from .docks import ConsoleDock, StartDock, ToolOptionsDock, SceneDock
from .menu_bar import setup_menu_bar
from .tool_bar import ToolBar
from .status_bar import StatusBar
from .welcome import WelcomeWidget


class MainWindow(QMainWindow):

    CONSOLE_NORMAL_HEIGHT = 100
    CONSOLE_EXPANDED_HEIGHT = 400

    def __init__(self, *, messenger=Messenger()):
        super().__init__()
        self._messenger = messenger
        self._actions = create_main_actions(self)
        self._init_window()
        self._init_status_bar()
        self._init_main_view()
        self._init_docks()
        self._init_menu_bar()
        self._init_tool_bar()
        self._tool_bar.hide()
 
    def _init_window(self):
        self.setWindowTitle("MusicBox")

    def _init_status_bar(self):
        self.setStatusBar(StatusBar())

    def _init_main_view(self):
        main_view = QTabWidget()
        self.setCentralWidget(main_view)
        main_view.setTabBarAutoHide(True)
        welcome_widget = WelcomeWidget()
        self._welcome_widget = welcome_widget
        main_view.addTab(welcome_widget, "Welcome")
        welcome_widget.link_hovered.connect(self.statusBar().set_message)
        welcome_widget.link_unhovered.connect(self.statusBar().remove_message)
        #welcome_widget.open_file.connect(self.load_file_action.trigger)
        #welcome_widget.open_file[str].connect(self.open_project)
        #welcome_widget.new_project.connect(self.open_project)
        main_view.addTab(CodeEditor(), "Editor")

    def _init_docks(self):
        start_dock = StartDock()
        console_dock = ConsoleDock()
#        tool_options_dock = ToolOptionsDock()
#        scene_dock = SceneDock()
        
        self._docks = {
            'start': start_dock,
            'console': console_dock,
#            'tool_options': tool_options_dock,
#            'scene': scene_dock,
        }

#        self.addDockWidget(Qt.LeftDockWidgetArea, scene_dock)
#        self.addDockWidget(Qt.LeftDockWidgetArea, tool_options_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, start_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)

        start_dock.license.connect(self._actions['show_license'].triggered)

        console_dock.expanded_changed.connect(self._update_dock_sizes)
        console_dock.status.connect(self.statusBar().set_message)
        console_dock.console().exit.connect(self.exit)
        console_dock.console().run()

        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        #self.tabifyDockWidget(self.tool_options_dock, self.console_dock)
        #self.setTabPosition(self.dock_area, Gui.TabWidget.North)

    def _init_menu_bar(self):
        setup_menu_bar(self.menuBar(), self._actions)

    def _init_tool_bar(self):
        self._tool_bar = ToolBar(self)
        self._tool_bar.setMovable(False)
        self._tool_bar.setFloatable(False)
        self.addToolBar(Qt.BottomToolBarArea, self._tool_bar)
        self._tool_bar.addAction(self._docks['console'].toggleViewAction())
        self._tool_bar.addSeparator()
        self._tool_bar.addAction("Filtering").setEnabled(False)
        self._tool_bar.addAction("Segmentation")
        self._tool_bar.addAction("Registration")
        self._tool_bar.addAction("Meshing")

    def showEvent(self, event):
        super().showEvent(event)
        #self._update_dock_sizes()

    def show_welcome_page(self):
        self._docks['console'].set_expanded(True)

    def set_plugin_preloader(self, preloader):
        self._plugin_preloader = preloader
        progress_bar = self.statusBar().add_progress_bar('plugins', "Loading plugins")
        preloader.progress_changed.connect(progress_bar.setValue)
        preloader.finished.connect(self.plugins_loaded)
        if preloader.is_finished():
            self.plugins_loaded()

    @Slot()
    def plugins_loaded(self):
        self.statusBar().remove_progress_bar('plugins')
        del self._plugin_preloader

    @Slot()
    def _update_dock_sizes(self):
        console_dock = self._docks['console']
        if console_dock.is_expanded():
            size = self.CONSOLE_EXPANDED_HEIGHT
        else:
            size = self.CONSOLE_NORMAL_HEIGHT
        self.resizeDocks([console_dock], [size], Qt.Vertical)
        self.layout().activate()

    @Slot(object)
    def open_project(self, initial_data=None):
        project = Project()
        if initial_data is not None:
            if isinstance(initial_data, str):
                initial_data = load_file(initial_data)
            project.scene().set_entity(initial_data)
        self._gui_groups.append(ProjectGroup(project))

    @Slot()
    def exit(self):
        self.close()
