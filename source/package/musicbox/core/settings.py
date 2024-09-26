# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox import config
from . import dev


dev.add_loaded_module(__name__)


if config.pyside_version() == 2:
    from PySide2.QtCore import QSettings
else:
    from PySide6.QtCore import QSettings


class Settings():

    def __init__(self):
        self._settings = QSettings('liryc', 'musicbox')

    def value(self, name, default_value=None):
        return self._settings.value(name, default_value)

    def set_value(self, name, value):
        self._settings.setValue(name, value)
