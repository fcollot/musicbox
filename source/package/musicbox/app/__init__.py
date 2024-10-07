# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.core import config, dev
from .application import application_class, init_application_class

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication
else:
    from PySide6.QtCore import QCoreApplication


def instance():
    """The current Qt application instance.

    """
    return QCoreApplication.instance()


def run(*, gui=True):
    """Run MusicBox.

    Use the 'gui' option to run in GUI or console-only mode.

    """
    app = instance()

    if app is None:
        init_application_class(gui=gui)
        app = application_class()()
    else:
        raise RuntimeError("Cannot run MusicBox because another Qt application is already running.")

    return app.run()


def quit():
    instance().quit()


def main():
    """Application entry point when running from the command line.

    Do not call this function from Python code. Use 'run()' instead.

    """
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()
    parser.add_argument('--gui', action=BooleanOptionalAction, default=True)
    parser.add_argument('--test', choices=['no-gui', 'gui', 'all'])
    parser.add_argument('--dev', action='store_true')
    args = parser.parse_args()

    if args.test:
        if args.test == 'no-gui' or args.test == 'all':
            dev.run_tests(gui=False)
        if args.test == 'gui' or args.test == 'all':
            dev.run_tests(gui=True)
    else:
        if args.dev:
            dev.set_auto_reload(True)
        run(gui=args.gui)
