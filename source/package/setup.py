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
)
