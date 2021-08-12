import unittest
from hdl import *


class TestWire(unittest.TestCase):

    def test_bus(self):
        b = bus()
        self.assertEqual(b._v, 0b0000, "v() failed")
        b.v(0b1010)
        self.assertEqual(b._v, 0b1010, "v() failed")
        w = b.wire(1)
        self.assertEqual(w.v(), 1, "v failed")
        w = b.wire(0)
        self.assertEqual(w.v(), 0, "v failed")


if __name__ == '__main__':
    unittest.main()