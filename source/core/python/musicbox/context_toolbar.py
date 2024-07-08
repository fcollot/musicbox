# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config

if config.pyside_version == 2:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QToolBar
else:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QToolBar

from . import layers, filter


class ContextToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        layers.ensure_init()
        filter_action = filter.FilterAction(self, input_producer=layers.layers.get)
        filter_action.setEnabled(False)
        self.addAction(filter_action)
