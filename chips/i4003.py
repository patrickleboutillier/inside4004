from hdl import *


class i4003:
    def __init__(self, name=""):
        self._tmp_out = bus(n=10)
        sensor.__init__(self, name, self._tmp_out)
        self._clock = wire()
        self._data_in = wire()
        self._parallel_out = bus(n=10)
        self._serial_out = wire()
        self._enable = wire()
        self._reg = shftreg(self._clock, self._data_in, self._tmp_out)
        # Connect data_in to serial_out to allow daisy-chaining.
        self._data_in.connect(self._serial_out)

    def clock(self):
        return self._clock

    def data_in(self):
        return self._data_in

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
