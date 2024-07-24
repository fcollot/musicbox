# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QStandardItem, QStandardItemModel
else:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QStandardItem, QStandardItemModel


class SceneNode():

    def __init__(self, contents=None):
        self._item = QStandardItem()
        if contents is not None:
            self._item.setData(contents, Qt.UserRole)

    def add_node(self, node):
        node._item.appendRow(self._item)


class Scene():

    def __init__(self, root_node=None, parent=None):
        self._model = QStandardItemModel(self)
        if root_node is not None:
            self.set_root_node(root_node)

    def model(self):
        return self._model

    def set_root_node(self, node):
        self._model.setItem(0, node)
