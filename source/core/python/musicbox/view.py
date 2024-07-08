# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config, plugins
from .scene import Scene

if config.pyside_version == 2:
    from PySide2.QtCore import Slot
    from PySide2.QtWidgets import QWidget
else:
    from PySide6.QtCore import Slot
    from PySide6.QtWidgets import QWidget


class View(QWidget):

    def __init__(self, parent=None, *, viewer_type, viewer_plugin=None):
        super().__init__(parent)
        self.scenes = []
        self.handles = {}
        self.viewer = plugins.load_plugin(viewer_type, viewer_plugin)()

    @Slot(Scene)
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
            self.viewer.remove_entity(handle)

    def _update_node(self, node):
        try:
            handle = self.handles[node]
        except KeyError:
            pass
        else:
            self.viewer.update_entity(handle)


class SliceView(View):

    def __init__(self, parent=None, *, viewer_plugin=None):
        super().__init__(parent, viewer_type='slice_viewer', viewer_plugin=viewer_plugin)
