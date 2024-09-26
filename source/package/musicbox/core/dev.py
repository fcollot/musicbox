# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from threading import RLock


_loaded_modules = []
_lock = RLock()


def add_loaded_module(name):
    with _lock:
        _loaded_modules.append(name)


add_loaded_module(__name__)


def reload_modules():
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
