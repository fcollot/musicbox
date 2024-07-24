# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Qt, Signal, Slot
    from PySide2.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Qt, Signal, Slot
    from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from musicbox.core import Settings


class WelcomeWidget(QWidget):

    link_hovered = Signal(str)
    link_unhovered = Signal()

    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())
        self.layout().addWidget(QLabel("LINKS"), 1, 2, Qt.AlignLeft)
        self.layout().addWidget(self._create_links_section(), 2, 2, Qt.AlignLeft | Qt.AlignTop)
        self.layout().addWidget(QLabel("RECENT FILES"), 1, 1, Qt.AlignLeft)
        self.layout().addWidget(self._create_recent_section(), 2, 1, Qt.AlignLeft | Qt.AlignTop)
        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 3)
        self.layout().setColumnStretch(2, 3)
        self.layout().setColumnStretch(3, 1)
        self.layout().setRowStretch(0, 1)
        self.layout().setRowStretch(3, 1)

    def _create_links_section(self):
        root = QWidget()
        root.setLayout(QVBoxLayout())

        links = [
            ("User Manual", 'https://github.com/LIRYC-IHU/musicbox'),
            ("Website", 'https://github.com/LIRYC-IHU/musicbox'),
            ("Community", 'https://github.com/LIRYC-IHU/musicbox'),
            ("Source code", 'https://github.com/LIRYC-IHU/musicbox'),
        ]

        class LinkLabel(QLabel):

            link_hovered = Signal(str)
            link_unhovered = Signal()

            def __init__(self, text, link):
                super().__init__(f'<a href="{link}">{text}</a>')
                self._link = link
                self.setTextFormat(Qt.RichText)
                self.setTextInteractionFlags(Qt.TextBrowserInteraction)
                self.setOpenExternalLinks(True)

            def enterEvent(self, event):
                event.accept()
                self.link_hovered.emit(self._link)

            def leaveEvent(self, event):
                event.accept()
                self.link_unhovered.emit()

        for text, link in links:
            label = LinkLabel(text, link)
            root.layout().addWidget(label, 0, Qt.AlignLeft)
            label.link_hovered.connect(self.link_hovered)
            label.link_unhovered.connect(self.link_unhovered)

        return root

    def _create_recent_section(self):
        root = QWidget()
        root.setLayout(QVBoxLayout())
        root.layout().setSpacing(0)

        recent_files = Settings().value('recent_files', [])

        if recent_files:
            for i in range(10):
                try:
                    recent_file = recent_files[i]
                    button_text = f'{i + 1}.) {recent_file}'
                except IndexError:
                    recent_file = ""
                    button_text = ""
                finally:
                    button = QPushButton(button_text)
                    button.setFlat(True)
                    # button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    root.layout().addWidget(button, 0, Qt.AlignLeft)
                    button.clicked.connect(lambda _ : self.open_file[str].emit(recent_file))
        else:
            root.layout().addWidget(Qt.Label("No recent files"), 0, Qt.AlignLeft)

        root.layout().addStretch(1)
                
        return root
