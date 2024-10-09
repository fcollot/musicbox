# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib
import sys
import unittest

from musicbox import app


class TestCommandLine(unittest.TestCase):
    """Test that command line options are correctly handled.

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
        app.run = self._function_call_tracker('run_app')
        app.dev.run_tests = self._function_call_tracker('run_tests')
        app.dev.set_auto_reload = self._function_call_tracker('set_auto_reload')
        self._function_calls = []

    def tearDown(self):
        sys.argv = self._previous_argv

    def test_non_gui_tests_option(self):
        self._ensure_options_trigger_function_call(['--test', 'no-gui'], 'run_tests', [[{'gui': False}]])

    def test_gui_tests_option(self):
        self._ensure_options_trigger_function_call(['--test', 'gui'], 'run_tests', [[{'gui': True}]])

    def test_all_tests_option(self):
        self._ensure_options_trigger_function_call(['--test', 'all'], 'run_tests', [[{'gui': True}], [{'gui': False}]])

    def test_gui_option(self):
        sys.argv = ['', '--gui']
        self._ensure_options_trigger_function_call(['--gui'], 'run_app', [[{'gui': True}]])

    def test_no_gui_option(self):
        self._ensure_options_trigger_function_call(['--no-gui'], 'run_app', [[{'gui': False}]])

    def test_gui_option_is_default(self):
        self._ensure_options_trigger_function_call([], 'run_app', [[{'gui': True}]])

    def test_dev_option_triggers_auto_reload(self):
        self._ensure_options_trigger_function_call(['--dev'], 'set_auto_reload', [[True]])

    def test_auto_reload_is_off_by_default(self):
        sys.argv = ['']
        app.main()
        self.assertFalse(app.dev.auto_reload())

    def _function_call_tracker(self, name):
        def _track_function_call(*args, **kwargs):
            all_args = [*args]
            if kwargs:
                all_args.append(kwargs)
            self._function_calls.append([name, all_args])

        return _track_function_call

    def _ensure_options_trigger_function_call(self, cl_options, function_name, expected_args_list):
        sys.argv = ['', *cl_options]
        app.main()
        args_list = []

        for function_call in self._function_calls:
            name, args = function_call
            if name == function_name:
                args_list.append(args)

        if not args:
            raise AssertionError(f'The function {function_name} was not called.')

        for expected_args in expected_args_list:
            try:
                args_list.remove(expected_args)
            except:
                raise AssertionError(f'Expected {function_name} to be called with arguments {expected_args_list}.')

        if args_list:
            raise AssertionsError(f'Unexpected call(s) to {function_name} with argument(s) {args_list}.')
