# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, Slot
else:
    from PySide6.QtCore import QObject, Slot


class GUIProxy(QObject):

    view_image = Signal(sitk.Image)
    view_mesh = Signal(vtk.vtkPolyData)
    view_scene = Signal(Scene)


class GUIManager(Singleton):

    def _singleton_init(self, first):
        self._proxy = first._proxy if first else GUIProxy()

    def proxy(self):
        return self._proxy

    def view(self, data):
        if isinstance(data, sitk.Image):
            self.view_image.emit(data)
        elif isinstance(data, vtk.vtkPolyData):
            self.view_mesh.emit(data)
        elif isinstance(data, Scene):
            self.view_scene.emit(data)
        elif isinstance(data, str):
            self.view(read(data))
        else:
            scene = Scene()
            for item in data:
                scene.add_data(data)
            self.view(scene)
