# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


def init():
    from SimpleITK import ReadImage, WriteImage
    from .file_manager import FileManager
    FileManager().add_reader(ReadImage)
    FileManager().add_writer(WriteImage)
