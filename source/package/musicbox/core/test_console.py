# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
import unittest

from . import console


class TestConsole(unittest.TestCase):

    def setUp(self):
        self._console_kwargs = {'show_welcome': False}
        try:
            del self._main_scope()['foo']
        except KeyError:
            pass

    def test_console_closes_when_exiting_context(self):
        with console.open(**self._console_kwargs) as c:
            self.assertTrue(console.instance())
        self.assertFalse(console.instance())

    def test_assigment_console_statement(self):
        """
        Test that assignments through the console affect the main scope.
        """
        with console.open(**self._console_kwargs) as c:
            c.push("foo = 1")
            self.assertEqual(self._main_scope()['foo'], 1)

    def test_multiline_console_statement(self):
        """
        Test that multiline statements through the console work properly.
        """
        with console.open(**self._console_kwargs) as c:
            c.push("def set_foo(x):")
            c.push("    global foo")
            c.push("    foo = x")
            c.push("")
            self._main_scope()['set_foo'](2)
            self.assertEqual(self._main_scope()['foo'], 2)

    def test_console_history(self):
        s1 = "foo = 1"
        s2 = "foo = 2"
        s3 = "foo = 3"

        with console.open(**self._console_kwargs) as c:
            c.push(s1)
            c.push(s2)
            c.push(s3)
            self.assertEqual(c.current_history_entry(), "")
            c.move_up_history()
            self.assertEqual(c.current_history_entry(), s3)
            c.move_up_history()
            self.assertEqual(c.current_history_entry(), s2)
            c.move_up_history()
            self.assertEqual(c.current_history_entry(), s1)
            c.move_up_history()
            self.assertEqual(c.current_history_entry(), s1)
            c.move_down_history()
            self.assertEqual(c.current_history_entry(), s2)
            c.move_down_history()
            self.assertEqual(c.current_history_entry(), s3)
            c.move_down_history()
            self.assertEqual(c.current_history_entry(), "")
            c.move_down_history()
            self.assertEqual(c.current_history_entry(), "")
        
    def _main_scope(self):
        return vars(sys.modules['__main__'])
