# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import builtins
import importlib
import inspect
from pathlib import Path
import os
import sys
from threading import Thread, RLock
import time
import unittest

import musicbox
from musicbox.core import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication, QObject, QThread, QTimer, Slot
else:
    from PySide6.QtCore import QCoreApplication, QObject, QThread, QTimer, Slot


_reload_activated = False
_reload_setting_lock = RLock()
_import_times = {}


def set_auto_reload(enable):
    with _reload_setting_lock:
        global _reload_activated

        if enable:
            global _builtins_import
            global _import_times

            if '_builtins_import' not in globals():
                _builtins_import = builtins.__import__

            builtins.__import__ = _import_and_track_time

            _reload_activated = True
            current_time = time.time()
            for name, module in sys.modules.items():
                if name.startswith('musicbox') and name not in _import_times:
                    _import_times[name] = current_time
            _run_module_reload_loop()
        else:
            if '_builtins_import' in globals():
                builtins.__import__ = _builtins_import
            _reload_activated = False


def auto_reload():
    return _reload_activated


def _import_and_track_time(name, globals=None, locals=None, fromlist=(), level=0):
    module = _builtins_import(name, globals=globals, locals=locals, fromlist=fromlist, level=level)
    if level > 0:
        name_parts = globals['__package__'].split('.')
        if level > 1:
            name_parts = name_parts[:1 - level]
    else:
        name_parts = []
    name_parts += name.split('.')
    if name_parts[0] == 'musicbox':
        global _import_times
        current_time = time.time()
        for i in range(len(name_parts)):
            _import_times['.'.join(name_parts[:i + 1])] = current_time
        if fromlist:
            full_name = '.'.join(name_parts)
            for item in fromlist:
                if inspect.ismodule(getattr(module, item)):
                    _import_times[f'{full_name}.{item}'] = current_time
    return module


def _run_module_reload_loop():
    def module_reload_loop():
        while True:
            with _reload_setting_lock:
                if _reload_activated:
                    for name in _import_times:
                        module = sys.modules[name]
                        if os.path.getmtime(module.__file__) > _import_times[name]:
                            print(f'Reloading {name}')
                            module = importlib.reload(sys.modules[name])
                            _import_times[name] = time.time()
                    time.sleep(2)
                else:
                    break

    thread = Thread(target=module_reload_loop, name="Module reload thread", daemon=True)
    thread.start() 


def run_tests(*, gui=True):
    """Run the unit tests.

    If the 'gui' option is True, an instance of the application will be created
    in order to run the GUI tests. This function may be called from the main
    thread of a running QApplication or not; in the latter case a temporary
    application will be created for GUI tests.

    """
    app = QCoreApplication.instance()
    preexisting_app = True if app else False

    if not gui:
        if not app:
            app = QCoreApplication()
        modules = find_test_modules(gui=False)
        run_module_tests(modules)
    else:
        if app:
            if QThread.currentThread() is not app.thread():
                raise RuntimeError("The GUI tests must be run from the main thread.")
            modules = find_test_modules(gui=True)
            run_module_tests(modules)
        else:
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
            timer.timeout.connect(app.quit)
            thread.started.connect(timer.start)
            thread.start()
            if config.pyside_version() == 2:
                return app._exec()
            else:
                return app.exec()

    if not preexisting_app:
        app.shutdown()


def run_module_tests(module_names):
    """Run the unit tests from a set of modules.

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
    """Find the MusicBox unit test modules using prefixes.

    The prefixes are:
        - '_test_' for non GUI tests.
        - '_gtest_' for GUI tests (which require a running QApplication).

    """
    musicbox_root = musicbox.__path__[0]
    module_prefix = f'_{"g" if gui else ""}test_'
    test_module_paths = list(Path(musicbox_root).glob(f'**/{module_prefix}*.py'))
    modules = []
    
    for module_path in test_module_paths:
        relative_path = module_path.relative_to(Path(musicbox_root).parent)
        module_file = relative_path.parts[-1]
        full_module_name = '.'.join(relative_path.parts)[:-3]
        if module_file.startswith(module_prefix):
            modules.append(full_module_name)

    return modules
