from hdl import *


active_timing = None


class timing(sensor):
    def __init__(self, clk1, clk2, sync):
        global active_timing
        active_timing = self
        
        self.clk1 = clk1
        self.clk2 = clk2
        self.phx = clk1._bus
        self.phase = -1
        sensor.__init__(self, self.phx)
        self.slave = 0
        self.master = 0 
        if sync is None:
            self.gen_sync = True
            self.sync = wire()
        else:
            self.gen_sync = False
            self.sync = sync

        self.dispatch = []
        for _ in range(8):
            self.dispatch.append([[], [], [], []])


    def always(self, signal):
        self.phase = (self.phase + 1) % 4

        if self.phx._v == 0b10:
            # A new step starts when clk1 goes high
            self.slave = self.master
        elif self.phx._v == 0b01:
            if self.gen_sync:
                self.master = (self.master + 1) % 8
            else:
                if self.sync.v:
                    self.master = 0
                else:
                    self.master += 1
        elif self.phase == 3:
            if self.gen_sync:
                if self.slave == 6:
                    self.sync.v = 1
                elif self.slave == 7:
                    self.sync.v = 0

        for f in self.dispatch[self.slave][self.phase]:
            f()


# Decorators
def A1clk1(f):
    active_timing.dispatch[0][0].append(f)
    return f

def A1clk2(f):
    active_timing.dispatch[0][2].append(f)
    return f

def A21(f):
    active_timing.dispatch[0][3].append(f)
    return f

def A2clk1(f):
    active_timing.dispatch[1][0].append(f)
    return f

def A2clk2(f):
    active_timing.dispatch[1][2].append(f)
    return f

def A31(f):
    active_timing.dispatch[1][3].append(f)
    return f

def A3clk1(f):
    active_timing.dispatch[2][0].append(f)
    return f

def A3clk2(f):
    active_timing.dispatch[2][2].append(f)
    return f

def M1clk1(f):
    active_timing.dispatch[3][0].append(f)
    return f

def M1clk2(f):
    active_timing.dispatch[3][2].append(f)
    return f

def M2clk1(f):
    active_timing.dispatch[4][0].append(f)
    return f

def M2clk2(f):
    active_timing.dispatch[4][2].append(f)
    return f

def X1clk1(f):
    active_timing.dispatch[5][0].append(f)
    return f

def X1clk2(f):
    active_timing.dispatch[5][2].append(f)
    return f

def X21(f):
    active_timing.dispatch[5][3].append(f)
    return f

def X2clk1(f):
    active_timing.dispatch[6][0].append(f)
    return f

def X2clk2(f):
    active_timing.dispatch[6][2].append(f)
    return f

def X31(f):
    active_timing.dispatch[6][3].append(f)
    return f

def X3clk1(f):
    active_timing.dispatch[7][0].append(f)
    return f

def X3clk2(f):
    active_timing.dispatch[7][2].append(f)
    return f

def A11(f):
    active_timing.dispatch[7][3].append(f)
    return f