# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


current = {}


def current_project():
    return current.get('project', None)
