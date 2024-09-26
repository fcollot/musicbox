# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import unittest

from musicbox.core import dev
from .mesh import *


dev.add_loaded_module(__name__)


class TestVTKMeshCreation(unittest.TestCase):

    def test_output_is_vtk_poly_data(self):
        mesh = create_vtk_mesh(8, lines=12)
        self.assertIsInstance(mesh, vtk.vtkPolyData)
