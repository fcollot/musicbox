# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import vtk


def box(size=(1, 1, 1)):
    return vtk.vtkCubeSource()
