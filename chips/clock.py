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
            if t.gen_sync:
                t.master = (t.master + 1) & 0b111
            else:
                if t.sync.v:
                    t.master = 0
                else:
                    t.master += 1
            for f in t.dispatch[t.slave][1]:
                f()      
        for t in self.timings:
            for f in t.dispatch[t.slave][2]:
                f()      
        for t in self.timings:
            if t.gen_sync:
                if t.slave == 6:
                    t.sync.v = 1
                elif t.slave == 7:
                    t.sync.v = 0
            for f in t.dispatch[t.slave][3]:
                f()                        