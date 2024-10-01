# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
import sys
from threading import Lock, Thread

from musicbox import config, dev, init, tui


dev.add_loaded_module(__name__)


_application_class = None


def init_application_class(*, gui=True):
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
            with self._lock:
                if self._is_running:
                    raise RuntimeError("MusicBox is already running.")
                self._is_running = True

            if self._gui:
                self._init_console()
            else:
                self._run_command_line()

            if config.pyside_version() == 2:
                return self._exec()
            else:
                return self.exec()

        def _init_console(self):
            if not self._gui:
                raise RuntimeError("Cannot create a console because the current MusicBox application was configured without a GUI")
            from musicbox.gui.console import GUIConsole
            console = GUIConsole()
            self._console = console
            console.run()
            console.show()
            sys.stdin = console

        def _run_command_line(self):
            """Run the Python command line on a separate thread.

            The command line cannot use the main thread as that one is occupied by
            the Qt event loop (which must be in the main thread).
            """
            def command_line():
                from musicbox.core.console import Console

                try:
                    console = Console()
                    while True:
                        line = input(console.prompt())
                        console.push(line)
                except EOFError:
                    print('\n')
                except Exception as e:
                    print(e)
                finally:
                    self.quit()

            thread = Thread(target=command_line, name="Python command line")
            thread.start()

    return Application
