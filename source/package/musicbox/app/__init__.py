# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.core import dev
from .application import create, instance


def run(*, gui=True):
    """Run MusicBox.

    Use the 'gui' option to run in GUI or console-only mode.

    """
    app = instance()

    if app is None:
        app = create(gui=gui)
    else:
        raise RuntimeError("Cannot run MusicBox because another Qt application is already running.")

    return app.run()


def main():
    """Application entry point when running from the command line.

    Do not call this function from Python code. Use 'run()' instead.

    """
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()
    parser.add_argument('--gui', action=BooleanOptionalAction, default=True)
    parser.add_argument('--test', choices=['no-gui', 'gui', 'all'])
    args = parser.parse_args()

    if args.test:
        if args.test == 'no-gui' or args.test == 'all':
            dev.run_tests(gui=False)
        if args.test == 'gui' or args.test == 'all':
            dev.run_tests(gui=True)
    else:
        run(gui=args.gui)
