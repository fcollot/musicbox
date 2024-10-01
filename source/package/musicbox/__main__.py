# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from argparse import ArgumentParser, BooleanOptionalAction


parser = ArgumentParser()
parser.add_argument('--gui', action=BooleanOptionalAction, default=True)
parser.add_argument('--test', action='store_true')
args = parser.parse_args()


if args.test:
    from . import dev
    dev.run_tests()
else:
    from .app import run
    run(
        gui=args.gui,
    )
