# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from pathlib import Path
import json

from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, Qt, Signal, Slot
    from PySide2.QtGui import QStandardItem, QStandardItemModel
else:
    from PySide6.QtCore import QObject, Qt, Signal, Slot
    from PySide6.QtGui import QStandardItem, QStandardItemModel


from . import file


class SceneNode(QStandardItem, file.Encodable):

    @classmethod
    def decode(cls, value):
        data = value['data'].decode()
        node = cls(node, data)
        for child_dict in value['children']:
            add_child(cls.decode(child_dict))
        return node

    def __init__(self, data=None):
        QStandardItem.__init__()
        self.setData(data, Qt.UserRole)

    def data(self):
        return self.getData(Qt.UserRole)

    def add_child(self, child):
        self.appendRow(child)

    def encode(self):
        return {
            'data': self.data().encode(),
            'children':  {self.child(i).encode() for i in range(self.rowCount())},
        }


class Scene(QStandardItemModel, file.Encodable):

    def __init__(self, name, path, root_node=None):
        QStandardItemModel.__init()
        self._name = name
        self._path = Path(path).resolve()
        if not self._path.exists():
            raise RuntimeError(f'The scene path does not exist: {self._path}')
        self._model = QStandardItemModel(self)
        if root_node is not None:
            self.set_root_node(root_node)

    def __eq__(self, other):
        return all((
            isinstance(other, Scene),
            self.name() == other.name(),
            self.path() == other.path(),
        ))

    def __hash__(self):
        return hash((self.name(), self.path()))

    def encode(self):
        return self.root_node().encode()

    def name(self):
        return self._properties['name']

    def path(self):
        return self._path

    def model(self):
        return self._model

    def set_root_node(self, node):
        self._model.setItem(0, node)


