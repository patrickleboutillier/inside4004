from hdl import *


class mem(sensor):
    def __init__(self, i, s, o, name=""):
        sensor.__init__(self, name, i, s, o)
        self._i = i
        self._s = s
        self._o = o

    def i(self):
        return self._i

    def s(self):
        return self._s

    def o(self):
        return self._o

    def always(self):
        if self._s.v():
            self._o.v(self._i.v())
