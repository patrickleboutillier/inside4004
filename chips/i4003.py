from hdl import *


class i4003(sensor):
    def __init__(self, name="", clock=None, data_in=None):
        self._tmp_out = bus(n=10)
        sensor.__init__(self, name, self._tmp_out)
        self._clock = wire() if clock is None else clock
        self._data_in = wire() if data_in is None else data_in
        self._parallel_out = bus(n=10)
        self._serial_out = wire()
        self._enable = wire()
        self._reg = shftreg(self._clock, self._data_in, self._tmp_out, self._serial_out, self._name)

    def clock(self):
        return self._clock

    def data_in(self):
        return self._data_in

    def parallel_out(self):
        return self._parallel_out

    def serial_out(self):
        return self._serial_out

    def enable(self):
        return self._enable

    def always(self):
        if self._enable.v():
            self._parallel_out.v(self._tmp_out.v())
        else:
            self._parallel_out.v(0)

    def dump(self):
        print("{}SR: CLK:{:b} DATA:{:b} OUT:{:010b} E:{:b} ".format(self._name, self._clock.v(), self._data_in.v(), 
            self._parallel_out.v(), self._enable.v()), end = "")
