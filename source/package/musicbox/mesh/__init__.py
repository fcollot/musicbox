# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import numpy
import vtk
from vtk.util import numpy_support

from .primitive import box


def create(arg_1, *, vertices=None, lines=None, triangles=None, strips=None):
    """Create a VTK mesh.

    Args:
        arg_1:     An initializer argument that can be a vtkPolyData (in which
                   case no other arguments are needed), or an array containing
                   the point coordinates of the mesh (of type vtkDataArray or
                   numpy), or simply the number of points to create in the mesh.
        vertices:  An initializer defining the solitary vertices of the mesh.
                   This can be a vtkCellArray, a vtkDataArray, a numpy array
                   or the number of vertices to create. In the case of
                   vtkDataArray and numpy arrays, the array must contain the
                   successive x1, y1, z1, x2, y2, z2 etc. values of the points
                   when the array is flattened to one dimension. In the case of
                   a number, the created array will be filled with zeroes.
        lines:     An initializer defining the lines of the mesh.
                   This can be a vtkCellArray, a vtkDataArray, a numpy array
                   or the number of lines to create. In the case of vtkDataArray
                   and numpy arrays, the array must contain the successive
                   x1, y1, z1, x2, y2, z2 etc. values of the points when the
                   array is flattened to one dimension. In the case of a number,
                   the created array will be filled with zeroes.
        triangles: An initializer defining the triangles of the mesh.
                   This can be a vtkCellArray, a vtkDataArray, a numpy array
                   or the number of triangles to create. In the case of
                   vtkDataArray and numpy arrays, the array must contain the
                   successive x1, y1, z1, x2, y2, z2 etc. values of the points
                   when the array is flattened to one dimension. In the case of a
                   number, the created array will be filled with zeroes.

    Returns:
        A new instance of vtk.vtkPolyData.

    """
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
        if triangles:
            mesh.SetPolys(create_vtk_cell_array(triangles, cell_size=3))
        if strips:
            mesh.SetStrips(create_vtk_cell_array(strips, cell_size=3))
    return mesh


def _raise_no_other_argument_needed_error(arg_1):
    raise TypeError(f'No additional argument is accepted with {type(arg_1)} as an initializer.')


def create_vtk_cell_array(arg, *, cell_size=None):
    """Create a VTK cell array.

    Args:
        arg:       An initializer for the array that can be a vtkCellArray,
                   a vtkDataArray, a numpy array or the number of cells. The
                   cells correspond to the components of the vtkDataArray or the
                   second dimension of the numpy array (when using one of those
                   types).
        cell_size: When the first argument is a number, this argument must be
                   used to specify the cell size.

    Returns:
        A new instance of vtk.vtkCellArray.

    """
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
