import unittest

import implicit_namespace_foo
import implicit_namespace_foo.bar


class TestPep420ImplicitNamespacePackage(unittest.TestCase):
    """
    Testing Differences between namespace packages and regular packages as defined in PEP 420. See https://www.python.org/dev/peps/pep-0420/#differences-between-namespace-packages-and-regular-packages

    """

    def test_namespace_has_no_file_attribute(self):
        self.assertFalse(hasattr(implicit_namespace_foo, '__file__'))

    def test_namespace_has_no___init___module(self):
        with self.assertRaises(ModuleNotFoundError) as cm:
            import implicit_namespace_foo.__init__

    def test_namespace_has_different_type_of_object_for__loader__(self):
        self.assertNotEqual(type(implicit_namespace_foo.__loader__),
                            type(implicit_namespace_foo.bar.__loader__))
