# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.core import dev
from musicbox.data.image import create_sitk_image, create_vtk_image, pixels


dev.add_loaded_module(__name__)


def image(arg_1, *, type='sitk', data_type=None, spacing=None, origin=None, direction=None):
    if type == 'sitk':
        image = create_sitk_image(arg_1, data_type, spacing=spacing, origin=origin, direction=direction)
    elif type == 'vtk':
        image = create_vtk_image(arg_1, data_type, spacing=spacing, origin=origin, direction=direction)
    else:
        raise TypeError(f'Argument is not a valid image type: {type}')
    return image


voxels = pixels
