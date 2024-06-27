# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import os.path


readers = []


class Image():

    def __init__(self, input):
        
        if isinstance(input, str):
            if os.path.isfile(input):
                for reader in readers:
                    if reader(input, self):
                        break
