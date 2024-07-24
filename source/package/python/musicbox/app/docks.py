# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Signal
    from PySide2.QtWidgets import QDockWidget, QFrame, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import QDockWidget, QFrame, QLabel,  QPushButton, QSizePolicy, QVBoxLayout, QWidget

from musicbox.gui import Console


class StartDock(QDockWidget):

    TITLE = "Start"
    open_file = Signal()
    new_project = Signal()
    license = Signal()

    def __init__(self, parent=None):
        super().__init__(self.TITLE, parent)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setTitleBarWidget(QWidget(self))
        root = QWidget()
        self.setWidget(root)
        root.setLayout(QVBoxLayout())

        title_label = QLabel("MusicBox")
        font = title_label.font()
        font.setPointSize(4 * font.pointSize())
        title_label.setFont(font)
        root.layout().addWidget(title_label, 0, Qt.AlignRight)
        root.layout().addWidget(QLabel("Version 1.0.0"), 0, Qt.AlignRight)
        license_button = QPushButton("License...")
        license_button.clicked.connect(self.license)
        license_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        root.layout().addWidget(license_button)

        line = QFrame()
        line.setFrameStyle(QFrame.Panel)
        root.layout().addWidget(line)
        
        button = QPushButton("Open file...")
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        root.layout().addWidget(button)
        button.clicked.connect(self.open_file)

        button = QPushButton("New project")
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        root.layout().addWidget(button)
        button.clicked.connect(self.new_project)

        root.layout().addStretch(1)


class ConsoleDock(QDockWidget):

    TITLE = "Python console"

    expanded_changed = Signal()
    status = Signal(str)

    def __init__(self, parent=None):
        super().__init__(self.TITLE, parent)
        self.setFeatures(QDockWidget.DockWidgetClosable)
        self.setWidget(Console())
        self.setTitleBarWidget(QWidget(self))
        self._is_expanded = False
        self._cursor_inside = False

    def console(self):
        return self.widget()

    def is_expanded(self):
        return self._is_expanded

    def set_expanded(self, expanded):
        if self._is_expanded != expanded:
            self.switch_expand()

    def switch_expand(self):
        self._is_expanded = not self._is_expanded
        self._update_status_message()
        self.expanded_changed.emit()

    def enterEvent(self, event):
        self._cursor_inside = True
        self._update_status_message()
        
    def leaveEvent(self, event):
        self._cursor_inside = False
        self.status.emit(None)

    def mouseDoubleClickEvent(self, event):
        event.accept()
        self.switch_expand()

    def _update_status_message(self):
        if self._cursor_inside:
            if self.is_expanded():
                message = "Double click to reduce the Python console."
            else:
                message = "Double click to expand the Python console."
            self.status.emit(message)


class ToolOptionsDock(QDockWidget):

    TITLE = "Tool options"

    def __init__(self, parent=None):
        super().__init__(self.TITLE, parent)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setWidget(QWidget())


class SceneDock(QDockWidget):

    TITLE = "Scene"

    def __init__(self, parent=None):
        super().__init__(self.TITLE, parent)
        self.setWidget(QWidget())
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.widget().setMinimumWidth(100)
        self.widget().setMaximumWidth(150)      
