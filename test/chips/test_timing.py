import unittest
from hdl import *
import chips.clock as clock, chips.modules.timing as timing


class TestTiming(unittest.TestCase):

    def test_timing(self):
        # gen_sync mode
        c = clock.clock()
        t = timing.timing(c.clk1, c.clk2, None)
        # At power on
        self.assertEqual(t.slave, 0)
        # start
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1)
        self.assertEqual(t.slave, 2) 
        c.tick(4)
        self.assertEqual(t.slave, 3) 
        c.tick(4)
        self.assertEqual(t.slave, 4) 
        c.tick(4)
        self.assertEqual(t.slave, 5) 
        c.tick(4)
        self.assertEqual(t.slave, 6) 
        c.tick(4)
        self.assertEqual(t.slave, 7) 
        # repeat
        c.tick(4)
        self.assertEqual(t.slave, 0)
        c.tick(4)
        self.assertEqual(t.slave, 1)
        c.tick(4)
        self.assertEqual(t.slave, 2) 
        c.tick(4)
        self.assertEqual(t.slave, 3) 
        c.tick(4)
        self.assertEqual(t.slave, 4) 
        c.tick(4)
        self.assertEqual(t.slave, 5) 
        c.tick(4)
        self.assertEqual(t.slave, 6) 
        c.tick(4)
        self.assertEqual(t.slave, 7) 

        # ! gen_sync mode
        c = clock.clock()
        sync = wire()
        t = timing.timing(c.clk1, c.clk2, sync)
        # At power on
        self.assertEqual(t.slave, 0)
        # start
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 0)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1) ; self.assertEqual(t.slave, 1)
        c.tick(1)
        self.assertEqual(t.slave, 2) 
        c.tick(4)
        self.assertEqual(t.slave, 3) 
        c.tick(4)
        self.assertEqual(t.slave, 4) 
        c.tick(4)
        self.assertEqual(t.slave, 5) 
        c.tick(4)
        self.assertEqual(t.slave, 6) 
        c.tick(4)
        self.assertEqual(t.slave, 7)
        sync.v = 1
        c.tick(4)
        self.assertEqual(t.slave, 0)
        sync.v = 0
        # repeat
        c.tick(4)
        self.assertEqual(t.slave, 1)
        c.tick(4)
        self.assertEqual(t.slave, 2) 
        c.tick(4)
        self.assertEqual(t.slave, 3) 
        c.tick(4)
        self.assertEqual(t.slave, 4) 
        c.tick(4)
        self.assertEqual(t.slave, 5) 
        c.tick(4)
        self.assertEqual(t.slave, 6) 
        c.tick(4)
        self.assertEqual(t.slave, 7) 


if __name__ == '__main__':
    unittest.main()