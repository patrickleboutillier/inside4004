import unittest
from hdl import *
import chips.clock as clock


class TestClock(unittest.TestCase):

    def test_clock(self):
        c = clock.clock()

        # At power on
        self.assertEqual(c.clk1.v, 0)
        self.assertEqual(c.clk2.v, 0)
        # start
        c.tick()
        self.assertEqual(c.clk1.v, 1)
        self.assertEqual(c.clk2.v, 0)
        c.tick()
        self.assertEqual(c.clk1.v, 0)
        self.assertEqual(c.clk2.v, 0)
        c.tick()
        self.assertEqual(c.clk1.v, 0)
        self.assertEqual(c.clk2.v, 1)
        c.tick()
        self.assertEqual(c.clk1.v, 0)
        self.assertEqual(c.clk2.v, 0)
        # repeat
        c.tick()
        self.assertEqual(c.clk1.v, 1)
        self.assertEqual(c.clk2.v, 0)
        c.tick()
        self.assertEqual(c.clk1.v, 0)
        self.assertEqual(c.clk2.v, 0)
        c.tick()
        self.assertEqual(c.clk1.v, 0)
        self.assertEqual(c.clk2.v, 1)
        c.tick()
        self.assertEqual(c.clk1.v, 0)
        self.assertEqual(c.clk2.v, 0)


if __name__ == '__main__':
    unittest.main()