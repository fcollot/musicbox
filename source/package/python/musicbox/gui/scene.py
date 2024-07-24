# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from enum import Enum

from .. import config

if config.pyside_version() == 2:
    from PySide2.QtWidgets import QGridLayout, QTabWidget, QVBoxLayout, QWidget
else:
    from PySide6.QtWidgets import QGridLayout, QTabWidget, QVBoxLayout, QWidget

from musicbox.core import PluginLoader


class SceneWorkspace():

    def __init__(self, *, main_view, graph_view, toolbar, tool_options):
        self._main_view = main_view
        self._graph_view = graph_view
        self._toolbar = toolbar
        self._tool_options = tool_options

    def _init_main_view(self):
        self._main_view = QTabWidget()
        self._main_view.setTabBarAutoHide(True)

    def _init_graph_view(self):
        pass

class SceneInterface():

    def __init__(self, scene):
        


class SceneView(QWidget):

    Mode = Enum('Mode', ['FRONT', 'RIGHT', 'TOP_FROM_FRONT', 'MOVING'])

    def __init__(self, scene, parent=None, *, mode=Mode.FRONT):
        super().__init__(parent)
        self._scenes = scene
        self._viewer = PluginLoader('viewer').load(config.default_viewer)()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._viewer)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def install_viewer_event_filter(self, event_filter):
        self._viewer.viewer_backend().installEventFilter(event_filter)


class SceneMultiView(QWidget):

    Mode = Enum('Mode', ['SINGLE', 'THREE', 'FOUR'])

    def __init__(self, scene, parent=None, *, mode=Mode.FOUR):
        self._scene = scene
        self._mode = mode
        self._views = {}
        
        self.setLayout(QGridLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        if mode is Mode.SINGLE:
            self._setup_view('single', 0, 0)
        elif mode is Mode.THREE:
            self._setup_view('left', 0, 0, SceneView.Mode.FRONT)
            self._setup_view('middle', 0, 1, SceneView.Mode.RIGHT)
            self._setup_view('right', 0, 2, SceneView.Mode.TOP_FROM_FRONT)
        else:
            self._setup_view('topleft', 0, 0, SceneView.Mode.TOP_FROM_FRONT)
            self._setup_view('topright', 0, 1, SceneView.Mode.MOVING)
            self._setup_view('bottomleft', 1, 0, SceneView.Mode.FRONT)
            self._setup_view('bottomright', 1, SceneView.Mode.RIGHT)

    def _setup_view(self, name, x, y, mode):
        view = SceneView(self._scene, mode=mode)
        self._views[name] = view
        self.layout().addWidget(view, x, y)
