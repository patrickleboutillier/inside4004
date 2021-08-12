import hdl


class wire():
    def __init__(self, v=0, bus=None, bit=0):
        self._bus = hdl.bus(1, v) if bus is None else bus
        self._bit = bit

    def v(self, v=None):
        if v is None:   # get
            return self._bus.bit(self._bit)
        else:           # set
            self._bus.bit(self._bit, v)