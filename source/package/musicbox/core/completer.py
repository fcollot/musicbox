# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import re
import rlcompleter

from musicbox.core import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Object, Slot, Signal
else:
    from PySide6.QtCore import QObject, Slot, Signal


class Completer(QObject, rlcompleter.Completer):

    successful_completion = Signal(str)
    possible_completions = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str)
    def complete(self, text):
        if text:
            match = re.search("[^\\( ]*$", text)

            try:
                completable_part = match.group(0)
            except IndexError:
                return

            completions = self.find_completions(completable_part)

            if completions:
                if len(completions) == 1:
                    completion = completions[0]
                    self.successful_completion.emit(text[:match.start(0)] + completion)
                else:
                    self.possible_completions.emit(completions)

    def find_completions(self, text):
        state = 0
        completions = []

        while True:
            completion = super().complete(text, state)
            state += 1
            if completion:
                completions.append(completion)
            else:
                break

        return completions
