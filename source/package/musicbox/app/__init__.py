# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys

from musicbox import dev

from .core_application import CoreApplication


dev.add_loaded_module(__name__)


def run(*, gui=False):
    if gui:
        raise NotImplementedError("The GUI is not yet implemented.")
    else:
        application_class = CoreApplication

    app = application_class.instance()

    if app is None:
        app = application_class()
    else:
        if not isinstance(app, CoreApplication):
            raise RuntimeError("Cannot run MusicBox because another Qt application is already running.")

    return app.run()
