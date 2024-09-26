# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


def generate_unique_name(prefix, existing_names=[]):
    name = prefix
    if name in existing_names:
        i = 1
        while True:
            suffixed_name = f'{name}_{i}'
            if suffixed_name not in existing_names:
                break
            i += 1
        name = suffixed_name
    return name
