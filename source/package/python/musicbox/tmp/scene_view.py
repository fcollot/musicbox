# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from ..scene import Scene
from . import Gui, Viewer


class SceneView(Gui.Widget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scenes = []
        self.handles = {}
        self.viewer = Viewer()
        self.setLayout(Gui.VBoxLayout())
        self.layout().addWidget(self.viewer)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def install_viewer_event_filter(self, event_filter):
        self.viewer.viewer_backend().installEventFilter(event_filter)

    @Gui.Slot(Scene)
    def add_scene(self, scene):
        if scene not in self.scenes:
            self.scenes.append(scene)
            scene.propagate_down(self._add_node)
            scene.add_observer(['added', 'changed'], self._add_node)
            scene.add_observer(['removed'], self._remove_node)
            scene.add_observer(['updated'], self._update_node)
        else:
            pass

    def _add_node(self, node):
        if node in self.handles:
            del self.handles[node]
        entity = node.entity()
        if entity is not None:
            handle = self.viewer.add_data_set(entity)
            self.handles[node] = handle

    def _remove_node(self, scene, node):
        try:
            handle = self.handles[scene].pop(node)
        except KeyError:
            pass
        else:
            self.viewer.remove_data_set(handle)

    def _update_node(self, node):
        try:
            handle = self.handles[node]
        except KeyError:
            pass
        else:
            self.viewer.update_data_set(handle)
