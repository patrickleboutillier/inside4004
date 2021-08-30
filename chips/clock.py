from hdl import *


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
        self.n = 0
        self.timings = []

    def tick(self):
        for _ in range(4):
            for t in self.timings:
                if self.n == 0:
                    t.tick0()
                elif self.n == 1:
                    t.tick1()
                elif self.n == 2:
                    t.tick2()
                else:   # n == 3
                    t.tick3()
                for f in t.dispatch[t.slave][self.n]:
                    f()                   
            self.n = (self.n + 1) & 0b11