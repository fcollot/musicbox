# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Signal
    from PySide2.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QPushButton, QToolBar, QWidget
else:
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QPushButton, QToolBar, QWidget

#from musicbox.gui import StatusMessageWidget


class ToolBar(QToolBar):

    console_toggled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        #console_button = QPushButton("Python console")
        #console_button.setCheckable(True)
        #console_button.clicked.connect(self.console_toggled)
        #self.addWidget(console_button)

        self.addSeparator()
