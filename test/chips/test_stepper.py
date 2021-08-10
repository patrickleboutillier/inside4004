import unittest
from hdl import *
import chips.clock as clock, chips.modules.stepper as stepper


class TestStepper(unittest.TestCase):

    def test_stepper(self):
        c = clock.clock()
        s = stepper.stepper(c.ph1(), c.ph2())

        # At power on
        self.assertEqual(s.step(), 0)       
        # start
        c.tick(4)
        self.assertEqual(s.step(), 0)   
        c.tick(4)
        self.assertEqual(s.step(), 1)   
        c.tick(4)
        self.assertEqual(s.step(), 2)   
        c.tick(4)
        self.assertEqual(s.step(), 3)   
        c.tick(4)
        self.assertEqual(s.step(), 4)   
        c.tick(4)
        self.assertEqual(s.step(), 5)   
        c.tick(4)
        self.assertEqual(s.step(), 6)   
        c.tick(4)
        self.assertEqual(s.step(), 7)
        # repeat   
        c.tick(4)
        self.assertEqual(s.step(), 0)   
        c.tick(4)
        self.assertEqual(s.step(), 1)   
        c.tick(4)
        self.assertEqual(s.step(), 2)   
        c.tick(4)
        self.assertEqual(s.step(), 3)   
        c.tick(4)
        self.assertEqual(s.step(), 4)   
        c.tick(4)
        self.assertEqual(s.step(), 5)   
        c.tick(4)
        self.assertEqual(s.step(), 6)   
        c.tick(4)
        self.assertEqual(s.step(), 7)

if __name__ == '__main__':
    unittest.main()