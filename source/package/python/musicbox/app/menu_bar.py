# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


def setup_menu_bar(menu_bar, actions):
    _init_file_menu(menu_bar, actions)


def _init_file_menu(menu_bar, actions):
    file_menu = menu_bar.addMenu("&File")
    file_menu.addAction(actions['new_data_set'])
    file_menu.addAction(actions['open_data_set'])
