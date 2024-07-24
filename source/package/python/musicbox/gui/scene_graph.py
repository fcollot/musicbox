# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .. import config


if config.pyside_version() == 2:
    from PySide2.QtWidgets import QTreeView, QWidget
else:
    from PySide6.QtWidgets import QTreeView, QWidget


class SceneGraphView(QtWidget):

    def __init__(self, scene_graph):
        self._scene_graph = scene_graph
        self.setLayout(QVBoxLayout())
        self._tree_view = QTreeView()
        self._tree_view.setModel(scene_graph.model())
        self.layout().addWidget(self._tree_view)
