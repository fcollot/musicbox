# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.core import dev
from .application import application_class, init_application_class


def instance():
    """The current Qt application instance.

    """
    return application_class().instance()


def run(*, gui=True, developer_mode=False):
    """Run MusicBox.

    Use the 'gui' option to run in GUI or console-only mode.

    The developer mode activates various functons such as automatic reloading of
    modules (when modified) or the display of specific information on the
    console.

    """
    app = instance()

    if app is None:
        app = application_class()()
    else:
        raise RuntimeError("Cannot run MusicBox because another Qt application is already running.")

    if developer_mode:
        dev.set_developer_info(True)
        dev.set_auto_reload(True)

    return app.run()


def quit():
    application_class().instance().quit()


def main():
    """Application entry point when running from the command line.

    Do not call this function from Python code. Use 'run()' instead.

    """
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()

    parser.add_argument('--gui', action=BooleanOptionalAction, default=True,
                        help="Run in GUI mode or not (default: --gui)"
    )
    parser.add_argument('--test', choices=['no-gui', 'gui', 'all'],
                        help="Run the unit tests"
    )
    parser.add_argument('--dev', action='store_true',
                        help="Enable developer utils when running the application"
    )
    args = parser.parse_args()

    if args.test:
        if args.test == 'no-gui' or args.test == 'all':
            dev.run_tests(gui=False)
        if args.test == 'gui' or args.test == 'all':
            dev.run_tests(gui=True)
    else:
        run(gui=args.gui, developer_mode=args.dev)
