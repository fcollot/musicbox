# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib
from pathlib import Path
import sys
from threading import Thread
import unittest

import musicbox
from musicbox.core import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication, QObject, QThread, QTimer, Slot
else:
    from PySide6.QtCore import QCoreApplication, QObject, QThread, QTimer, Slot


def reload_modules():
    """Reload all previously loaded MusicBox modules.

    """
    for name, module in sys.modules.copy().items():
        try:
            if name.startswith('musicbox.'):
                importlib.reload(module)
                print(f'Reloaded {name}.')
        except Exception as e:
            print(e)


def run_tests(*, gui=True):
    """Run the unit tests.

    The 'gui' option determines whether the GUI or non-GUI tests are run. This
    function may be called from the main thread of a running application or
    not; in the latter case a temporary QCoreApplication (or QApplication for
    GUI tests) will be created.

    """
    preexisting_app = QCoreApplication.instance()

    if not gui:
        if not preexisting_app:
            QCoreApplication()
    else:
        if preexisting_app:
            if QThread.currentThread() is not preexisting_app.thread():
                raise RuntimeError("The GUI tests must be run from the main thread.")
        else:
            _create_gui_application_and_run_tests()
            return

    try:
        modules = find_test_modules(gui=gui)
        if modules:
            run_module_tests(modules)
        else:
            raise RuntimeError("No tests found.")
    finally:
        if not preexisting_app:
            QCoreApplication.instance().shutdown()


def _create_gui_application_and_run_tests():

    class GUITestRunner(QObject):
        @Slot()
        def run(self):
            run_tests(gui=True)

    if config.pyside_version() == 2:
        from PySide2.QtWidgets import QApplication
    else:
        from PySide6.QtWidgets import QApplication

    app = QApplication()
    runner = GUITestRunner()
    timer = QTimer()
    thread = QThread()

    timer.setSingleShot(True)
    timer.timeout.connect(runner.run)
    timer.timeout.connect(thread.terminate)
    timer.timeout.connect(app.instance().quit)

    thread.started.connect(timer.start)
    thread.start()

    if config.pyside_version() == 2:
        return app._exec()
    else:
        return app.exec()


def run_module_tests(module_names):
    """Run the unit tests from a list of modules.

    If any of the modules contain GUI tests (which require a running
    QApplication), it is up to the caller to ensure the application was created
    beforehand and that this function is called from the main thread.

    """
    loader = unittest.defaultTestLoader
    runner = unittest.TextTestRunner(verbosity=2)

    for name in module_names:
        module = importlib.import_module(name)
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromModule(module))
        runner.run(suite)


def find_test_modules(gui):
    """Find the unit test modules using prefixes.

    The prefixes are:

        - '_test_' for non GUI tests (which may optionally need a running
          QCoreApplication to handle events).

        - '_gui_test_' for GUI tests (which require a running QApplication).

    """
    musicbox_root = musicbox.__path__[0]
    module_prefix = f'_{"gui_" if gui else ""}test_'
    test_module_paths = list(Path(musicbox_root).glob(f'**/{module_prefix}*.py'))
    modules = []
    
    for module_path in test_module_paths:
        relative_path = module_path.relative_to(Path(musicbox_root).parent)
        module_file = relative_path.parts[-1]
        full_module_name = '.'.join(relative_path.parts)[:-3]
        if module_file.startswith(module_prefix):
            modules.append(full_module_name)

    return modules
