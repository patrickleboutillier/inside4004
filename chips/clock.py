from hdl import *


# This class implements the 2-phase clock used by the entire MCS-4 system:
#
#        __              __              __              __
# clk1: |  |____________|  |____________|  |____________|  |____________
#                __              __              __              __
# clk2: ________|  |____________|  |____________|  |____________|  |____
#
#       |--   cycle   --|--   cycle   --|--   cycle   --|--   cycle   --|


class clock:
    def __init__(self):
        self.timings = []

        
    def tick(self):
        for t in self.timings:
            # A new step starts when clk1 goes high
            t.slave = t.master
            for f in t.dispatch[t.slave][0]:
                f() 
        for t in self.timings:
            t.tick1()
            for f in t.dispatch[t.slave][1]:
                f()      
        for t in self.timings:
            t.tick2()
            for f in t.dispatch[t.slave][2]:
                f()      
        for t in self.timings:
            t.tick3()
            for f in t.dispatch[t.slave][3]:
                f()                        