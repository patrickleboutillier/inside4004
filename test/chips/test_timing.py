import unittest
from hdl import *
import chips.clock as clock, chips.modules.timing as timing


class Testtiming(unittest.TestCase):

    def test_timing(self):
        c = clock.clock()
        sync = wire()
        t = timing.timing(c.ph1, c.ph2, sync)

        # At power on
        self.assertEqual(t.step, 0)       
        # start
        c.tick(4)
        self.assertEqual(t.step, 0)   
        c.tick(4)
        self.assertEqual(t.step, 1)   
        c.tick(4)
        self.assertEqual(t.step, 2)   
        c.tick(4)
        self.assertEqual(t.step, 3)   
        c.tick(4)
        self.assertEqual(t.step, 4)   
        c.tick(4)
        self.assertEqual(t.step, 5)   
        c.tick(4)
        self.assertEqual(t.step, 6)   
        c.tick(4)
        self.assertEqual(t.step, 7)
        # repeat   
        c.tick(4)
        self.assertEqual(t.step, 0)   
        c.tick(4)
        self.assertEqual(t.step, 1)   
        c.tick(4)
        self.assertEqual(t.step, 2)   
        c.tick(4)
        self.assertEqual(t.step, 3)   
        c.tick(4)
        self.assertEqual(t.step, 4)   
        c.tick(4)
        self.assertEqual(t.step, 5)   
        c.tick(4)
        self.assertEqual(t.step, 6)   
        c.tick(4)
        self.assertEqual(t.step, 7)

if __name__ == '__main__':
    unittest.main()