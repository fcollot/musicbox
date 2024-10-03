# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib
import inspect
from pathlib import Path
import sys
import unittest

import musicbox
from musicbox.core import config
from musicbox.app.application import application_class, init_application_class

if config.pyside_version() == 2:
    from PySide2.QtCore import QThread, QTimer
else:
    from PySide6.QtCore import QThread, QTimer


def reload_modules(modules_or_names=None):
    """Reload previously loaded modules.

    If 'modules_or_names' is None all previously loaded MusicBox modules are
    reloaded.

    This function is intended for development purposes and will likely cause
    issues.

    """
    if modules_or_names:
        module_names = [item.__name__ if inspect.ismodule(item) else item for item in modules_or_names]
        modules = {name : sys.modules[name] for name in module_names}
    else:
        modules = {name : module for module in sys.modules.copy().items() if name.startswith('musicbox.')}
    
    for name, module in modules.items():
        try:
            importlib.reload(module)
            print(f'Reloaded {name}.')
        except Exception as e:
            print(e)


def run_tests(*, gui=True):
    """Run the unit tests.

    If the 'gui' option is True, an instance of the application will be created
    in order to run the GUI specific tests.

    """
    non_gui_modules, gui_modules = _find_test_modules()
    run_module_tests(non_gui_modules)

    if gui:
        init_application_class(gui=True)
        app = application_class()()
        timer = QTimer()
        thread = QThread()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda : run_module_tests(gui_modules))
        timer.timeout.connect(thread.terminate)
        timer.timeout.connect(app.quit)
        thread.started.connect(timer.start)
        thread.start()
        app.run()


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


def _find_test_modules():
    musicbox_root = musicbox.__path__[0]
    test_module_paths = list(Path(musicbox_root).glob('**/test_*.py'))
    gui_modules = []
    non_gui_modules = []
    
    for module_path in test_module_paths:
        relative_path = module_path.relative_to(Path(musicbox_root).parent)
        module_name = '.'.join(relative_path.parts)[:-3]
        if module_name.startswith('musicbox.gui'):
            gui_modules.append(module_name)
        else:
            non_gui_modules.append(module_name)

    return non_gui_modules, gui_modules
