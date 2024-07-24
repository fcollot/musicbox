# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.data import Project


class ProjectGui():

    def __init__(self, project=Project()):
        super().__init__()
        self._project = project
        self.views = {}

        main_view = self.request_component('main_view')
        self.main_view = main_view
        main_view.setLayout(Gui.GridLayout())
        main_view.layout().setSpacing(0)
        main_view.layout().setContentsMargins(0, 0, 0, 0)

        self.setup_view('topleft', 0, 0)
        self.setup_view('topright', 0, 1)
        self.setup_view('bottomleft', 1, 0)
        self.setup_view('bottomright', 1, 1)

        #scene_editor = gui_group['scene_editor']
        #scene_editor.set_scene(self._scene)

    def scene_graph_view(self):
        return self._views['scene_graph']

    def scene_view(self):
        return self._views['scene']

    def setup_view(self, id, x, y):
        view = SceneView()
        self.views[id] = view
        self.main_view.layout().addWidget(view, x, y)
        view.add_scene(self.project.scene())
        event_handlers = {
            Gui.Event.MouseButtonPress: None,
            Gui.Event.MouseButtonRelease: None,
            Gui.Event.MouseButtonDblClick: lambda _ : self._switch_view_mode(id),
        }
        event_filter = EventFilter(view, event_handlers)
        view.install_viewer_event_filter(event_filter)

    def _switch_view_mode(self, view_id):
        for id, view in self.views.items():
            if id != view_id:
                view.setVisible(not view.isVisible())
        self.main_view.layout().activate()
