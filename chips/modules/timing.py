from hdl import *


class timing(sensor):
    def __init__(self, ph1, ph2, sync, *signals):
        self.ph1 = ph1
        self.ph2 = ph2
        self.phx = ph1._bus
        sensor.__init__(self, self.ph1, self.ph2)
        for s in signals:
            self.addSignal(s)
        self.step = 0
        self.output = bus(8, 1)
        self.a1 = self.output.wire(0)
        self.a2 = self.output.wire(1)
        self.a3 = self.output.wire(2)
        self.m1 = self.output.wire(3)
        self.m2 = self.output.wire(4)
        self.x1 = self.output.wire(5)
        self.x2 = self.output.wire(6)
        self.x3 = self.output.wire(7)

        self.dispatch = []
        for _ in range(8):
            self.dispatch.append([[], [], [], []])


    def always(self, signal):
        if signal is self.ph2 and self.phx._v == 0:
            # A new step starts when ph2 goes low
            self.step = (self.step + 1) % 8
            self.output.v(1 << self.step)

        if self.phx._v:
            for (f, ctx) in self.dispatch[self.step][self.phx._v]:
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