# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
from threading import Thread

import musicbox
from musicbox import config, dev, tui
from musicbox.core import Messenger

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication
else:
    from PySide6.QtCore import QCoreApplication


dev.add_loaded_module(__name__)


class CoreApplication(QCoreApplication):

    def __init__(self, argv=None):
        super().__init__(argv=argv)
        self.setApplicationName("MusicBox")
        self._is_running = False

    def run(self):
        if self._is_running:
            raise RuntimeError("MusicBox is already running.")
        self._init_messenger()
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
        messenger.user_info.connect(print)
        messenger.user_warning.connect(print)
        messenger.user_alert.connect(print)

    def _run_command_line(self):
        def command_line():
            try:
                code.interact(local=vars(tui))
            except SystemExit:
                self.quit()

        thread = Thread(target=command_line, name="Python command line")
        thread.start()
