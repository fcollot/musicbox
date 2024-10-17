# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
import unittest

from pymedinria import app
from pymedinria.core import console
from .console_widget import ConsoleWidget


class TestConsoleWidget(unittest.TestCase):

    def setUp(self):
        self.console_widget = app.instance()._console_widget

    def test_unique_code_completion(self):
        unique_name = 'unique_name_1'
        console.instance().push(f'{unique_name} = None')
        self.console_widget._complete_input(unique_name[:-4])
        self.assertEqual(self.console_widget._input_widget.text(), unique_name)

    def test_multiple_code_completion(self):
        class StreamCapture():
            def __init__(self):
                self.output = []
                self.stdout = sys.stdout

            def write(self, text):
                self.output.append(text)
                self.stdout.write(text)

            def flush(self):
                self.stdout.flush()

        names = ('test_name_1', 'test_name_2', 'test_name_3')
        for name in names:
            console.instance().push(f'{name} = None')
        old_stdout = sys.stdout
        capture = StreamCapture()
        sys.stdout = capture
        self.console_widget._complete_input('test_name_')
        sys.stdout = capture.stdout
        output = ''.join(capture.output).split()
        for name in names:
            self.assertIn(name, output)
