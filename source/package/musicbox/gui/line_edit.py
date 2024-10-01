# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from musicbox import config, dev

if config.pyside_version() == 2:
    from PySide2.QtCore import QEvent, QObject, Qt, Signal, Slot
    from PySide2.QtWidgets import QLineEdit
else:
    from PySide6.QtCore import QEvent, QObject, Qt, Signal, Slot
    from PySide6.QtWidgets import QLineEdit


class LineEdit(QLineEdit):

    up = Signal()
    down = Signal()
    line = Signal(str, str)
    tab = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_prompt("")
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if object is self and event.type() is QEvent.KeyPress:
            if event.key() == Qt.Key_Tab:
                self.tab.emit(self.text())
                return True
        return False
 
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return:
            self.line.emit(self.prompt(), self.text())
        elif key == Qt.Key_Up:
            self.up.emit()
        elif key == Qt.Key_Down:
            self.down.emit()
        elif (key != Qt.Key_Backspace and key != Qt.Key_Left) or self.cursorPosition() > len(self.prompt()):
            super().keyPressEvent(event)
        else:
            event.accept()

    def text(self):
        return super().text()[len(self.prompt()):]

    @Slot(str)
    def setText(self, text=""):
        super().setText(f'{self.prompt()}{text}')

    def prompt(self):
        return self._prompt

    @Slot(str)
    def set_prompt(self, prompt=""):
        self._prompt = prompt
