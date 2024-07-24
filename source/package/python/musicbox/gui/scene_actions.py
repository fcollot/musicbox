# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .file_actions import LoadFileAction


class LoadSceneAction(LoadFileAction):

    TITLE = "Open scene"

    def __init__(self, parent=None):
        super().__init__(self.title, parent, select_multiple=False, add_to_recent=True)

    def filters(self):
        filters = [f'{definition} ({", ".join(extensions)})' for reader in readers for definition, extensions in reader.file_filters().items()]
        return [""]

    def reader_for_filter(self, filter):
        

    @abstractmethod
    def reader(self):
        pass

    @Slot()
    def select_file(self):
        file_filters.append()
        options = self.options()
        if self._select_multipls:
        else:
            filename, _ = QFileDialog.getOpenFileName(self.parent(), self.name, "", ';;'.join(file_filters), options=options)
        if filename:
            pass

    def _handle_paths(self, paths):
        try:
            data = [self.reader().read(path) for path in paths]
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
