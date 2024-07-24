# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import vtk

import numpy
import vtk
from vtk.util import numpy_support


class Mesh(abc.ABC):

    def __init__(self):
        super.__init__()

    @abc.abstractmethod
    def cell_size(self):
        return

    @abc.abstractmethod
    def num_cells(self):
        return

    def as_numpy(self):
        view = None
        try:
            view  = self._numpy_view
        except AttributeError:
            view = self._create_numpy_view()
            self._numpy_view = view
        return view

    def as_vtk(self):
        view = None
        try:
            view  = self._vtk_view
        except AttributeError:
            view = self._create_vtk_view()
            self._vtk_view = view
        return view

    @abc.abstractmethod
    def _create_numpy_view(self):
        return

    @abc.abstractmethod
    def _create_vtk_view(self):
        return


class NumpyMesh(Mesh):

    def __init__(self, point_array, cell_array, deep_copy=True):
        super().__init__()
        if deep_copy:
            point_array = point_array.copy()
            cell_array = cell_array.copy()
        self._points = point_array
        self._cells = cell_array

    def cell_size(self):
        return self._cells.shape[1]

    def num_cells(self):
        return self._cells.shape[0]

    def as_numpy(self):
        return self

    def _create_vtk_view(self):
        view = VTKMesh.from_numpy(self._points, self._cells, deep_copy=False)
        view._numpy_view = self
        return view


class VTKMesh(Mesh, vtk.PolyData):
    
    def __init__(self, point_array, cell_array, deep_copy=True):
        super().__init__()
        vtk_point_array = numpy_support.numpy_to_vtk(num_array=point_array.ravel(), deep=deep_copy)
        vtk_cell_array = numpy_support.numpy_to_vtk(num_array=cell_array.ravel(), deep=deep_copy)
        self.GetPoints().SetData(vtk_points)
        cell_size = cell_array.shape[1]
        self._cell_size = cell_size
        if cell_size >= 3:
            self.SetPolys(vtk_cells)
        elif cell_size == 2:
            self.SetLines(vtk_cells)
        else:
            self.SetVerts(vtk_cells)

    def cell_size(self):
        return self._cell_size

    def num_cells(self):
        if self.cell_size() >= 3:
            num_cells = self.GetNumberOfPolys()
        elif self.cell_size() == 2:
            num_cells = self.GetNumberOfLines()
        else:
            num_cells = self.GetNumberOfVerts()
        return num_cells

    def as_vtk(self):
        return self

    def _create_numpy_view(self):
        point_array = numpy_support.vtk_to_numpy(self.GetPoints().GetData())
        point_array.shape = self.dimensions()
        cell_array = numpy_support.vtk_to_numpy(self.GetPoints().GetData())
        cell_array.shape = (self.num_cells(), self.cell_size())
        view = NumpyMesh.(point_array, cell_array, deep_copy=False)
        view._vtk_view = self
        return view


_type2class = {
    'numpy': NumpyMesh,
    'vtk': VTKMesh,
}


def mesh(arg_1, arg_2=None, *, type='numpy'):
    np_array = None
    if isinstance(arg_1, Mesh):
        np_array = arg_1.as_numpy()
    elif isinstance(arg_1, numpy.ndarray):
        np_array = arg_1
    if np_array is None:
        np_array = numpy.zeros(arg_1, dtype=data_type)
    try:
        mesh_class = _type2class[type]
    except KeyError:
        raise ValueError(f'Unknown mesh type \'{type}\'')
    else:
        new_mesh = mesh_class(point_array, cell_array)
    return new_mesh
