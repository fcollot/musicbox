# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from threading import Lock, Thread

import pymedinria
from pymedinria.core import config, console

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication
else:
    from PySide6.QtCore import QCoreApplication


def instance():
    return QCoreApplication.instance()


def create(*args, gui=True, **kwargs):
    """Create the application.

    Set 'gui' to False for a non-GUI application.
    The remaining arguments are forwarded to the class constructor.

    """
    base_class = _select_base_class(gui)
    application_class = _create_application_class(base_class)
    return application_class(*args, **kwargs)


def _select_base_class(gui):
    if gui:
        if config.pyside_version() == 2:
            from PySide2.QtWidgets import QApplication
        else:
            from PySide6.QtWidgets import QApplication

        return QApplication
    else:
        return QCoreApplication


def _create_application_class(base_class):

    class Application(base_class):

        _lock = Lock()
        _is_running = False

        def __init__(self, argv=None):
            super().__init__(argv=argv)
            self.setApplicationName("pyMedInria")

        def run(self):
            exit_value = 1

            with self._lock:
                if self._is_running:
                    raise RuntimeError(f'{config.application_name()}is already running.')
                self._is_running = True

            console_locals = {'pymedinria' : pymedinria, 'mb' : pymedinria}

            with console.open(locals=console_locals, show_welcome=False, exit_function=self.quit):
                if base_class.__name__ == 'QApplication':
                    self._init_console_widget()
                else:
                    self._init_console_command_line()
                exit_value = self._run_qt()

            with self._lock:
                self._is_running = False

            return exit_value

        def _run_qt(self):
            if config.pyside_version() == 2:
                return self._exec()
            else:
                return self.exec()

        def _init_console_widget(self):
            from pymedinria.gui.console_widget import ConsoleWidget

            self._console_widget = ConsoleWidget()
            self._console_widget.show()
            self.aboutToQuit.connect(lambda : self._console_widget.update_output_streams(False))

        def _init_console_command_line(self):
            """Run the console command line on a separate thread.

            The command line cannot use the main thread as that one is occupied by
            the Qt event loop (which must be in the main thread).

            """
            def command_line():
                try:
                    console.instance().show_welcome()

                    while True:
                        line = input(console.instance().prompt())
                        console.instance().push(line)
                except Exception as e:
                    print(e)

            thread = Thread(target=command_line, name="Console command line", daemon=True)
            thread.start()

    return Application
