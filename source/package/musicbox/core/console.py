# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import builtins
import code
from importlib.metadata import version
import sys
import threading

from musicbox.core import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Object, Slot, Signal
else:
    from PySide6.QtCore import QObject, Slot, Signal


class Console(QObject):
    """Interactive console for the Python intepreter.

    This class is a wrapper over the code module's InteractiveConsole class. It
    adds a prompt, a custom welcome message and a history of previously pushed
    expressions, and it also modifies some of the builtin functions that can
    cause issues outside the terminal command line environment.
    """

    welcome_text = f'Python {sys.version} on {sys.platform}\n\nMusicBox {version("musicbox")}\n'

    run_ended = Signal()

    _running_instance = None

    def __init__(self, *, globals={}):
        """
        The 'locals' option will cause the associated dict to be merged into the
        __main__ dict, allowing the symbols to be accessible within the console.

        """
        super().__init__()
        self._lock = threading.RLock()
        self._globals = globals
        self._thread = None
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

    def run(self, *, command_line_thread=None):
        with self._lock:
            cls = type(self)
            if cls._running_instance:
                raise RuntimeError("A console instance is already running.")
            cls._running_instance = self

            self._command_line_thread = command_line_thread
            self._setup_internal_console()
            self._setup_printing()

            print(self.welcome_text)

            if not self._command_line_thread:
                self._run_command_line_thread()

    def _setup_internal_console(self):
        main_scope = vars(sys.modules['__main__'])
        main_scope.update(self._globals)
        self._console = code.InteractiveConsole(locals=main_scope)

    def _setup_printing(self):
        if not hasattr(builtins, '_print'):
            builtins._print = print
        builtins.print = self.print

    def _run_command_line_thread(self):
        self._command_line_thread = threading.Thread(
            target=self._command_line_loop,
            name="Console command line"
        )
        self._command_line_thread.start()

    def _command_line_loop(self):
        try:
            while True:
                line = input(self.prompt())
                self.push(line)
        except Exception as e:
            print(e)
        except SystemExit:
            pass
        finally:
            self.end_run()

    def end_run(self):
        with self._lock:
            self_console = None
            builtins.print = builtins._print
            type(self)._running_instance = None
            self._command_line_thread = None
            self.run_ended.emit()

    @Slot(str)
    def print(self, object='', sep='', end='\n', file=None, flush=False):
        with self._lock:
            thread = threading.current_thread()
            if thread is not self._command_line_thread:
                object = f'\n{object}{end}{self.prompt()}'
                end = ''
            builtins._print(object, sep=sep, end=end, file=file or sys.stdout, flush=flush)

    @Slot(str)
    def push(self, line):
        """Push a line of text to the console.

        If the accumulated lines form a complete expression it will be
        evaluated by the interpreter within the __main__ context.

        """
        with self._lock:
            self._history_index = len(self._history) - 1
            self._history[self._history_index] = line

            if line.strip():
                self._history.append("")
                self._history_index += 1

            more = self._console.push(line)

            if more:
                self._prompt = self._ps2
            else:
                self._prompt = self._ps1

    @Slot()
    def reset_input(self):
        """Reset the current stack of lines.
        """
        with self._lock:
            self._console.resetbuffer()

    def prompt(self):
        """The current prompt.

        The prompt for a new expression is '>>>'. The prompt for a
        multiline expression (after the first line) is '...'.

        """
        with self._lock:
            return self._prompt

    def current_history_entry(self):
        with self._lock:
            return self._history[self._history_index]

    @Slot()
    def move_up_history(self):
        with self._lock:
            self._history_index = max(self._history_index - 1, 0)

    @Slot()
    def move_down_history(self):
        with self._lock:
            self._history_index = min(self._history_index + 1, len(self._history) - 1)
