import unittest
from hdl import *


class TestDecoder(unittest.TestCase):

    def test_decoder(self):
        for n in range(2, 4):
            n2 = 1 << n
            bi = bus("", n)
            bo = bus("", n2)
            decoder(bi, bo)

            for x in range(0, n2):
                print(n, n2)
                bi.v(x)
                res = 1 << x
                self.assertEqual(bo.v(), res, "decoder({:>0{w1}b})={:0>{w2}b}".format(x, res, w1=n, w2=n2))


if __name__ == '__main__':
    unittest.main()