# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.core import dev
from .application import application_class, init_application_class


def instance():
    """The current Qt application instance.

    """
    return application_class().instance()


def run(*, gui=True):
    """Run MusicBox.

    Use the 'gui' option to run in GUI or console-only mode.

    """
    init_application_class(gui=gui)
    app = instance()

    if app is None:
        app = application_class()()
    else:
        raise RuntimeError("Cannot run MusicBox because another Qt application is already running.")

    return app.run()


def quit():
    application_class().instance().quit()


def main():
    """Application entry point when running from the command line.

    Do not call this function from Python code. Use 'run()' instead.

    """
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()
    parser.add_argument('--gui', action=BooleanOptionalAction, default=True)
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    if args.test:
        dev.run_tests(gui=args.gui)
    else:
        run(gui=args.gui)
