# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Slot
    from PySide2.QtWidgets import QLabel, QProgressBar, QStatusBar
else:
    from PySide6.QtCore import Slot
    from PySide6.QtWidgets import QLabel, QProgressBar, QStatusBar


class StatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._message_owner = None
        self._labels = {}
        self._progress_bars = {}

    @Slot(str)
    @Slot(str, int)
    def set_message(self, message=None, timeout=0):
        if message is None:
            self.remove_message()
        else:
            self.showMessage(message)
            if timeout == 0:
                self._message_owner = self.sender()

    @Slot(object)
    def remove_message(self):
        if self._message_owner is self.sender():
            self.clearMessage()
            self_message_owner = None

    def add_label(self, name, initial_text=""):
        label = QLabel(initial_text)
        self.addWidget(label)
        return label

    def remove_label(self, name):
        try:
            label = self._labels.pop(name)
            self.removeWidget(label)
        except:
            pass

    def add_progress_bar(self, name, title=None):
        if title is not None:
            label = QLabel(title + ":")
            self._labels[name] = label
            self.addWidget(label)
        progress_bar = QProgressBar()
        self._progress_bars[name] = progress_bar
        self.addWidget(progress_bar)
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        return progress_bar

    def remove_progress_bar(self, name):
        self.remove_label(name)
        try:
            progress_bar = self._progress_bars.pop(name)
            self.removeWidget(progress_bar)
        except:
            pass
