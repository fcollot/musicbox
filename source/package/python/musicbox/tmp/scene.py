# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


class Scene():

    def __init__(self, entity=None):
        super().__init__()
        self._entity = entity
        self._parent = None
        self._children = []
        self._observers = {
            'added': [],
            'removed': [],
            'changed': [],
            'updated': []
        }

    def parent(self):
        return self._parent

    def set_parent(self, parent):
        if self._parent:
            del self._parent._children[self]
            self._parent.propagate_up(lambda node : node.notify_about('removed', self))
        self._parent = parent
        parent._children.append(self)
        parent.propagate_up(lambda node : node.notify_about('added', self))

    def entity(self):
        return self._scene_entity

    def set_entity(self, entity):
        self._scene_entity = entity
        self.propagate_up(lambda node : node.notify_about('changed', self))

    def update(self):
        self.propagate_down(lambda node : node.notify_about('updated', self))

    def add_node(self, node):
        node.set_parent(self)

    def remove_node(self, node):
        node.set_parent(None)

    def propagate_down(self, function):
        function(self)
        for child in self._children:
            child.propagate_down(function)

    def propagate_up(self, function):
        function(self)
        if self._parent is not None:
            propagate_upwards(self._parent, function)

    def add_observer(self, actions, observer):
        for action in actions:
            if observer not in self._observers[action]:
                self._observers[action].append(observer)

    def remove_observer(self, actions, observer):
        for action in actions:
            try:
                del self._observers[action][observer]
            except KeyError:
                pass

    def notify_about(self, action, node):
        for observer in self._observers[action]:
            observer(node)
