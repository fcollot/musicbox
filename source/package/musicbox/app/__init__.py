# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys

from musicbox import dev

from .application import init_application_class


dev.add_loaded_module(__name__)


def run(*, gui=False):
    application_class = init_application_class(gui=gui)
    app = application_class.instance()

    if app is None:
        app = application_class()
    else:
        if not isinstance(app, application_class):
            raise RuntimeError("Cannot run MusicBox because another Qt application is already running.")

    return app.run()


def test_modules():
    return []
