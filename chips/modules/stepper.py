from hdl import *


class stepper(sensor):
    def __init__(self, ph1, ph2):
        sensor.__init__(self, ph2)
        self._ph1 = ph1
        self._ph2 = ph2
        self._output = bus(8, 1) 


    def output(self):
        return self._output

    def always(self):
        if self._ph2.v() == 0:
            # A new step starts when ph2 goes low
            o = self._output.v()
            step = self._output.v() << 1
            if step > 128:
                step = 1
            # print("STEP {} (PH1:{}, PH2:{}) for {}".format(step, self.ph1(), self.ph2(), self))
            self._output.v(step)

    def ph1(self):
        return self._ph1

    def ph2(self):
        return self._ph2

    def step(self): # returns 0 -> 7, -1 before the first clock tick
        o = self._output.v()
        step = -1
        while (o > 0):
            step += 1
            o >>= 1
        return step

    def a1(self):
        return self._output.wire(0).v()

    def a2(self):
        return self._output.wire(1).v()

    def a3(self):
        return self._output.wire(2).v()

    def m1(self):
        return self._output.wire(3).v()

    def m2(self):
        return self._output.wire(4).v()