# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from rlcompleter import Completer
import sys

from pymedinria.core import config, console
from .line_edit import LineEdit

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Signal, Slot
    from PySide2.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Qt, Signal, Slot
    from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


class ConsoleWidget(QWidget):
    """Widget to display console input and output.

    (The console must be created before this widget)
    In addition to providing a GUI for the console, this widget adds code
    completion using the tab key.

    """

    def __init__(self, parent=None, *, size=(800, 600), title=f'{config.application_name()} Python console', locals={}):
        super().__init__(parent)
        self._init_window(size, title)
        self._init_output_widget()
        self._init_input_widget()
        self._init_fonts()
        self._init_code_completion()
        self.destroyed.connect(lambda : self.update_output_streams(False))
        self.update_output_streams(True)
        console.instance().show_welcome()
  
    def _init_window(self, size, title):
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)
        self.resize(*size)

    def _init_output_widget(self):
        self._output_widget = QLabel()
        self._output_widget.setAlignment(Qt.AlignBottom)
        self._output_widget.setWordWrap(True)
        self._output_widget.setTextFormat(Qt.PlainText)
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidget(self._output_widget)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.horizontalScrollBar().setEnabled(False)
        scroll_bar = self._scroll_area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda _, max : scroll_bar.setValue(max))
        self.layout().addWidget(self._scroll_area)

    def _init_input_widget(self):
        self._input_widget = LineEdit()
        self.layout().addWidget(self._input_widget)
        self.setFocusProxy(self._input_widget)
        self._update_input_widget()
        self._input_widget.line.connect(self._handle_input)
        self._input_widget.up.connect(console.instance().move_up_history)
        self._input_widget.up.connect(self._update_input_widget)
        self._input_widget.down.connect(console.instance().move_down_history)
        self._input_widget.down.connect(self._update_input_widget)
        self._input_widget.cursorPositionChanged.connect(self._ensure_cursor_after_prompt)
        self._input_widget.tab.connect(self._complete_input)

    def _init_fonts(self):
        font = self._output_widget.font()
        font.setFamily("Courier")
        self._output_widget.setFont(font)
        self._input_widget.setFont(font)
        self._input_widget.setFrame(False)

    def _init_code_completion(self):
        self._completer = Completer()

    def update_output_streams(self, enable):
        if enable:
            self._stdout = sys.stdout
            self._stderr = sys.stderr
            sys.stdout = self
            sys.stderr = _StreamWrapper((sys.stderr, self))
        else:
            sys.stdout = self._stdout
            sys.stderr = self._stderr
  
    @Slot(str, str)
    def _handle_input(self, prompt, text):
        print(f'{prompt}{text}')
        console.instance().push(text)
        self._update_input_widget()

    def _update_input_widget(self):
        self._input_widget.set_prompt(console.instance().prompt())
        self._input_widget.setText(console.instance().current_history_entry())

    @Slot(int, int)
    def _ensure_cursor_after_prompt(self, _, new_position):
        self._input_widget.setCursorPosition(max(len(self._input_widget.prompt()), new_position))

    def write(self, text):
        self._output_widget.setText(f'{self._output_widget.text()}{text}')

    def flush(self):
        pass

    def showEvent(self, event):
        self.setFocus()

    @Slot(str)
    def _complete_input(self, text):
        completions = self._completions(text)
        if completions:
            if len(completions) == 1:
                self._input_widget.setText(completions[0])
            else:
                print(f'{self._input_widget.prompt()}{self._input_widget.text()}')
                for i in range(len(completions)):
                    sys.stdout.write(f'{completions[i]}\t\t')
                print()

    def _completions(self, text):
        state = 0
        completions = []
        completer = Completer()
        while True:
            completion = completer.complete(text, state)
            state += 1
            if completion:
                completions.append(completion)
            else:
                break
        return completions


class _StreamWrapper():
    """Combine multiple streams into one.

    Use for printing on both the console and the standard output.
    (This is currently used for the error stream only)

    """

    def __init__(self, streams):
        self._streams = streams

    def write(self, text):
        for stream in self._streams:
            stream.write(text)

    def flush(self):
        for stream in self._streams:
            stream.flush()
