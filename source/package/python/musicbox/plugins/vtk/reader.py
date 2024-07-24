# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import vtk
from musicbox import plugins


class Reader():

    @staticmethod
    def file_filters():
        return {'VTK files': ['*.vtk']}

    def read(self, filename):
        reader = vtk.vtkGenericDataObjectReader()
        reader.SetFileName(filename)
        reader.Update()
        points = np.array(reader.GetOutput().GetPoints().GetData())

        
        sitk_image = sitk.ReadImage(filename)
        np_array = sitk.GetArrayFromImage(sitk_image)
        np_image = plugins.load_plugin('data', 'numpy_image')(np_array)
        return np_image
