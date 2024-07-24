# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .. import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Signal, Slot
    from PySide2.QtWidgets import QAction, QCheckBox, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QRadioButton, QSpinBox, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Signal, Slot
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QCheckBox, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QRadioButton, QSpinBox, QVBoxLayout, QWidget

from musicbox.core import PluginLoader

from .file_actions import LoadFileAction


class LoadDataSetAction(LoadFileAction):

    TITLE = "Open data set"

    def __init__(self, parent=None):
        plugin_loader = PluginLoader(groups=('data_readers',))
        reader_plugins, _ = plugin_loader.load_all()
        readers = [plugin() for plugin in reader_plugins]
        super().__init__(self.TITLE, parent, readers=readers, add_to_recent=True)


class NewDataSetAction(QAction):

    TITLE = "New data set"

    def __init__(self, parent=None):
        super().__init__(f'{self.TITLE}...', parent)
        self.triggered.connect(self._select_type)

    @Slot()
    def _select_type(self):
        dialog = QDialog()
        self._dialog = dialog
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(QLabel("Select type:"))
        dialog.layout().addWidget(self._create_image_type_widget())
        dialog.layout().addWidget(self._create_mesh_type_widget())
        if dialog.exec() is QDialog.Accepted:
            pass

    def _create_image_type_widget(self):
        root = QGroupBox("Image")
        root.setLayout(QVBoxLayout())
        root.setCheckable(True)
        form = QWidget()
        root.layout().addWidget(form)
        form.setLayout(QFormLayout())
        dimensions = QWidget()
        form.layout().addRow("Dimensions:", dimensions)
        dimensions.setLayout(QHBoxLayout())
        image_2D = QRadioButton("2D")
        image_3D = QRadioButton("3D")
        dimensions.layout().addWidget(image_2D)
        dimensions.layout().addWidget(image_3D)
        x_size = QSpinBox()
        y_size = QSpinBox()
        z_size = QSpinBox()
        x_size.setRange(0, 10000)
        y_size.setRange(0, 10000)
        z_size.setRange(0, 10000)
        form.layout().addRow("x", x_size)
        form.layout().addRow("y", y_size)
        form.layout().addRow("z", z_size)
        return root

    def _create_mesh_type_widget(self):
        root = QGroupBox("Mesh")
        root.setLayout(QVBoxLayout())
        root.setCheckable(True)
        return root
