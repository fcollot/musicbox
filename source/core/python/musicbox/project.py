# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config
from .gui_group import GuiGroup
from .scene import Scene
from .scene_view import SceneView

if config.pyside_version == 2:
    from PySide2.QtWidgets import QVBoxLayout
else:
    from PySide6.QtWidgets import QVBoxLayout


class Project():

    def __init__(self):
        self._scene = Scene()
        self._views = []

    def open(self):
        group_spec = {
            'scene_editor': 'scene_editor',
            'main_view': 'main_view'
        }
        gui_group = GuiGroup(group_spec)
        self.gui_group = gui_group
        
        main_view = gui_group['main_view']
        main_view.setLayout(QVBoxLayout())
        scene_view = SceneView(scene=self._scene)
        main_view.layout().addWidget(scene_view)
        main_view.show()

        #scene_editor = gui_group['scene_editor']
        #scene_editor.set_scene(self._scene)
