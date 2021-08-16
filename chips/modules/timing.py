from hdl import *


class timing(sensor):
    def __init__(self, ph1, ph2, sync):
        self.ph1 = ph1
        self.ph2 = ph2
        self.phx = ph1._bus
        sensor.__init__(self, self.phx)
        self.slave = 0
        self.master = 0 
        self.output = bus(8, 0)
        self.a1 = self.output.wire(0)
        self.a2 = self.output.wire(1)
        self.a3 = self.output.wire(2)
        self.m1 = self.output.wire(3)
        self.m2 = self.output.wire(4)
        self.x1 = self.output.wire(5)
        self.x2 = self.output.wire(6)
        self.x3 = self.output.wire(7)
        if sync is None:
            self.gen_sync = True
            self.sync = self.x3
        else:
            self.gen_sync = False
            self.sync = sync

        self.dispatch = []
        for _ in range(8):
            self.dispatch.append([[], [], [], []])


    def always(self, signal):
        if self.phx._v == 0b10:
            # A new step starts when ph1 goes high
            self.slave = self.master
            self.output.v(1 << self.slave)
        elif self.phx._v == 0b01:
            if self.gen_sync:
                self.master = (self.master + 1) % 8
            else:
                if self.sync.v():
                    self.master = 0
                else:
                    self.master += 1

        if self.phx._v:
            for (f, ctx) in self.dispatch[self.slave][self.phx._v]:
                f(ctx)        


    def whenA1ph1(self, f, context):
        self.dispatch[0][0b10].append((f, context))

    def whenA1ph2(self, f, context):
        self.dispatch[0][0b01].append((f, context))

    def whenA2ph1(self, f, context):
        self.dispatch[1][0b10].append((f, context))

    def whenA2ph2(self, f, context):
        self.dispatch[1][0b01].append((f, context))

    def whenA3ph1(self, f, context):
        self.dispatch[2][0b10].append((f, context))

    def whenA3ph2(self, f, context):
        self.dispatch[2][0b01].append((f, context))

    def whenM1ph1(self, f, context):
        self.dispatch[3][0b10].append((f, context))

    def whenM1ph2(self, f, context):
        self.dispatch[3][0b01].append((f, context))

    def whenM2ph1(self, f, context):
        self.dispatch[4][0b10].append((f, context))

    def whenM2ph2(self, f, context):
        self.dispatch[4][0b01].append((f, context))

    def whenX1ph1(self, f, context):
        self.dispatch[5][0b10].append((f, context))

    def whenX1ph2(self, f, context):
        self.dispatch[5][0b01].append((f, context))

    def whenX2ph1(self, f, context):
        self.dispatch[6][0b10].append((f, context))

    def whenX2ph2(self, f, context):
        self.dispatch[6][0b01].append((f, context))

    def whenX3ph1(self, f, context):
        self.dispatch[7][0b10].append((f, context))

    def whenX3ph2(self, f, context):
        self.dispatch[7][0b01].append((f, context))