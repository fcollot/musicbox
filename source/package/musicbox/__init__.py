# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config
from .core import dev


dev.add_loaded_module(__name__)


def test_modules_list():
    """List of modules containing test code.

    (used by musicbox.dev.run_tests)
    """
    return []
