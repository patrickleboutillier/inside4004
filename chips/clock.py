from hdl import *
import time


# This class implements the 2-phase clock used by the entire MCS-4 system:
#
#        __              __              __              __
# clk1: |  |____________|  |____________|  |____________|  |____________
#                __              __              __              __
# clk2: ________|  |____________|  |____________|  |____________|  |____
#
#       |--   cycle   --|--   cycle   --|--   cycle   --|--   cycle   --|


class clock():
    def __init__(self):
        self.phx = pbus(2)
        self.clk1 = self.phx.pwire(1)
        self.clk2 = self.phx.pwire(0)
        self.sclk1 = wire(0, 0b0010)
        self.sclk2 = wire(0, 0b0011)
        self.n = 0
        self.qperiod = 0.00005
        print("qperiod", self.qperiod)


    def tick(self, nb=1):
        for _ in range(nb):
            start = time.perf_counter()

            if self.n == 0:
                self.sclk1.v = 1
                self.phx.v(0b10)
            elif self.n == 1:
                self.sclk1.v = 0
                self.phx.v(0b00)
            elif self.n == 2:
                self.sclk2.v = 1
                self.phx.v(0b01)
            else:   # n == 3
                self.sclk2.v = 0
                self.phx.v(0b00)
            self.n = (self.n + 1) % 4

            dur = time.perf_counter() - start
            if dur < self.qperiod:
                time.sleep(self.qperiod - dur) 