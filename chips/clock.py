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


cycle = 0

class clock():
    def __init__(self):
        self.phx = pbus(2)
        self.clk1 = self.phx.pwire(1)
        self.clk2 = self.phx.pwire(0)
        self.sclk1 = wire(0, 0b0010)
        self.sclk2 = wire(0, 0b0011)
        self.n = 0
        self.qperiod = 0.000100
        print("qperiod", self.qperiod)


    def run(self, nb=1):
        while True:
            self.sclk1.v = 1
            self.sclk1.v = 0 
            self.sclk2.v = 1
            self.sclk2.v = 0
    