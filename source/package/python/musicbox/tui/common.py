# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.data import DataManager, FileManager

#from .project import close_project, switch_project
#from .scene import close_scene, switch_scene


def read(path):
    return FileManager().read(path)


def write(path):
    return FileManager().write(path)


def switch(object):
    if isinstance(object, Scene):
        switch_scene(object)
    elif isinstance(object, Project):
        switch_project(object)
    else:
        raise TypeError(f'Unsupported type \'{object.__class__}\'')


def close(object):
    if isinstance(object, Scene):
        data_manager().close_scene(object)
    elif isinstance(object, Project):
        close_project(object)
    else:
        raise TypeError(f'Unsupported type \'{object.__class__}\'')
