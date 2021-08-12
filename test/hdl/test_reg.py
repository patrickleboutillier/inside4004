import unittest
from hdl import *


class TestReg(unittest.TestCase):

    def test_reg(self):
        # Basic test for Register circuit.
        bin = bus()
        bout = bus()
        ws = wire()
        reg(bin, ws, bout)

        # Let input from the input bus into the register and turn on the enabler
        ws.v(1)
        self.assertEqual(bout._v, 0b0000, "R(i:0000,s:1)=o:0000, s=on, initial state, output should be 0")
        ws.v(0)
        bin.wire(3).v(1)
        self.assertEqual(bout._v, 0b0000, "R(i:1000,s:0)=o:0000, s=off, since s=off, output should be 0")
        ws.v(1)
        self.assertEqual(bout._v, 0b1000, "R(i:1000,s:1)=o:1000, s=on, since s=on, i should flow to o")
        ws.v(0)
        bin.wire(3).v(0)
        ws.v(1)
        self.assertEqual(bout._v, 0b00000000, "R(i:00000000,s:1)=o:00000000, s=on, i flows, so 0")


if __name__ == '__main__':
    unittest.main()