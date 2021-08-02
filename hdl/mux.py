from hdl import *


class mux(sensor):
    # len(bi) must be equal to 2**len(bsel)
    def __init__(self, bi, bsel, o, name=""):
        sensor.__init__(self, name, bi, bsel)
        self._bi = bi
        self._bsel = bsel
        self._o = o

    def bi(self):
        return self._bi

    def bsel(self):
        return self._bsel

    def o(self):
        return self._o

    def always(self):
        idx = self._bsel.v()
        self._o.v(self._bi.wire(idx).v())

