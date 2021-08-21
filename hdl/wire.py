import hdl


class pwire():
    def __init__(self, v=0, bus=None, bit=0):
        self._bus = hdl.pbus(1, v) if bus is None else bus
        self._bit = bit

    @property
    def v(self):
        return (self._bus._v >> self._bit) & 1    

    @v.setter
    def v(self, v):
        v = (self._bus._v & ~(1 << self._bit)) | v << self._bit
        if self._bus._v != v:
            self._bus.v(v)


class wire():
    def __init__(self, v=0):
        self.v = v