# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import musicbox


gui = musicbox.gui.instance()


class CommandLine(gui.LineEdit):

    def __init__(self):
        super().__init__()
        self.prompt = ""
        self._history = [""]
        self._history_index = 0
 
    def keyPressEvent(self, event):
        key = event.key()
        if key == gui.Key_Down or key == gui.Key_Up:
            if key == gui.Key_Down:
                self._history_index = min(self._history_index + 1, len(self._history) - 1)
            else:
                self._history_index = max(self._history_index - 1, 0)
            self.setText(self._history[self._history_index])
        elif key == gui.Key_Return:
            self._history_index = len(self._history) - 1
            line = self.line()
            self._history[self._history_index] = line
            if line.strip():
                self._history.append("")
                self._history_index += 1
        if key != gui.Key_Backspace or self.cursorPosition() > len(self.prompt):
            super().keyPressEvent(event)
        else:
            event.accept()

    def line(self):
        return super().text()[len(self.prompt):]

    def setText(self, text=""):
        super().setText(self.prompt + text)
