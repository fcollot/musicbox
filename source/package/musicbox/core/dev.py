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
from musicbox import app
from musicbox.app.application import application_class, init_application_class

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, QThread, QTimer, Slot
else:
    from PySide6.QtCore import QObject, QThread, QTimer, Slot


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
    in order to run the GUI specific tests.

    """
    if not gui:
        modules = _find_test_modules(gui=False)
        run_module_tests(modules)
    
    if gui:
        if app.instance():
            modules = _find_test_modules(gui=True)
            run_module_tests(modules)
        else:
            class GUITestRunner(QObject):

                @Slot()
                def run(self):
                    run_tests(gui=True)

            init_application_class(gui=gui)
            application = application_class()()
            runner = GUITestRunner()
            timer = QTimer()
            thread = QThread()
            timer.setSingleShot(True)
            timer.timeout.connect(runner.run)
            timer.timeout.connect(thread.terminate)
            timer.timeout.connect(app.quit)
            thread.started.connect(timer.start)
            thread.start()
            application.run()

def run_module_tests(module_names):
    """Run the unit tests from a list of modules.

    """
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()

    for name in module_names:
        module = importlib.import_module(name)
        suite.addTests(loader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def _find_test_modules(gui):
    musicbox_root = musicbox.__path__[0]
    module_prefix = f'{"g" if gui else ""}test_'
    test_module_paths = list(Path(musicbox_root).glob(f'**/{module_prefix}*.py'))
    modules = []
    
    for module_path in test_module_paths:
        relative_path = module_path.relative_to(Path(musicbox_root).parent)
        module_file = relative_path.parts[-1]
        full_module_name = '.'.join(relative_path.parts)[:-3]
        if module_file.startswith(module_prefix):
            modules.append(full_module_name)

    return modules
