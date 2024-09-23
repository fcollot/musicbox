# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.data import Project


def project_locations():
    return Project.project_locations()


def set_project_locations(locations):
    Project.set_project_locations(locations)


def _find_by_name(name):
    selected_projects = []
    for existing_project in projects():
        if existing_project.name == project:
            selected_projects.append(existing_project)
    if not selected_projects:
        raise RuntimeError(f'There is no opened project named \'{project}\'.')
    elif len(selected_project) > 1:
        raise RuntimeError(f'There are multiple opened projects named \'{project}\'. Invoke with the project object directly (call projects(\'project\') for a list of candidates).')
    else:
        return selected_projects[0]


def projects(name=None):
    result = _manager().projects()
    if name:
        result = filter(lambda project : project.name() == name, result)
    return tuple(result)


def new_project(*args, **kwargs):
    project = Project.create(*args, **kwargs)
    _manager().open(project)
    return project


def open_project(name):
    return _manager().open(name)


def close_project(project=None):
    if project and isinstance(project, str):
        project = _find_by_name(project)
    _manager().close(project or _manager().current())


def current_project():
    return _manager().current()


def switch_project(project):
    if isinstance(project, str):
        project = _find_by_name(project)
    _manager().set_current(project)
