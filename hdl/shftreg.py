from hdl import *


class shftreg(sensor):
    def __init__(self, clk, i, bo, name=""):
        sensor.__init__(self, name, clk)
        self._clk = clk
        self._i = i
        self._bo = bo

    def clk(self):
        return self._clk

    def i(self):
        return self._i

    def bo(self):
        return self._bo

    def always(self):
        if self._clk.v():
            # clk went from 0 to 1
            n = self._bo.v()
            n = (n << 1) | self._i.v()
            self._bo.v(n)        


