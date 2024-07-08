# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config
from .view import SliceView

if config.pyside_version == 2:
    from PySide2.QtWidgets import QGridLayout, QWidget
else:
    from PySide6.QtWidgets import QGridLayout, QWidget, QLabel


class SceneView(QWidget):

    def __init__(self, parent=None, *, scene=None, viewer_plugin=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)
        view = SliceView(viewer_plugin)
        layout.addWidget(view, 0, 0)
#        layout.addWidget(view.SliceView(viewer_plugin), 0, 1)
#        layout.addWidget(view.SliceView(viewer_plugin), 1, 0)
        self.scene = scene
        view.add_scene(scene)
