import hdl
import hdl.uart as uart


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
    def __init__(self, v, id=None, read=False):
        self.id = id
        self._v = v
        self.read = read

    @property
    def v(self):
        if self.id is not None and uart.port is not None and self.read:
            return uart.wireRead(self.id)
        else:
            return self._v

    @v.setter
    def v(self, v):
        self._v = v
        if self.id is not None and uart.port is not None:
            if v:
                uart.wireOn(self.id)
            else:
                uart.wireOff(self.id)
