# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import unittest

from .view import *
from musicbox.data.mesh import create_vtk_mesh

import time

class TestView(unittest.TestCase):

    def test_no_duplicate_prop(self):
        mesh = create_vtk_mesh(8, triangles=12)
        prop1 = manager().find_or_create_prop(mesh, '3D')
        prop2 = manager().find_or_create_prop(mesh, '3D')
        self.assertEqual(prop1, prop2)

    def test_view_creation(self):
        view = manager().create_view('3D')
        self.assertIsInstance(view, QVTKRenderWindowInteractor)
