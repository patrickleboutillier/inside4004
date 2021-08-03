import unittest
from hdl import *


class TestShftReg(unittest.TestCase):

    def test_shftreg(self):
        # Basic test for Shift Register circuit.
        clk = wire()
        i = wire()
        bo = bus("", 10)
        o = wire()
        shftreg(clk, i, bo, o)

        self.assertEqual(bo.v(), 0b0000000000)
        i.v(1)
        clk.v(1)
        self.assertEqual(bo.v(), 0b0000000001)
        clk.v(0)
        self.assertEqual(bo.v(), 0b0000000001)
        i.v(0)
        self.assertEqual(bo.v(), 0b0000000001)
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0000000010)       
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0000000100)       
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0000001000)       
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0000010000)       
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0000100000)       
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0001000000)    
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0010000000)       
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0100000000)       
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b1000000000)
        self.assertEqual(o.v(), 0)
        clk.v(1) ; clk.v(0)
        self.assertEqual(bo.v(), 0b0000000000)
        self.assertEqual(o.v(), 1)

        i.v(1) ; clk.v(1) ; clk.v(0) ; i.v(0)
        self.assertEqual(bo.v(), 0b0000000001)
        self.assertEqual(o.v(), 0)

if __name__ == '__main__':
    unittest.main()