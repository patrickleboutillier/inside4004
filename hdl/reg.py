from hdl import *


class reg():
    def __init__(self, bi, s, bo, name=""):
        sensor.__init__(self, name, bi, s)
        self._bi = bi
        self._s = s
        self._bo = bo
        # Problems with shift registers
        # for i in range(bo.len()-1, -1, -1):
        #     mem(bi.wire(i), self._s, bo.wire(i), "{}.mem[{}]".format(name, i))

    def bi(self):
        return self._bi

    def s(self):
        return self._s

    def bo(self):
        return self._bo

    def always(self):
        if self._s.v():
            self._bo.v(self._bi.v())
