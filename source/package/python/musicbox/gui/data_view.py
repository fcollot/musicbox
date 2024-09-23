# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from .. import config

if config.pyside_version() == 2:
    from PySide2.QtWidgets import QWidget, QVBoxLayout
else:
    from PySide6.QtWidgets import QWidget, QVBoxLayout

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util import numpy_support
import SimpleITK as sitk


class DataView(QWidget):

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

        self._data = []

    def _add_sitk_image(self, image):
        #self.sliceSlider = QSlider(Qt.Horizontal)
        #self.sliceSlider.valueChanged.connect(self.updateSlice)
        #self.layout().addWidget(self.sliceSlider)

#        self.sliceLabel = QLabel("Slice: 0")
#        self.layout().addWidget(self.sliceLabel)

        self.sliceMapper = vtk.vtkImageSliceMapper()
        imageSlice = vtk.vtkImageSlice()
        imageSlice.SetMapper(self.sliceMapper)
        self.renderer.AddViewProp(imageSlice)

        vtk_image = numpy_utils.voxel_set_to_vtk_image(data_set)
        self.sliceMapper.SetInputData(self.vtk_image)
        self.sliceMapper.SetOrientationToZ()
        self.sliceMapper.SetSliceNumber(0)
        self.sliceMapper.Update()

        self.sliceSlider.setMaximum(self.vtk_image.GetDimensions()[2] - 1)
        self.currentSlice = 0
        self.updateSlice()

        self.renderer.ResetCamera()

        self._data.append(data)
        self._image_slicers[data] = image_slice

        return self.vtk_image
