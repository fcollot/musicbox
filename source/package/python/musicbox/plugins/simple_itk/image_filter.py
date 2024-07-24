# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import SimpleITK as sitk


class ImageFilterWidget(musicbox.ImageFilterWidget):

    def __init__(self):
        self.filters = [x for x in [getattr(sitk, x) for x in dir(sitk)]  if isinstance(x, type) and issubclass(x, sitk.ImageFilter)]
