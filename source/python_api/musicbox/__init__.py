# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from PySide@MBOX_PYSIDE_VERSION_MAJOR@.QtCore import Qt
from PySide@MBOX_PYSIDE_VERSION_MAJOR@.QtWidgets import QApplication
from .main_window import MainWindow


main_window = None


stylesheet = """
    QWidget {
        background-color: #2E002E;
    }
    QMainWindow {
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    QLabel {
        color: #FFFFFF;
    }
    QMenuBar {
        background-color: #444444;
        color: #FFFFFF;
    }
    QMenuBar::item {
        background-color: #444444;
        color: #FFFFFF;
    }
    QMenuBar::item::selected {
        background-color: #555555;
    }
    QMenu {
        background-color: #444444;
        color: #FFFFFF;
    }
    QMenu::item::selected {
        background-color: #555555;
    }
"""


def run():
    app = QApplication()
    #app.setStyleSheet(stylesheet)
    create_main_window()
    return app.exec()

#    app.setStyleSheet(stylesheet)


def create_main_window():
    global main_window
    main_window = MainWindow()
    #main_window.setAttribute(Qt.WA_DeleteOnClose)
    main_window.show()
    return main_window
