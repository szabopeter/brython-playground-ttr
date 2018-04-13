import unittest
from controlid import ControlIdFactory


class BrythonFunctionsMock:
    def __init__(self, *valid_ids):
        self.valid_ids = valid_ids

    def get_element(self, eid):
        if eid in self.valid_ids:
            return eid

        raise KeyError()


class ControlIdTestCase(unittest.TestCase):
    def test_validation(self):

        cif = ControlIdFactory(BrythonFunctionsMock("existing8", "existing5", "existing8_sub"), 8)

        self.assertTrue(cif.is_valid()[0])

        cif.create("existing")
        self.assertTrue(cif.is_valid()[0])

        cif.create("is_missing")
        valid, message = cif.is_valid()
        self.assertFalse(valid)
        self.assertIn("is_missing", message)
