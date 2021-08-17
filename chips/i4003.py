from hdl import *


# This class implements the behaviour of the 4003 shift register chip.


class i4003(sensor):
    def __init__(self, clock, data_in, enable, name=""):
        sensor.__init__(self, clock)
        self.name = name                # The chip name, for dump info
        self.clock = clock              # The clock that triggers a shift
        self.data_in = data_in          # The data_in wire
        self.parallel_out = bus(n=10)   # The parallel out bus
        self.serial_out = wire()        # The serial out wire, to chain multiple 4003s together
        self.enable = enable            # The enable wire (always on in our case)
        self.reg = 0                    # The internal register that stores the current value


    def always(self, signal):
        if self.clock.v():
            # clock went from 0 to 1, we shift
            o = self.reg >> 9
            self.reg = ((self.reg << 1) | self.data_in.v()) & 0x3FF
            self.serial_out.v(o)
            if self.enable.v():
                self.parallel_out.v(self.reg)
            else:
                self.parallel_out.v(0)

    def dump(self):
        print("{}SR: CLK:{:b} DATA:{:b} OUT:{:010b} E:{:b} ".format(self.name, self.clock.v(), self.data_in.v(), 
            self.parallel_out._v, self.enable.v()), end = "")
