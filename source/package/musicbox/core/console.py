# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
import sys

from musicbox import dev


dev.add_loaded_module(__name__)


class Console():

    welcome_text = f'Python {sys.version} on {sys.platform}\n'
    
    _builtins_initialized = False

    @classmethod
    def _init_builtins(cls):
        if not cls._builtins_initialized:
            builtins_dict = vars(sys.modules['builtins'])
            help_function = builtins_dict['help']
            builtins_dict['help'] = lambda subject : help_function(subject)
            del builtins_dict['license']

    def __init__(self):
        locals = vars(sys.modules['__main__'])
        self._console = code.InteractiveConsole(locals)
        self._init_prompt()
        self._init_history()

    def _init_prompt(self):
        try:
            self._ps1 = sys.ps1
        except AttributeError:
            self._ps1 = ">>> "
        try:
            self._ps2 = sys.ps2
        except AttributeError:
            self._ps2 = "... "
        self._prompt = self._ps1

    def _init_history(self):
        self._history = [""]
        self._history_index = 0

    def run(self):
        print(self.welcome_text)
        self._init_builtins()

    def prompt(self):
        return self._prompt

    def push(self, line):
        self._history_index = len(self._history) - 1
        self._history[self._history_index] = line
        if line.strip():
            self._history.append("")
            self._history_index += 1
        if self._console.push(line):
            self._prompt = self._ps2
        else:
            self._prompt = self._ps1

    def reset(self):
        self._console.resetbuffer()

    def current_history_entry(self):
        return self._history[self._history_index]
    
    def move_up_history(self):
        self._history_index = max(self._history_index - 1, 0)

    def move_down_history(self):
        self._history_index = min(self._history_index + 1, len(self._history) - 1)
