# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib
import sys
import unittest

from musicbox import app


class TestCommandLineOptions(unittest.TestCase):
    """ Test that command line options are correctly handled.

    These tests replace the entry functions that would normally be called with
    special functions that allow checking if the expected function was called
    with the expected options (if applicable).

    """

    @classmethod
    def tearDownClass(cls):
        importlib.reload(app)
        importlib.reload(app.dev)

    def setUp(self):
        self._previous_argv = sys.argv
        app.run = self._dummy_function
        app.dev.run_tests = self._dummy_function
        self._validated = False

    def tearDown(self):
        sys.argv = self._previous_argv

    def test_test_option(self):
        """
        Test that --test runs the tests (╯°□°)╯︵ ┻━┻
        """
        sys.argv = ['', '--test', 'no-gui']
        app.dev.run_tests = self._option_validator({'gui': False})
        app.main()
        self.assertTrue(self._validated)

        sys.argv = ['', '--test', 'gui']
        app.dev.run_tests = self._option_validator({'gui': True})
        app.main()
        self.assertTrue(self._validated)

        def foo(**kwargs):
            try:
                self._option_validator({'gui': True})(**kwargs)
            except AssertionError:
                self._option_validator({'gui': False})(**kwargs)

        sys.argv = ['', '--test', 'all']
        app.dev.run_tests = foo
        app.main()
        self.assertTrue(self._validated)

    def test_gui_option(self):
        sys.argv = ['', '--gui']
        app.run = self._option_validator({'gui': True})
        app.main()
        self.assertTrue(self._validated)

    def test_no_gui_option(self):
        sys.argv = ['', '--no-gui']
        app.run = self._option_validator({'gui': False})
        app.main()
        self.assertTrue(self._validated)

    def test_gui_option_is_default(self):
        """
        Test that the MusicBox runs in GUI mode by default.
        """
        sys.argv = ['']
        app.run = self._option_validator({'gui': True})
        app.main()
        self.assertTrue(self._validated)

    def _option_validator(self, expected_kwargs={}):
        def _validate_option(**kwargs):
            for name, value in expected_kwargs.items():
                self.assertIn(name, kwargs)
                self.assertEqual(kwargs[name], value)
            self._validated = True

        return _validate_option

    @staticmethod
    def _dummy_function(*args, **kwargs):
        pass      
