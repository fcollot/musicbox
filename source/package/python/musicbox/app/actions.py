# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox.gui import LoadDataSetAction, NewDataSetAction, ShowLicenseAction


def create_main_actions(parent=None):
    actions = {
        'show_license': ShowLicenseAction(parent),
        'new_data_set': NewDataSetAction(parent),
        'open_data_set': LoadDataSetAction(parent),
    }
    return actions
