from hdl import *


class buf(sensor):
    def __init__(self, i, o):
        sensor.__init__(self, i)
        self._i = i
        self._o = o

    def i(self):
        return self._i

    def o(self):
        return self._o

    def always(self, signal):
        self._o.v(self._i.v())
