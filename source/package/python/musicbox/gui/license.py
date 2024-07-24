# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from ..core import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Slot
    from PySide2.QtWidgets import QAction, QMessageBox
else:
    from PySide6.QtCore import Slot
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QMessageBox


class LicenseBox(QMessageBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("MusicBox licenses")
        self.setDetailedText("Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.\nLicense: BSD-3-Clause")


class ShowLicenseAction(QAction):

    NAME = "License"

    def __init__(self, parent):
        super().__init__(f'{self.NAME}...', parent)
        self.triggered.connect(self.show_license)

    @Slot()
    def show_license(self):
        license_box = LicenseBox()
        if config.pyside_version() == 2:
            license_box._exec()
        else:
            license_box.exec()
        
