# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause

from tokenize import generate_tokens

from ..core import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Signal, Slot
    from PySide2.QtGui import QTextCursor
    from PySide2.QtWidgets import QTextEdit
else:
    from PySide6.QtCore import Qt, Signal, Slot
    from PySide6.QtGui import QTextCursor
    from PySide6.QtWidgets import QTextEdit


DEFAULT_COLORS = {
    'KEYWORD': (255, 100, 100),
    'ASSIGNED_VARIABLE': (255, 0, 0),
    'FUNCTION_NAME': (0, 0, 255),
    'CLASS_NAME': (0, 255, 0),
    'BUILTIN_NAME': (100, 100, 255),
}


class CodeEditor(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._block_tokenizer = generate_tokens(lambda : self.textCursor().block().text())

    def keyPressEvent(self, event):
        key = event.key()
        super().keyPressEvent(event)
        tokens = next(self._block_tokenizer)
        cursor = self.textCursor()
        cursor.setPosition(cursor.block().position)
        for token in tokens:
            cursor.movePositiontoken.start[1]
            if token.type is tokenize.NAME:
                pass
