from hdl import *


class decoder(sensor):
    # len(bo) must be equal to 2**len(bi)
    def __init__(self, bi, bo, name=""):
        sensor.__init__(self, name, bi)
        self._bi = bi
        self._bo = bo

    def bi(self):
        return self._bi

    def bo(self):
        return self._bo

    def always(self):
        n = self._bi.v()
        self._bo.v(1 << n)

