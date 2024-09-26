# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config, data, tui
from .core import dev


dev.add_loaded_module(__name__)


def test_modules_list():
    return data.test_modules_list()
