# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import unittest

from .image import *


class TestSITKImageCreation(unittest.TestCase):

    test_shape = (2, 5, 3)

    def test_output_is_sitk_image(self):
        image = create_sitk_image(self.test_shape)
        self.assertIsInstance(image, sitk.Image)

    def test_with_shape_only(self):
        image = create_sitk_image(self.test_shape)
        self.assertEqual(self.test_shape, image.GetSize())

    def test_default_type_is_uint8(self):
        image = create_sitk_image(self.test_shape)
        self.assertEqual(image.GetPixelIDValue(), sitk_type_map[numpy.uint8])

    def test_with_shape_and_type(self):
        data_type = numpy.float32
        image = create_sitk_image(self.test_shape, data_type)
        self.assertEqual(image.GetPixelIDValue(), sitk_type_map[data_type])

    def test_with_numpy_array(self):
        input_pixels = numpy.random.rand(*self.test_shape)
        image = create_sitk_image(input_pixels)
        self.assertTrue(numpy.array_equal(input_pixels, pixels(image)))

    def test_with_sitk_image(self):
        input_pixels = numpy.random.rand(*self.test_shape)
        input_image = create_sitk_image(input_pixels)
        output_image = create_sitk_image(input_image)
        self.assertTrue(numpy.array_equal(input_pixels, pixels(output_image)))

    def test_with_vtk_image(self):
        input_pixels = numpy.random.rand(*self.test_shape)
        input_image = create_vtk_image(input_pixels)
        output_image = create_sitk_image(input_image)
        self.assertTrue(numpy.array_equal(input_pixels, pixels(output_image)))


class TestVTKImageCreation(unittest.TestCase):

    test_shape = (2, 5, 3)

    def test_output_is_vtk_image(self):
        image = create_vtk_image(self.test_shape)
        self.assertIsInstance(image, vtk.vtkImageData)

    def test_with_shape_only(self):
        image = create_vtk_image(self.test_shape)
        self.assertEqual(self.test_shape, image.GetDimensions())

    def test_default_type_is_uint8(self):
        image = create_vtk_image(self.test_shape)
        self.assertEqual(image.GetPointData().GetScalars().GetDataType(), vtk_type_map[numpy.uint8])

    def test_with_shape_and_type(self):
        data_type = numpy.float32
        image = create_vtk_image(self.test_shape, data_type)
        self.assertEqual(image.GetPointData().GetScalars().GetDataType(), vtk_type_map[data_type])

    def test_with_numpy_array(self):
        input_pixels = numpy.random.rand(*self.test_shape)
        image = create_vtk_image(input_pixels)
        self.assertTrue(numpy.array_equal(input_pixels, pixels(image)))

    def test_with_sitk_image(self):
        input_pixels = numpy.random.rand(*self.test_shape)
        input_image = create_sitk_image(input_pixels)
        output_image = create_vtk_image(input_image)
        self.assertTrue(numpy.array_equal(input_pixels, pixels(output_image)))

    def test_with_vtk_image(self):
        input_pixels = numpy.random.rand(*self.test_shape)
        input_image = create_vtk_image(input_pixels)
        output_image = create_vtk_image(input_image)
        self.assertTrue(numpy.array_equal(input_pixels, pixels(output_image)))
