from hdl import *


active_timing = None


class timing(sensor):
    def __init__(self, ph1, ph2, sync):
        global active_timing
        active_timing = self
        
        self.ph1 = ph1
        self.ph2 = ph2
        self.phx = ph1._bus
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
            # A new step starts when ph1 goes high
            self.slave = self.master
            if self.gen_sync:
                if self.slave == 7:
                    self.sync.v = 1
                elif self.slave == 0:
                    self.sync.v = 0
        elif self.phx._v == 0b01:
            if self.gen_sync:
                self.master = (self.master + 1) % 8
            else:
                if self.sync.v:
                    self.master = 0
                else:
                    self.master += 1

        for f in self.dispatch[self.slave][self.phase]:
            f()


# Decorators
def A1ph1(f):
    active_timing.dispatch[0][0].append(f)

def A1ph2(f):
    active_timing.dispatch[0][2].append(f)

def A2ph1(f):
    active_timing.dispatch[1][0].append(f)

def A2ph2(f):
    active_timing.dispatch[1][2].append(f)

def A3ph1(f):
    active_timing.dispatch[2][0].append(f)

def A3ph2(f):
    active_timing.dispatch[2][2].append(f)

def M1ph1(f):
    active_timing.dispatch[3][0].append(f)

def M1ph2(f):
    active_timing.dispatch[3][2].append(f)

def M2ph1(f):
    active_timing.dispatch[4][0].append(f)

def M2ph2(f):
    active_timing.dispatch[4][2].append(f)

def X1ph1(f):
    active_timing.dispatch[5][0].append(f)

def X1ph2(f):
    active_timing.dispatch[5][2].append(f)

def X2pre(f):
    active_timing.dispatch[5][3].append(f)

def X2ph1(f):
    active_timing.dispatch[6][0].append(f)

def X2ph2(f):
    active_timing.dispatch[6][2].append(f)

def X3pre(f):
    active_timing.dispatch[6][3].append(f)

def X3ph1(f):
    active_timing.dispatch[7][0].append(f)

def X3ph2(f):
    active_timing.dispatch[7][2].append(f)