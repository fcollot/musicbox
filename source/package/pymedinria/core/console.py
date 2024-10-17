# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
from contextlib import contextmanager
import sys
from threading import Lock

from . import config


_instance = None
_lock = Lock()


@contextmanager
def open(*args, **kwargs):
    """Context manager for the console.

    To be used as follows:

        with console.open(arguments):
            (code to execute)

   The arguments will be forwared to the console constructor.
    Only one console can be open at any time.

    """
    global _instance

    with _lock:
        if _instance:
            raise RuntimeError("The console is already open.")
        _instance = _Console(*args, **kwargs)

    try:
        yield _instance
    finally:
        with _lock:
            _instance.close()
            _instance = None


def instance():
    with _lock:
        return _instance


class _Console():
    """Interactive console for the Python intepreter.

    This class is a wrapper over the code module's InteractoveConsole class. It
    adds a prompt, a custom welcome message and a history of previously pushed
    expressions, and it also modifies some of the builtin functions that can
    cause issues outside the standard command line environment.
    """

    welcome_text = f'Python {sys.version} on {sys.platform}\n\n{config.application_name()} {config.application_version()}\n'
    
    def __init__(self, *, locals={}, show_welcome=True, exit_function=sys.exit):
        """
        The 'locals' option will cause the associated dict to be merged into the
        __main__ dict, allowing the symbols to be accessible within the console.

        A custom exit funtion can be specified. It will replace the builtin 'exit'
        and 'quit' functions.

        """
        try:
            self._init_internal_console(locals)
            self._init_builtins(exit_function)
            self._init_prompt()
            self._init_history()
            if show_welcome:
                self.show_welcome()
        except:
            self.close()
            raise

    def _init_internal_console(self, locals):
        main_scope = vars(sys.modules['__main__'])
        main_scope.update(locals)
        self._console = code.InteractiveConsole(locals=main_scope)

    def _init_builtins(self, exit_function):
        builtins_dict = vars(sys.modules['builtins'])
        self._builtins_dict_copy = builtins_dict.copy()
        help_function = builtins_dict['help']
        builtins_dict['help'] = lambda subject : help_function(subject)
        builtins_dict['exit'] = exit_function
        builtins_dict['quit'] = exit_function
        del builtins_dict['license']

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

    def show_welcome(self):
        print(self.welcome_text)

    def close(self):
        self._restore_builtins()

    def _restore_builtins(self):
        vars(sys.modules['builtins']).update(self._builtins_dict_copy)

    def push(self, line):
        """Push a line of text to the console.

        If the accumulated lines form a complete expression it will be
        evaluated by the interpreter within the __main__ context.

        """
        self._history_index = len(self._history) - 1
        self._history[self._history_index] = line

        if line.strip():
            self._history.append("")
            self._history_index += 1

        try:
            more = self._console.push(line)
        except SystemExit:
            self.close()
            return

        if more:
            self._prompt = self._ps2
        else:
            self._prompt = self._ps1

    def reset(self):
        """Reset the current stack of lines.
        """
        self._console.resetbuffer()

    def prompt(self):
        """The current prompt.

        The prompt for a new expression is '>>>'. The prompt for a
        multiline expression (after the first line) is '...'.

        """
        return self._prompt

    def current_history_entry(self):
        return self._history[self._history_index]
    
    def move_up_history(self):
        self._history_index = max(self._history_index - 1, 0)

    def move_down_history(self):
        self._history_index = min(self._history_index + 1, len(self._history) - 1)
