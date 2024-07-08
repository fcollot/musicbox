# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from importlib.metadata import entry_points

from . import config


_plugins = {}


def find_plugins(group):
    group_plugins = _plugins.setdefault(group, {})
    for entry_point in entry_points(group=f'musicbox.{group}'):
        if entry_point.name in group_plugins:
            pass
        else:
            group_plugins[entry_point.name] = entry_point
    return plugin_names(group)


def plugin_names(group):
    return list(_plugins.setdefault(group, {}).keys())


def load_plugin(group, name=None):
    if name is None:
        name = config.plugins[group]
    if group not in _plugins:
        find_plugins(group)
    return _plugins[group][name].load()
