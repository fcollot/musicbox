# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from distutils.core import setup


setup(name='musicbox_plugins',
      version='@PROJECT_VERSION@',
      install_requires=[
          'SimpleITK',
          'vtk',
      ],
      packages=[
          'musicbox_plugins',
          'musicbox_plugins.console',
          'musicbox_plugins.numpy',
          'musicbox_plugins.qt',
          'musicbox_plugins.simple_itk',
          'musicbox_plugins.vtk',
      ],
      entry_points = {
          'musicbox.console': [
              'musicbox = musicbox_plugins.console:Console'
          ],
          'musicbox.viewer': [
              'vtk = musicbox_plugins.vtk:Viewer'
          ],
          'musicbox.widgets.main_window': [
              'qt = musicbox_plugins.qt:MainWindow'
          ],
          'musicbox.slice_viewer': [
              'vtk = musicbox_plugins.vtk.slice_viewer:SliceViewer'
          ],
          'musicbox.reader': [
              'simple_itk = musicbox_plugins.simple_itk:Reader'
          ],
          'musicbox.data': [
              'numpy_image = musicbox_plugins.numpy:Image'
          ],
      }
)
