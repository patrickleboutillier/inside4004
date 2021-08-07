import hdl


class wire():
    def __init__(self, v=None, _bus=None, bit=0):
        self._bus = hdl.bus(1, v) if _bus is None else _bus
        self._bit = bit

    def v(self, v=None):
        if v != None:    # set
            self._bus.bit(self._bit, v)
        else:   # get
            return self._bus.bit(self._bit)