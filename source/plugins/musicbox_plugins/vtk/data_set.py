# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import vtk
from vtk.util import numpy_support


class DataSet():

    def __init__(self, vtk_data_set):
        self.natve_data = vtk_data_set

    def view_mode(self):
        if isinstance(self.native_data, vtkPolyData):
            return '3d mesh'
        else if isinstance(self.native_data, vtkImageData):
            return '2d slice'
        else:
            return None
