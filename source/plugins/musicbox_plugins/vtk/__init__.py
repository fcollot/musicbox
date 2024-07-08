# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import musicbox

if musicbox.config.pyside_version == 2:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QLabel, QSlider, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QLabel, QSlider, QVBoxLayout, QWidget

import SimpleITK as sitk
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Viewer(QWidget):

    def __init__(self, image=None):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.vtk_widget = QVTKRenderWindowInteractor()
        self.layout().addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        self.sliceSlider = QSlider(Qt.Horizontal)
        self.sliceSlider.valueChanged.connect(self.updateSlice)
        self.layout().addWidget(self.sliceSlider)

        self.sliceLabel = QLabel("Slice: 0")
        self.layout().addWidget(self.sliceLabel)

        if image:
            self.sliceMapper = vtk.vtkImageSliceMapper()
            self.imageSlice = vtk.vtkImageSlice()
            self.imageSlice.SetMapper(self.sliceMapper)
            self.renderer.AddViewProp(self.imageSlice)

            self.image = image
            self.sliceMapper.SetInputData(image)
            self.sliceMapper.SetOrientationToZ()
            self.sliceMapper.SetSliceNumber(0)
            self.sliceMapper.Update()

            self.sliceSlider.setMaximum(image.GetDimensions()[2] - 1)
            self.currentSlice = 0
            self.updateSlice()

            self.renderer.ResetCamera()
            self.renderer.GetRenderWindow().Render()
            self.interactor.Initialize()
            self.interactor.Start()

    def updateSlice(self):
        slice_number = self.sliceSlider.value()
        self.sliceMapper.SetSliceNumber(slice_number)
        self.sliceMapper.Update()
        self.sliceLabel.setText(f"Slice: {slice_number}")
        self.renderer.GetRenderWindow().Render()
