import unittest
from hdl import *


class TestMem(unittest.TestCase):

    def test_mem(self):
        wi = wire()
        ws = wire()
        wo = wire()
        mem(wi, ws, wo)

        self.assertEqual(wo.v(), 0, "M(i:0,s:0)=o:0, s=off, o should be initialized at 0")
        ws.v(1)
        self.assertEqual(wo.v(), 0, "M(i:0,s:1)=o:0, s=on, o should equal i")
        wi.v(1)

        self.assertEqual(wo.v(), 1, "M(i:1,s:1)=o:1, s=on, o should equal i")
        ws.v(0)
        self.assertEqual(wo.v(), 1, "M(i:1,s:0)=o:1, s=off, o still equal to i")
        wi.v(0)
        self.assertEqual(wo.v(), 1, "M(i:0,s:0)=o:1, s=off and i=off, o stays at 1")
        ws.v(1)
        self.assertEqual(wo.v(), 0, "M(i:0,s:1)=o:0, s=on, o goes to 0 since i is 0")
        ws.v(0)
        self.assertEqual(wo.v(), 0, "M(i:0,s:0)=o:0, s=off, i and o stay at 0")
        wi.v(1)
        self.assertEqual(wo.v(), 0, "M(i:1,s:0)=o:0, s=off, o stays at 0")

        # More specific cases...
        wi = wire()
        ws = wire()
        wo = wire()
        mem(wi, ws, wo)

        self.assertEqual(wo.v(), 0, "M(i:0,[0],s:0)=o:0")
        ws.v(1)
        self.assertEqual(wo.v(), 0, "M(i:0,[0],s:0)=o:0")
        ws.v(0)
        wi.v(1)
        self.assertEqual(wo.v(), 0, "M(i:0,[0],s:0)=o:0")

        wi = wire()
        ws = wire()
        wo = wire()
        mem(wi, ws, wo)

        self.assertEqual(wo.v(), 0, "M(i:0,[0],s:0)=o:0")
        ws.v(1)
        self.assertEqual(wo.v(), 0, "M(i:0,[0],s:0)=o:0")

        wi.v(1)
        ws.v(0)
        self.assertEqual(wo.v(), 1, "M(i:1,[1],s:0)=o:1")


if __name__ == '__main__':
    unittest.main()