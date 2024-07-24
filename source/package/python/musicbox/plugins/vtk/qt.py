# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import musicbox

if musicbox.config.pyside_version == 2:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QLabel, QSlider, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QLabel, QSlider, QVBoxLayout, QWidget

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from . import numpy_utils


class QtViewer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        self.vtk_widget = QVTKRenderWindowInteractor()
        self.layout().addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        self.renderer.ResetCamera()
        self.renderer.GetRenderWindow().Render()
        self.interactor.Initialize()
        self.interactor.Start()

    def viewer_backend(self):
        return self.vtk_widget

    def add_data_set(self, data_set):
        return self.add_voxel_set(data_set)

    def add_voxel_set(self, data_set):
        self.sliceSlider = QSlider(Qt.Horizontal)
        self.sliceSlider.valueChanged.connect(self.updateSlice)
        self.layout().addWidget(self.sliceSlider)

#        self.sliceLabel = QLabel("Slice: 0")
#        self.layout().addWidget(self.sliceLabel)

        self.sliceMapper = vtk.vtkImageSliceMapper()
        self.imageSlice = vtk.vtkImageSlice()
        self.imageSlice.SetMapper(self.sliceMapper)
        self.renderer.AddViewProp(self.imageSlice)

        self.data_set = data_set
        self.vtk_image = numpy_utils.voxel_set_to_vtk_image(data_set)
        self.sliceMapper.SetInputData(self.vtk_image)
        self.sliceMapper.SetOrientationToZ()
        self.sliceMapper.SetSliceNumber(0)
        self.sliceMapper.Update()

        self.sliceSlider.setMaximum(self.vtk_image.GetDimensions()[2] - 1)
        self.currentSlice = 0
        self.updateSlice()

        self.renderer.ResetCamera()

        return self.vtk_image

    def updateSlice(self):
        slice_number = self.sliceSlider.value()
        self.sliceMapper.SetSliceNumber(slice_number)
        self.sliceMapper.Update()
        #self.sliceLabel.setText(f"Slice: {slice_number}")
        self.renderer.GetRenderWindow().Render()
