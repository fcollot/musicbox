# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys

from . import config
from .application import Application


def run(**options):
    app = Application.instance()
    if app is None:
        app = Application(sys.argv)
    else:
        if not isinstance(app, Application):
            raise RuntimeError("Cannot run MusicBox because another Qt application is already running.")

    return app.run(**options)
