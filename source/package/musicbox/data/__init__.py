# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.core import dev
from . import image, mesh


dev.add_loaded_module(__name__)


def test_modules():
    modules = [
        'test_image',
        'test_mesh',
    ]
    return [f'{__name__}.{module}' for module in modules]
