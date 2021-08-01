import unittest
from hdl import *


class TestWire(unittest.TestCase):

    def test_bus(self):
        b = bus()
        self.assertEqual(b.v(), 0b00000000, "v() failed")
        b.v(0b1010)
        self.assertEqual(b.v(), 0b1010, "v() failed")
        w = b.wire(1)
        self.assertEqual(w.v(), 1, "v failed")
        w = b.wire(0)
        self.assertEqual(w.v(), 0, "v failed")

        a, b = bus(), bus()
        a.connect(b)
        a.v(10)
        self.assertEqual(b.v(), 10, "connected buses transmit values")
        b.v(5)
        self.assertEqual(a.v(), 5, "connected buses transmit values")


if __name__ == '__main__':
    unittest.main()