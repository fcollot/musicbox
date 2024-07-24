# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Signal, Slot
    from PySide2.QtWidgets import QAction, QFileDialog
else:
    from PySide6.QtCore import Signal, Slot
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QFileDialog

from musicbox.core import Settings


class LoadFileAction(QAction):

    output_ready = Signal(object)
    failed = Signal(Exception)

    def __init__(self, title , parent=None, *, readers, select_multiple=False, add_to_recent=False):
        super().__init__(f'{title}...', parent)
        self._title = title
        self._select_multiple = select_multiple
        self._add_to_recent = add_to_recent
        self.triggered.connect(self._select_file)
        self._filter_to_reader = {}
        for reader in readers:
            filters = [f'{definition} ({", ".join(extensions)})' for definition, extensions in reader.file_types().items()]
            for filter in filters:
                if filter in self._filter_to_reader:
                    self.duplicate_filter.emit(reader, filter)
                else:
                    self._filter_to_reader[filter] = filter

    @Slot()
    def _select_file(self):
        filters = self._filter_to_reader.keys()
        if self._select_multiple:
            paths, selected_filter = QFileDialog.getOpenFileNames(self.parent(), self._title, "", ';;'.join(filters))
        else:
            path, selected_filter = QFileDialog.getOpenFileName(self.parent(), self._title, "", ';;'.join(filters))
            paths = [path] if path else None
        if paths:
            reader = self.reader_for_filter(selected_filter)
            self._handle_paths(paths, reader)

    def _handle_paths(self, paths, reader):
        try:
            data = [reader.read(path) for path in paths]
        except Exception as e:
            self.failed.emit(e)
        else:
            if self._add_to_recent:
                settings = Settings()
                recent_files = settings.get_value('recent_files', [])
                for path in paths:
                    if path in recent_files:
                        recent_files.remove(path)
                    recent_files.insert(0, path)
                while len(recent_files) > 10:
                    recent_files.pop()
                settings.set_value('recent_files', recent_files)
            if not self._select_multiple:
                data = data[0]
            self.output_ready.emit(data)
