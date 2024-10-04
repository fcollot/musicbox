# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from abc import ABC, abstractmethod
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from musicbox.core import config

if config.pyside_version() == 2:
    from PySide2.QtWidgets import QWidget
else:
    from PySide6.QtWidgets import QWidget


_manager = None


def manager():
    global _manager
    if not _manager:
        _manager = _ViewManager()
    return _manager


class _ViewManager():

    def __init__(self):
        self._props = {}
        self._views = []

    def find_or_create_prop(self, arg, view_mode):
        prop = self._props.get(arg)

        if prop:
            return prop
        else:
            if isinstance(arg, vtk.vtkDataSet):
                if isinstance(arg, vtk.vtkPolyData):
                    mapper = vtk.vtkPolyDataMapper()
                    mapper.SetInputData(arg)
                    prop = vtk.vtkActor()
                    prop.SetMapper(mapper)

        if not prop:
            raise TypeError(f'Cannot create prop from {type(arg)}')

        self._props[arg] = prop
        return prop

    def create_view(self, mode):
        if mode == '2D':
            view = _View2D()
        elif mode == '3D':
            view = _View3D()
        else:
            raise KeyError(f'{mode} is not a valid view mode')
        self._views.append(view)
        return view


class _View(QVTKRenderWindowInteractor):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.renderer = vtk.vtkRenderer()
        self.renderer.ResetCamera()
        self.GetRenderWindow().AddRenderer(self.renderer)
        self.GetRenderWindow().Render()

        self.interactor = self.GetRenderWindow().GetInteractor()
        self.interactor.Initialize()
        self.interactor.Start()


class _View3D(_View):

    def add_data(self, data):
        prop = manager().find_or_create_prop(prop, '3D')
        self.renderer.add_prop(prop)
            
