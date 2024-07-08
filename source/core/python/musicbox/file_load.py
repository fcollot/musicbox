# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config, plugins

if config.pyside_version == 2:
    from PySide2.QtCore import Signal, Slot
    from PySide2.QtWidgets import QAction, QFileDialog
else:
    from PySide6.QtCore import Signal, Slot
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QFileDialog


readers = None


def ensure_init():
    global readers
    if readers is None:
        readers = [plugins.load_plugin('reader', reader_name)() for reader_name in plugins.find_plugins('reader')]


class LoadFileAction(QAction):

    name = "Open file"
    output_ready = Signal(object)
    failed = Signal()

    def __init__(self, parent):
        super().__init__(f'{self.name}...', parent)
        ensure_init()
        self.triggered.connect(self.select_file)

    def load_file(self, filename):
        for reader in readers:
            data = reader.read(filename)
            if data:
                self.output_ready.emit(data)
                return data
        return None

    @Slot()
    def select_file(self):
        file_filters = [f'{definition} ({", ".join(extensions)})' for reader in readers for definition, extensions in reader.file_filters().items()]
        file_filters.sort()
        file_filters.append("All Files (*)")
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self.parent(), self.name, "", ';;'.join(file_filters), options=options)
        if filename:
            data = self.load_file(filename)
            if data is None:
                self.failed.emit()
