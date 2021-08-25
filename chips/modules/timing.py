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
def A12clk1(f):
    active_timing.dispatch[0][0].append(f)
    return f
A12 = A12clk1

def A12clk2(f):
    active_timing.dispatch[0][2].append(f)
    return f

def A21(f):
    active_timing.dispatch[0][3].append(f)
    return f

def A22clk1(f):
    active_timing.dispatch[1][0].append(f)
    return f
A22 = A22clk1

def A22clk2(f):
    active_timing.dispatch[1][2].append(f)
    return f

def A31(f):
    active_timing.dispatch[1][3].append(f)
    return f

def A32clk1(f):
    active_timing.dispatch[2][0].append(f)
    return f
A32 = A32clk1

def A32clk2(f):
    active_timing.dispatch[2][2].append(f)
    return f

def M12clk1(f):
    active_timing.dispatch[3][0].append(f)
    return f
M12 = M12clk1

def M12clk2(f):
    active_timing.dispatch[3][2].append(f)
    return f

def M22clk1(f):
    active_timing.dispatch[4][0].append(f)
    return f
M22 = M22clk1

def M22clk2(f):
    active_timing.dispatch[4][2].append(f)
    return f

def X12clk1(f):
    active_timing.dispatch[5][0].append(f)
    return f
X12 = X12clk1

def X12clk2(f):
    active_timing.dispatch[5][2].append(f)
    return f

def X21(f):
    active_timing.dispatch[5][3].append(f)
    return f

def X22clk1(f):
    active_timing.dispatch[6][0].append(f)
    return f
X22 = X22clk1

def X22clk2(f):
    active_timing.dispatch[6][2].append(f)
    return f

def X31(f):
    active_timing.dispatch[6][3].append(f)
    return f

def X32clk1(f):
    active_timing.dispatch[7][0].append(f)
    return f
X32 = X32clk1

def X32clk2(f):
    active_timing.dispatch[7][2].append(f)
    return f

def A11(f):
    active_timing.dispatch[7][3].append(f)
    return f