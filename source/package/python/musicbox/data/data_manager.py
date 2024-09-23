# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, Signal, Slot
else:
    from PySide6.QtCore import QObject, Signal, Slot

from musicbox.core import Singleton

from .file_manager import FileManager


class DataManager(Singleton):

    data_opened = Signal(object)
    data_closed = Signal(object)
    current_data_changed = Signal(object)

    @classmethod
    def instance(cls):
        try:
            instance = cls._instance
        except AttributeError:
            instance = cls()
            cls._instance = instance
        return instance

    def __init__(self, parent=None):
        Singleton.__init__()

    def _singleton_init(self, first):
        self._data = first._data if first else []
        self._current = first._current if first else None

    def data(self):
        return self._data

    def open(self, data, *, make_current=True):
        if isinstance(data, str):
            data = self._file_manager.instance().read(data)
        if data in self._data:
            raise RuntimeError(f'Cannot open data of type \'{type(data)}\' twice')
        else:
            self._data.append(data)
        self.data_opened.emit(data)
        if make_current:
            self.set_current(data)
        return data

    def close(self, data):
        if data not in self._data:
            raise RuntimeError('The data is not open')
        self._data.remove(data)
        if data is self._current:
            other_data = self._data[0] if self._data else None
            self.set_current(other_data)
        self.data_closed.emit(data)

    def set_current(self, data):
        if data and data not in self._data:
            raise RuntimeError('Cannot switch to data that is not open')
        self._current = data
        self.current_data_changed.emit(data)

    def current(self):
        return self._current


#    def unique_scene_name(self):
#        project = self.project()
#        scene_names = project.scene_names() if project else [scene.name() for scene in self.opened_scenes()]
#        return utils.generate_unique_name('scene', existing_names=scene_names)
