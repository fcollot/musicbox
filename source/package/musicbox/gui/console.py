# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
from rlcompleter import Completer
import sys

from musicbox import config, dev
from musicbox.core.console import Console
from .line_edit import LineEdit

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Signal, Slot
    from PySide2.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Qt, Signal, Slot
    from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


dev.add_loaded_module(__name__)


class GUIConsole(QWidget):

    exit = Signal()

    def __init__(self, parent=None, *, size=(800, 600), title="Python console", shared_output=False):
        super().__init__(parent)
        self._init_window(size, title)
        self._init_output_widget()
        self._init_console()
        self._init_input_widget()
        self._init_fonts()
        self._init_completion()
        self.is_running = False

    def _init_window(self, size, title):
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)
        self.resize(*size)

    def _init_console(self):
        sys.stdout = self
        sys.stderr = self
        self._console = Console()

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
        self._input_widget.up.connect(self._console.move_up_history)
        self._input_widget.up.connect(self._update_input_widget)
        self._input_widget.down.connect(self._console.move_down_history)
        self._input_widget.down.connect(self._update_input_widget)
        self._input_widget.cursorPositionChanged.connect(self._ensure_cursor_after_prompt)
        self._input_widget.tab.connect(self._complete_input)

    def _init_fonts(self):
        font = self._output_widget.font()
        font.setFamily("Courier")
        self._output_widget.setFont(font)
        self._input_widget.setFont(font)
        self._input_widget.setFrame(False)

    def _init_completion(self):
        self._completer = Completer()

    def run(self):
        if not self.is_running:
            self._console.run()
            self.is_running = True
  
    @Slot(str, str)
    def _handle_input(self, prompt, text):
        print(f'{prompt}{text}')
        self._console.push(text)
        self._update_input_widget()

    def _update_input_widget(self):
        self._input_widget.set_prompt(self._console.prompt())
        self._input_widget.setText(self._console.current_history_entry())

    @Slot(int, int)
    def _ensure_cursor_after_prompt(self, _, new_position):
        self._input_widget.setCursorPosition(max(len(self._input_widget.prompt()), new_position))

    def print(self, text):
        self.write(f'{text}\n')

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
                    self.write(f'{completions[i]}\t\t')

    def _completions(self, text):
        state = 0
        completions = []
        while True:
            completion = self._completer.complete(text, state)
            state += 1
            if completion:
                completions.append(completion)
            else:
                break
        return completions
