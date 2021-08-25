import unittest
from hdl import *


class TestWire(unittest.TestCase):

    def test_pwire(self):
        w = pwire()
        self.assertEqual(w.v, 0, "power initialized at false")
        w.v = 1
        self.assertEqual(w.v, 1, "power set to true")
        w.v = 0
        self.assertEqual(w.v, 0, "power set to false")    

if __name__ == '__main__':
    unittest.main()