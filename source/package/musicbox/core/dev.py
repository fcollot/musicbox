# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from threading import RLock


_loaded_modules = []
_lock = RLock()


def add_loaded_module(name):
    """Declare a loaded module.

    Must be called from every module in the application, right after the imports.
    (use the __name__ variable as the parameter)
    This allows the module to be reloaded through the reload_modules() call.
    """
    with _lock:
        _loaded_modules.append(name)


add_loaded_module(__name__)


def reload_modules():
    """Reload all previously loaded modules.

    For this to work, add_loaded_module must be used properly.
    (see the function for more details)
    """
    import importlib
    import sys

    with _lock:
        for module in _loaded_modules:
            importlib.reload(sys.modules[module])


def run_tests():
    import unittest
    import musicbox

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    
    for module in musicbox.test_modules_list():
        module = importlib.import_module(module)
        suite.addTests(loader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner()
    runner.run(suite)
