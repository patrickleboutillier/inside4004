import unittest
from hdl import *
import chips.clock as clock, chips.modules.timing as timing


class TestTiming(unittest.TestCase):

    def test_timing(self):
        # gen_sync mode
        c = clock.clock()
        t = timing.timing(c.ph1, c.ph2, None)
        # At power on
        self.assertEqual(t.output._v, 0)
        # start
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1)
        self.assertEqual(t.output._v, 0b00000100) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00001000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00010000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00100000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b01000000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b10000000) 
        # repeat
        c.tick(4)
        self.assertEqual(t.output._v, 0b00000001)
        c.tick(4)
        self.assertEqual(t.output._v, 0b00000010)
        c.tick(4)
        self.assertEqual(t.output._v, 0b00000100) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00001000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00010000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00100000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b01000000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b10000000) 

        # ! gen_sync mode
        c = clock.clock()
        sync = wire()
        t = timing.timing(c.ph1, c.ph2, sync)
        # At power on
        self.assertEqual(t.output._v, 0)
        # start
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000001)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1) ; self.assertEqual(t.output._v, 0b00000010)
        c.tick(1)
        self.assertEqual(t.output._v, 0b00000100) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00001000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00010000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00100000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b01000000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b10000000)
        sync.v(1)
        c.tick(4)
        self.assertEqual(t.output._v, 0b00000001)
        sync.v(0)
        # repeat
        c.tick(4)
        self.assertEqual(t.output._v, 0b00000010)
        c.tick(4)
        self.assertEqual(t.output._v, 0b00000100) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00001000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00010000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b00100000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b01000000) 
        c.tick(4)
        self.assertEqual(t.output._v, 0b10000000) 


if __name__ == '__main__':
    unittest.main()