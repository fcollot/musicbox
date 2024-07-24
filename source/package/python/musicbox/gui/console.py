# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import code
import sys

from ..core import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Signal, Slot
    from PySide2.QtWidgets import QLabel, QLineEdit, QScrollArea, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Qt, Signal, Slot
    from PySide6.QtWidgets import QLabel, QLineEdit, QScrollArea, QVBoxLayout, QWidget


class CommandLine(QLineEdit):

    def __init__(self):
        super().__init__()
        self.prompt = ""
        self._history = [""]
        self._history_index = 0
 
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Down or key == Qt.Key_Up:
            if key == Qt.Key_Down:
                self._history_index = min(self._history_index + 1, len(self._history) - 1)
            else:
                self._history_index = max(self._history_index - 1, 0)
            self.setText(self._history[self._history_index])
        elif key == Qt.Key_Return:
            self._history_index = len(self._history) - 1
            line = self.line()
            self._history[self._history_index] = line
            if line.strip():
                self._history.append("")
                self._history_index += 1
        if key != Qt.Key_Backspace or self.cursorPosition() > len(self.prompt):
            super().keyPressEvent(event)
        else:
            event.accept()

    def line(self):
        return super().text()[len(self.prompt):]

    def setText(self, text=""):
        super().setText(self.prompt + text)


class Console(QWidget):
    
    WELCOME_TEXT = f'Python {sys.version} on {sys.platform}\n'

    exit = Signal()
    _builtins_initialized = False

    @classmethod
    def _init_builtins(cls):
        if not cls._builtins_initialized:
            builtins_dict = sys.modules['builtins'].__dict__
            help_function = builtins_dict['help']
            builtins_dict['help'] = lambda subject : help_function(subject)
            del builtins_dict['license']

    def __init__(self, *, size=(800, 600), title="Python console", shared_output=False):
        super().__init__()
        self._init_window(size, title)
        self._init_output_widget()
        self._init_input_widget()
        self._init_fonts()
        self._init_builtins()
        self._init_prompt()
        self.is_running = False
 
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
        self._input_widget = CommandLine()
        self.layout().addWidget(self._input_widget)
        self.setFocusProxy(self._input_widget)
        self._input_widget.returnPressed.connect(self._handle_input)
        self._input_widget.cursorPositionChanged.connect(self._ensure_cursor_after_prompt)

    def _init_fonts(self):
        font = self._output_widget.font()
        font.setFamily("Courier")
        self._output_widget.setFont(font)
        self._input_widget.setFont(font)
        self._input_widget.setFrame(False)

    def _init_prompt(self):
        try:
            self.ps1 = sys.ps1
        except AttributeError:
            self.ps1 = ">>> "
        try:
            self.ps2 = sys.ps2
        except AttributeError:
            self.ps2 = "... "
        self._input_widget.prompt = self.ps1
        self._input_widget.setText()

    def run(self):
        if not self.is_running:
            self._stdout = sys.stdout
            sys.stdout = self
            sys.stderr = self
            self._interpreter = code.InteractiveInterpreter(sys.modules['__main__'].__dict__)
            self._reset_input_buffer()
            self._print_welcome_text()
            self.is_running = True

    def _print_welcome_text(self):
        self.print(self.WELCOME_TEXT, internal=True)
  
    def _reset_input_buffer(self):
        self._input_buffer = []

    @Slot()
    def _handle_input(self):
        self.print(self._input_widget.text(), internal=True)
        line = self._input_widget.line()
        self._input_buffer.append(line)
        source = "\n".join(self._input_buffer)
        try:
            more = self._interpreter.runsource(source)
            self._update_input_status(new_command = not(more and line))
        except SystemExit:
            self._update_input_status()
            self.exit.emit()

    def _update_input_status(self, new_command=True):
        if new_command:
            self._input_widget.prompt = self.ps1
            self._reset_input_buffer()
        else:
            self._input_widget.prompt = self.ps2
        self._input_widget.setText()

    @Slot(int, int)
    def _ensure_cursor_after_prompt(self, _, new_position):
        self._input_widget.setCursorPosition(max(len(self._input_widget.prompt), new_position))

    def print(self, text, *, internal=False):
        self.write(text + '\n', internal=internal)

    def write(self, text, *, internal=False):
        if not internal:
            self._stdout.write(text)
        self._output_widget.setText(f'{self._output_widget.text()}{text}')

    def flush(self):
        self._stdout.flush()
        pass

    def showEvent(self, event):
        self.setFocus()
