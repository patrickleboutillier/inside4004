import unittest
from hdl import *


class TestMux(unittest.TestCase):

    def test_mux(self):
        for n in range(1, 5):
            n2 = 1 << n
            bi = bus(n=n2)
            bsel = bus(n=n)
            o = wire()
            mux(bi, bsel, o)

            for x in range(n2):
                for y in range(n):
                    bi.v(x)
                    bsel.v(y)
                    self.assertEqual(o.v(), bi.wire(y).v())


if __name__ == '__main__':
    unittest.main()