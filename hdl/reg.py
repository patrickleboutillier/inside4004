from hdl import *


class reg(sensor):
    def __init__(self, bi, s, bo):
        sensor.__init__(self, bi, s)
        self._bi = bi
        self._s = s
        self._bo = bo
        if bi.v() != 0:
            s.v(1)
            s.v(0)


    def bi(self):
        return self._bi

    def s(self):
        return self._s

    def bo(self):
        return self._bo

    @property
    def v(self):
        return self._bo._v

    def always(self, signal):
        if self._s.v():
            self._bo.v(self._bi.v())
