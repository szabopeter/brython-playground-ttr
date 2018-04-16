import unittest
from controlid import ControlIdFactory
from testutil import BrythonFunctionsMock


class ControlIdTestCase(unittest.TestCase):
    def test_validation(self):

        brython_functions = BrythonFunctionsMock.using_idlist("existing8", "existing5", "existing8_sub")
        cif = ControlIdFactory(brython_functions, 8)

        self.assertTrue(cif.is_valid()[0])

        cif.create("existing")
        self.assertTrue(cif.is_valid()[0])

        cif.create("is_missing")
        valid, message = cif.is_valid()
        self.assertFalse(valid)
        self.assertIn("is_missing", message)
