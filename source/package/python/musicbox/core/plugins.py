# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from importlib.metadata import entry_points
from threading import Lock, Thread

from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, Signal
else:
    from PySide6.QtCore import QObject, Signal


class PluginLoader(QObject):

    plugin_loaded = Signal(str, str)
    plugin_failed = Signal(str, str, Exception)

    def __init__(self, *, groups):
        super().__init__()
        
        def _collect_entry_points(group):
            return {entry_point.name: entry_point for entry_point in entry_points(group=f'musicbox.{group}')}

        self._plugins = {group: _collect_entry_points(group) for group in groups}

    def plugin_names(self, group=None):
        group = group or self._first_group()
        return list(self._plugins[group].keys())

    def num_plugins(self, group):
        group = group or self._plugins.keys[0]
        return len(self._plugins[group])

    def load(self, name_or_group, name=None):
        group = name_or_group if name is not None else self._first_group()
        try:
            plugin = self._plugins[group][name].load()
            self.plugin_loaded.emit(group, name)
            return plugin
        except Exception as e:
            self.plugin_failed.emit(group, name, e)
            raise

    def load_all(self, group=None):
        group = group or self._first_group()
        plugins = []
        errors = {}
        for name in self.plugin_names(group):
            try:
                plugins.append(self.load(group, name))
            except Exception as e:
                errors[name] = e
        return plugins, errors

    def _first_group(self):
        return list(self._plugins.keys())[0]


class PluginPreloader(QObject):

    progress_changed = Signal(float)
    finished = Signal()
    plugin_loaded = Signal(str, str)
    plugin_failed = Signal(str, str, Exception)

    @classmethod
    def run_in_dedicated_thread(cls, *args, **kwargs):
        preloader = cls()
        thread = Thread(target=preloader.run, args=args, kwargs=kwargs, name="Plugin preloader", daemon=True)
        thread.start()
        return preloader

    def __init__(self):
        super().__init__()
        self._lock = Lock()
        self._is_finished = False

    def run(self, plugin_specs, *args, **kwargs):
        groups = [x if isinstance(x, str) else x[0] for x in plugin_specs]
        plugin_loader = PluginLoader(groups=groups, *args, **kwargs)
        plugin_loader.plugin_loaded.connect(self.plugin_loaded)
        plugin_loader.plugin_failed.connect(self.plugin_failed)
        increment = 100 / len(plugin_specs)
        progress = 0
        self.progress_changed.emit(progress)
        self._errors = []

        for plugin_spec in plugin_specs:
            if isinstance(plugin_spec, str):
                group = plugin_spec
                names = plugin_loader.plugin_names(group)
            else:
                group, names = plugin_spec
            if names:
                subincrement = increment / len(names)
                for name in names:
                    try:
                        plugin_loader.load(group, name)
                    except Exception as e:
                        self._errors.append(e)
                    progress += subincrement
            else:
                progress += increment
            self.progress_changed.emit(progress)

        self.progress_changed.emit(100)
        self.finished.emit()
        with self._lock:
            self._is_finished = True

    def is_finished(self):
        with self._lock:
            return self._is_finished

    def errors(self):
        return self._errors
