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

        # a, b = wire(), wire()
        # a.connect(b)
        # a.v(1)
        # self.assertEqual(b.v(), 1, "connected wires transmit values")
        # b.v(0)
        # self.assertEqual(a.v(), 0, "connected wires transmit values")

        # a.connect(wire.GND)
        # a.v(1)
        # self.assertEqual(wire.GND.v(), 0, "constant wires cannot be changed")        

if __name__ == '__main__':
    unittest.main()