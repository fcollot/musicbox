# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
import sys
from threading import Thread

from . import config

if config.pyside_version() == 2:
    from PySide2.QtWidgets import QApplication
else:
    from PySide6.QtWidgets import QApplication, QWidget

import musicbox
from musicbox.core import Messenger, PluginPreloader


class Application(QApplication):

    preloaded_plugins = [
        'data_readers',
        'data_writers',
    ]

    def __init__(self, argv=None):
        super().__init__(argv=argv)
        self.setApplicationName("MusicBox")
        self.setQuitOnLastWindowClosed(False)
        self._is_running = False

    def run(self):
        if self._is_running:
            raise RuntimeError("MusicBox is already running.")
        self._init_messenger()
        plugin_preloader = self._preload_plugins_in_background_thread()
       # sys.modules['__main__'].__dict__['mbox'] = musicbox#{symbol: getattr(musicbox_api, symbol) for symbol in dir(musicbox_api) if not symbol.startswith('_')}
        self._run_command_line()

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

    def _preload_plugins_in_background_thread(self):
        preloader = PluginPreloader.run_in_dedicated_thread(self.preloaded_plugins)
        return preloader

    def _run_command_line(self):
        def command_line():
            try:
                code.interact(local=vars(musicbox))
            except SystemExit:
                self.quit()

        thread = Thread(target=command_line, name="Python command line")
        thread.start()
