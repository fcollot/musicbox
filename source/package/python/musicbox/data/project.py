# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from pathlib import Path
import json

from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, QStandardPaths, Signal, Slot
else:
    from PySide6.QtCore import QObject, QStandardPaths, Signal, Slot

from musicbox.core import Settings


class Project():

    PROJECT_FILE_NAME = 'project.musicbox'

    @classmethod
    def project_locations(cls):
        try:
            locations = Settings().value('project_locations')
            if locations is None:
                locations = [Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)).joinpath('projects')].as_posix()
                set_project_locations(locations)
        finally:
            return locations

    @classmethod
    def set_project_locations(cls, locations):
        Settings().set_value('project_locations', [Path(location).as_posix() for location in locations])

    @classmethod
    def set_default_projects_directory(cls, root_dir, *, create=False):
        root_dir = Path(root_dir).reslove()
        if not root_dir.exists():
            if create:
                parent_dir = root_dir.parent
                if parent_dir != root_dir and not parent_dir.exists():
                    raise RuntimeError('The parent directory does not exist')
                else:
                    root_dir.mkdir()
            else:
                raise RuntimeError('Path does not exist. Set \'create\' to True to create it')
        cls._default_root_dir = root_dir

    @classmethod
    def create(cls, name, *, root_dir=None, accept_non_empty=False):
        if root_dir is None:
            if cls._default_root_dir is None:
                raise RuntimeError('The default root directory has not been set')
            root_dir = Path(cls._default_root_dir)
        else:
            root_dir = Path(root_dir).resolve()
            if not root_dir.exists():
                raise RuntimeError(f'The root directory does not exist')
            elif not root_dir.is_dir():
                raise RuntimeError(f'Not a directory: {root_dir}')

        if name != Path(name).name:
            raise RuntimeError(f'Not a proper project name: {name}')

        project_dir = root_dir.joinpath(name)

        if project_dir.exists():
            if not project_dir.is_dir():
                raise RuntimeError(f'Not a directory: {project_dir}')
            if any(project_dir.iterdir()) and not accept_non_empty:
                raise RuntimeError('The project directory is not empty. Set \'accept_non_empty\' to True to use it anyways.')
            elif Path(cls.PROJECT_FILE_NAME) in project_dir.iterdir():
                raise RuntimeError('The project directory already contains a project')
        else:
            project_dir.mkdir()

        project = cls(name, project_dir)
        ProjectWriter(project).write()
        return project

    @classmethod
    def read(cls, name):
        path = Path(name)
        if path.name == name:
            path = Path(cls._default_root_dir).joinpath(name)
        elif not path.is_absolute():
            raise RuntimeError('Relative paths are not supported')
        project_file_path = path.joinpath(cls.PROJECT_FILE_NAME)
        with open(project_file_path, 'r') as project_file:
            properties = json.load(project_file)
            return cls(name, path, _properties=properties)

    @classmethod
    def decode_contents(cls, contents):
        project = cls()
        for scene_encoding in contents['scenes']:
            scene = decode(scene_encoding)
            project.add_

    def __init__(self, name, path, *, _properties):
        self._path = Path(path).resolve()
        if not self._path.exists():
            raise RuntimeError(f'The project path does not exist: {self._path}')
        self._properties = {
            'name': name
        }

    def __eq__(self, other):
        return all((
            isinstance(other, Project),
            self.name() == other.name(),
            self.path() == other.path(),
        ))

    def __hash__(self):
        return hash((self.name(), self.path()))

    def name(self):
        return self._properties['name']

    def path(self):
        return self._path

    def project_file(self):
        return self._path.joinpath(self.PROJECT_FILE_NAME)

    def properties(self):
        return self._properties

    def write(self):
        with open(self.project_file(), 'w') as project_file:
            json.dump(self.project.properties(), project_file)


#encode.register_encodable_type(Project)
