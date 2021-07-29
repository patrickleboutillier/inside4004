import unittest
from hdl import *


class TestWire(unittest.TestCase):

    def test_wire(self):
	    w = wire()
	    self.assertEqual(w.v(), 0, "power initialized at false")
	    w.v(1)
	    self.assertEqual(w.v(), 1, "power set to true")
	    w.v(0)
	    self.assertEqual(w.v(), 0, "power set to false")

    def test_bus(self):
        b = bus()
        self.assertEqual(b.v(), 0b00000000, "v() failed")
        b.v(0b1010)
        self.assertEqual(b.v(), 0b1010, "v() failed")
        w = b.wire(1)
        self.assertEqual(w.v(), 1, "v failed")
        w = b.wire(0)
        self.assertEqual(w.v(), 0, "v failed")


if __name__ == '__main__':
    unittest.main()