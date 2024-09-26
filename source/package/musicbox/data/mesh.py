# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import vtk
from vtk.util import numpy_support

from musicbox.core import dev


dev.add_loaded_module(__name__)


def create_vtk_mesh(arg_1, *, vertices=None, lines=None, polygons=None, strips=None):
    mesh = vtk.vtkPolyData()

    if isinstance(arg_1, vtk.vtkPolyData):
        if vertices or lines or polygons or strips:
            _raise_no_other_argument_needed_error(arg_1)
    else:
        mesh.SetPoints(vtk.vtkPoints())

        if isinstance(arg_1, vtk.vtkDataArray):
            mesh.GetPoints().DeepCopy(arg_1)
        elif isinstance(arg_1, numpy.ndarray):
            point_array = numpy_support.numpy_to_vtk(num_array=arg_1.reshape(-1), deep=True)
            mesh.GetPoints().SetData(point_array)
        else:
            mesh.GetPoints().SetNumberOfPoints(arg_1)

        if vertices:
            mesh.SetVertices(create_vtk_cell_array(vertices, cell_size=1))
        if lines:
            mesh.SetLines(create_vtk_cell_array(lines, cell_size=2))
        if polygons:
            mesh.SetPolys(create_vtk_cell_array(polygons, cell_size=1))
        if strips:
            mesh.SetStrips(create_vtk_cell_array(strips, cell_size=3))
    return mesh


def _raise_no_other_argument_needed_error(arg_1):
    raise TypeError(f'No additional argument is accepted with {type(arg_1)} as an initializer.')


def create_vtk_cell_array(arg, *, cell_size=None):
    cell_array = vtk.vtkCellArray()

    if isinstance(arg, vtk.vtkCellArray):
        cell_array.DeepCopy(arg)
    else:
        if isinstance(arg, vtk.vtkDataArray):
            connectivity = vtk.vtkDataArray()
            connectivity.DeepCopy(arg)
            connectivity.SetNumberOfComponents(1)
            cell_array.SetData(arg.GetNumberOfComponents(), connectivity)
        elif isinstance(arg, numpy.ndarray):
            connectivity = numpy_support.numpy_to_vtk(num_array=arg.reshape(-1), deep=True)
            cell_array.SetData(arg.shape[1], connectivity)
        else:
            cell_array.ResizeExact(arg, arg * cell_size)

    return cell_array
