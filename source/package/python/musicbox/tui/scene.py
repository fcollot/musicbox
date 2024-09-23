# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.data import Scene, SceneManager


def new_scene(name=None, *, subdir=None):
#    project = data_manager().project()
#    if name is None:
#        name = data_manager().unique_scene_name()
#    else:
#        if project:
#            if name in project.scene_names(subdir):
#                raise RuntimeError("A scene with this name already exists in the project")
#        elif subdir:
#            raise RuntimeError("Ther \'subdir\' option can only be used when creating project scenes")
    scene = Scene.create(name)
#    if project:
#        project.add_scene(scene, subdir)
    data_manager.open_scene(scene)
    return scene


def open_scene(name):
    path = Path(name)
    if path.name != name:
        name = path.name
        subdir = path.parents


def current_scene():
    return data_manager().current_scene()


def switch_scene(scene):
    data_manager().set_current_scene(scene)


def save_scene(scene=None):
    scene = scene or data_manager().current_scene()
    if scene:
        scene.save()
    else:
        raise RuntimeError('There is no scene to save')


def save_all_scenes():
    for scenes in data_manager().opened_scenes():
        scene.save()


def close_scene(scene=None):
    scene = scene or data_manager().current_scene()
    if scene:
        data_manager().close_scene(scene)
    else:
        raise RuntimeError('There is no scene to close')


def close_all_scenes():
    for scenes in data_manager().opened_scenes():
        data_manager().close_scene(scene)


def current_node():
    return data_manager().current_scene_node()


def add_data(data=None, name=None):
    node = SceneNode(name=name, contents=data)
    data_manager().current_scene_node().add_node(node)


def switch_data(data):
    data_manager().set_current_data(data)


def node_up():
    parent = node.parent()
