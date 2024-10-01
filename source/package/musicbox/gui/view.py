# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util import numpy_support

from musicbox import config, dev
from . import proxy

if config.pyside_version() == 2:
    from PySide2.QtWidgets import QWidget, QVBoxLayout, Slot
else:
    from PySide6.QtWidgets import QWidget, QVBoxLayout, Slot


dev.add_loaded_module(__name__)


def init():
    gui_proxy = proxy.instance()
    gui_proxy.create_view.connect()


class ViewManager(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._views = []

    @Slot(parent)
    def create_view(self, parent=None):
        self._views.append(View(parent))


class View(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        #self.layout().setSpacing(0)
        #self.layout().setContentsMargins(2, 2, 2, 2)

        self.vtk_widget = QVTKRenderWindowInteractor()
        self.layout().addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()
        interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        interactor.Initialize()
        interactor.Start()

        self._data = []

    def add_mesh(self, mesh):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        mapper.SetScalarRange(cube.GetScalarRange())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
