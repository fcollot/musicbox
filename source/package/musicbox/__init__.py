# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .core import dev


dev.add_loaded_module(__name__)


def init():
    pass


def test_modules():
    """List of modules containing test code.

    (used by musicbox.dev.run_tests)
    """

    import importlib

    subpackages = [
        'core',
        'data',
        'tui',
        'app',
    ]
    modules = []

    for subpackage in subpackages:
        package_module = importlib.import_module(f'musicbox.{subpackage}')
        modules += getattr(package_module, 'test_modules')()

    return modules
