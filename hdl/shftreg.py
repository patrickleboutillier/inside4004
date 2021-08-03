from hdl import *


class shftreg(sensor):
    def __init__(self, clk, i, bo, o, name=""):
        sensor.__init__(self, name, clk)
        self._clk = clk
        self._i = i
        self._bo = bo
        self._o = o
        self._obo = bus.make([self._o] + self._bo.wires())

    def clk(self):
        return self._clk

    def i(self):
        return self._i

    def bo(self):
        return self._bo

    def o(self):
        return self._o

    def always(self):
        if self._clk.v():
            # clk went from 0 to 1
            n = self._bo.v()
            n = (n << 1) | self._i.v()
            self._obo.v(n)        


