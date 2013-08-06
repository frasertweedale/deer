import unittest

import deer


class Foo(deer.Deer):
    x = deer.DeerAttribute(type=str)
    y = deer.DeerAttribute(default='hi')
    z = deer.DeerAttribute(default=None)


class TypeTestCase(unittest.TestCase):
    def test_can_only_assign_valid_types(self):
        foo = Foo()
        foo.x = 'hi'
        self.assertEqual(foo.x, 'hi')
        with self.assertRaises(TypeError):
            foo.x = 10

    def test_can_only_init_with_valid_types(self):
        self.assertEqual(Foo(x='bye').x, 'bye')
        with self.assertRaises(TypeError):
            Foo(x=10)

class DefaultTestCase(unittest.TestCase):
    def test_has_default_value_if_no_constructor_arg_given(self):
        self.assertEqual(Foo().y, 'hi')

    def test_constructor_arg_overrides_default_value(self):
        self.assertEqual(Foo(y='bye').y, 'bye')

    def test_can_use_None_as_default(self):
        self.assertIsNone(Foo().z)
