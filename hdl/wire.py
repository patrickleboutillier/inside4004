import hdl


class wire():
    def __init__(self, v=0, bus=None, bit=0):
        self._bus = hdl.bus(1, v) if bus is None else bus
        self._bit = bit

    def v(self, v=None):
        if v is None:   # get
            return (self._bus._v >> self._bit) & 1 
        else:           # set
            v = (self._bus._v & ~(1 << self._bit)) | v << self._bit
            if self._bus._v != v:
                self._bus.v(v)