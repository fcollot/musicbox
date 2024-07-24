# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
import traceback

from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Slot
    from PySide2.QtWidgets import QApplication
else:
    from PySide6.QtCore import Slot
    from PySide6.QtWidgets import QApplication

from musicbox import api as musicbox_api
from musicbox.core import Messenger, PluginPreloader

from .main_window import MainWindow


class Application(QApplication):

    preloaded_plugins = [
        'data_readers',
        'data_writers',
    ]

    def __init__(self, argv=None):
        super().__init__(argv=argv)
        self.setApplicationName("MusicBox")
        self._is_running = False

    def run(self, *, splash=False):
        if self._is_running:
            raise RuntimeError("MusicBox is already running.")
        self._init_messenger()
        splash = self._create_splash() if splash else None
        plugin_preloader = self._preload_plugins_in_background_thread()
        self._init_main_window()
        self._main_window.set_plugin_preloader(plugin_preloader)
        sys.modules['__main__'].__dict__['mbox'] = musicbox_api#{symbol: getattr(musicbox_api, symbol) for symbol in dir(musicbox_api) if not symbol.startswith('_')}

        if splash is not None:
            splash.finish(self._main_window)

        if config.pyside_version() == 2:
            return self._exec()
        else:
            return self.exec()

    def _init_messenger(self):
        messenger = Messenger()
        self._messenger = messenger
        messenger.internal_info.connect(print)
        messenger.internal_warning.connect(print)
        messenger.internal_alert.connect(print)

    def _create_splash(self):
        if config.pyside_version() == 2:
            from PySide2.QtCore import Signal, Qt
            from Pyside2.QtGui import QPixmap
            from PySide2.QtWidgets import QLabel, QSplashScreen, QVBoxLayout
        else:
            from PySide6.QtCore import Signal, Qt
            from PySide6.QtGui import QPixmap
            from PySide6.QtWidgets import QLabel, QSplashScreen, QVBoxLayout

        pixmap = QPixmap('/Users/florent.collot/Downloads/logo.png')
        splash = QSplashScreen(pixmap)
        splash.setLayout(QVBoxLayout())
        splash.layout().addWidget(QLabel("v1.0"), 0, Qt.AlignTop | Qt.AlignRight)
        splash.showMessage("Loading...", Qt.AlignBottom | Qt.AlignRight)
        splash.show()
        self.processEvents()
        return splash

    def _preload_plugins_in_background_thread(self):
        preloader = PluginPreloader.run_in_dedicated_thread(self.preloaded_plugins)
        preloader.plugin_loaded.connect(self._plugin_loaded)
        preloader.plugin_failed.connect(self._plugin_failed)
        return preloader

    @Slot(str, str)
    def _plugin_loaded(self, group, name):
        self._messenger.internal_info(f'Loaded plugin \'{group}:{name}\'')

    @Slot(str, str, Exception)
    def _plugin_failed(self, group, name, exception):
        self._messenger.alert_internal(f'Error while loading plugin \'{group}:{name}\'')
        self._messenger.alert_internal(''.join(traceback.format_exception(exception)))

    def _init_main_window(self):
        self._main_window = MainWindow(messenger=self._messenger)
        self._main_window.showMaximized()
        self._main_window.show_welcome_page()
