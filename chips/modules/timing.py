from hdl import *


class timing(sensor):
    def __init__(self, ph1, ph2, sync):
        sensor.__init__(self, ph2)
        self.ph1 = ph1
        self.ph2 = ph2
        self.phx = ph1._bus
        self.output = bus(8, 1)
        self.a1 = self.output.wire(0)
        self.a2 = self.output.wire(1)
        self.a3 = self.output.wire(2)
        self.m1 = self.output.wire(3)
        self.m2 = self.output.wire(4)
        self.x1 = self.output.wire(5)
        self.x2 = self.output.wire(6)
        self.x3 = self.output.wire(7)  

    def always(self):
        if self.ph2.v() == 0:
            # A new step starts when ph2 goes low
            o = self.output.v()
            step = self.output.v() << 1
            if step > 128:
                step = 1
            # print("STEP {} (PH1:{}, PH2:{}) for {}".format(step, self.ph1(), self.ph2(), self))
            self.output.v(step)