# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from distutils.core import setup
from setuptools import find_packages


setup(name='musicbox',
      version='@PROJECT_VERSION@',
      packages=find_packages(include=['musicbox', 'musicbox.*']),
      install_requires=[
      '@MBOX_PYSIDE_PACKAGE@',
      'SimpleITK',
      'vtk',
      ],
      entry_points = {
          'musicbox.console': [
              'musicbox = musicbox.plugins.console:Console'
          ],
          'musicbox.viewer.vtk': [
              'tk = musicbox.plugins.vtk.tk:TkViewer',
              'qt = musicbox.plugins.vtk.qt:QtViewer'
          ],
          'musicbox.gui': [
              'tk = musicbox.plugins.tk:Gui',
              'qt = musicbox.plugins.qt:Gui'
          ],
          'musicbox.data_readers': [
              'simple_itk = musicbox.plugins.simple_itk:Reader'
          ],
          'musicbox.data': [
              'numpy_image = musicbox.plugins.numpy:Image'
          ],
      }
)
