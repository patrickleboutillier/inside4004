from hdl import *


class i4003(sensor):
    def __init__(self, clock, data_in, enable, name=""):
        sensor.__init__(self, clock)
        self._name = name
        self._clock = clock
        self._data_in = data_in
        self._parallel_out = bus(n=10)
        self._serial_out = wire()
        self._enable = enable
        self._reg = 0
 

    def parallel_out(self):
        return self._parallel_out

    def serial_out(self):
        return self._serial_out

    def always(self):
        if self._clock.v():
            # clk went from 0 to 1
            o = self._reg >> 9
            self._reg = ((self._reg << 1) | self._data_in.v()) & 0x3FF
            # print("{} ({},{:010b})".format(self._data_in.v(), o, self._reg))
            self._serial_out.v(o)
            if self._enable.v():
                self._parallel_out.v(self._reg)
            else:
                self._parallel_out.v(0)

    def dump(self):
        print("{}SR: CLK:{:b} DATA:{:b} OUT:{:010b} E:{:b} ".format(self._name, self._clock.v(), self._data_in.v(), 
            self._parallel_out.v(), self._enable.v()), end = "")
