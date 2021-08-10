import unittest
from hdl import *
import chips.clock as clock, chips.modules.timing as timing


class Testtiming(unittest.TestCase):
    def step(self, timing): # returns 0 -> 7
        o = timing.output.v()
        step = -1
        while (o > 0):
            step += 1
            o >>= 1
        return step

    def test_timing(self):
        c = clock.clock()
        sync = wire()
        t = timing.timing(c.ph1, c.ph2, sync)

        # At power on
        self.assertEqual(self.step(t), 0)       
        # start
        c.tick(4)
        self.assertEqual(self.step(t), 0)   
        c.tick(4)
        self.assertEqual(self.step(t), 1)   
        c.tick(4)
        self.assertEqual(self.step(t), 2)   
        c.tick(4)
        self.assertEqual(self.step(t), 3)   
        c.tick(4)
        self.assertEqual(self.step(t), 4)   
        c.tick(4)
        self.assertEqual(self.step(t), 5)   
        c.tick(4)
        self.assertEqual(self.step(t), 6)   
        c.tick(4)
        self.assertEqual(self.step(t), 7)
        # repeat   
        c.tick(4)
        self.assertEqual(self.step(t), 0)   
        c.tick(4)
        self.assertEqual(self.step(t), 1)   
        c.tick(4)
        self.assertEqual(self.step(t), 2)   
        c.tick(4)
        self.assertEqual(self.step(t), 3)   
        c.tick(4)
        self.assertEqual(self.step(t), 4)   
        c.tick(4)
        self.assertEqual(self.step(t), 5)   
        c.tick(4)
        self.assertEqual(self.step(t), 6)   
        c.tick(4)
        self.assertEqual(self.step(t), 7)

if __name__ == '__main__':
    unittest.main()