# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from numpy import (
    int8,
    int16,
    int32,
    int64,
    uint8,
    uint16,
    uint32,
    uint64,
    float32,
    float64,
)

from musicbox.core import dev
from .image import image, pixels, voxels


dev.add_loaded_module(__name__)


def test_modules():
    return []
