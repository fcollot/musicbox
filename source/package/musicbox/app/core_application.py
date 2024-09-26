# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
from threading import Lock, Thread

from musicbox import config, dev

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication
else:
    from PySide6.QtCore import QCoreApplication


dev.add_loaded_module(__name__)


class CoreApplication(QCoreApplication):

    _lock = Lock()

    def __init__(self, argv=None):
        super().__init__(argv=argv)
        self.setApplicationName("MusicBox")
        with self._lock:
            self._is_running = False

    def run(self):
        with self._lock:
            if self._is_running:
                raise RuntimeError("MusicBox is already running.")

        self._run_command_line()

        if config.pyside_version() == 2:
            return self._exec()
        else:
            return self.exec()

    def _run_command_line(self):
        def command_line():
            try:
                code.interact()
            except SystemExit:
                self.quit()

        thread = Thread(target=command_line, name="Python command line")
        thread.start()
