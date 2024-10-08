# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from threading import Lock, Thread

import musicbox
from musicbox.core import config


_application_class = None


def init_application_class(*, gui=True):
    """Initialize the application class.

    Specify 'gui=False' for a console-only application.

    """
    if gui:
        if config.pyside_version() == 2:
            from PySide2.QtWidgets import QApplication
        else:
            from PySide6.QtWidgets import QApplication

        base_class = QApplication
    else:
        if config.pyside_version() == 2:
            from PySide2.QtCore import QCoreApplication
        else:
            from PySide6.QtCore import QCoreApplication

        base_class = QCoreApplication

    global _application_class
    _application_class = _create_application_class(base_class, gui)
    return _application_class


def application_class():
    """The application class.

    If the class has not been initialized yet (using init_application_class),
    a default one will be initialized.

    """
    if not _application_class:
        return init_application_class()
    else:
        return _application_class


def _create_application_class(base_class, gui):

    class Application(base_class):

        _lock = Lock()
        _is_running = False
        _gui = gui

        def __init__(self, argv=None):
            super().__init__(argv=argv)
            self.setApplicationName("MusicBox")

        def run(self):
            exit_value = 1

            with self._lock:
                if self._is_running:
                    raise RuntimeError("MusicBox is already running.")
                self._is_running = True

            self._run_console()

            exit_value = self._run_qt()

            with self._lock:
                self._is_running = False

            return exit_value

        def _run_qt(self):
            if config.pyside_version() == 2:
                return self._exec()
            else:
                return self.exec()

        def _run_console(self):
            if self._gui:
                from musicbox.gui.console_widget import ConsoleWidget as Console
            else:
                from musicbox.core.console import Console

            globals = {'musicbox' : musicbox, 'mb' : musicbox}
            console = Console(globals=globals)
            console.run_ended.connect(self.quit)
            console.run()

            if self._gui:
                console.show()

        def console_widget(self):
            return self._console_widget

    return Application
