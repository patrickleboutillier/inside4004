from hdl import *


class inst(sensor):
    def __init__(self, cpu, timing, data):
        sensor.__init__(self, timing.phx, data)
        self.cpu = cpu
        self.timing = timing
        self.data = data 
        self.dc = 0
        self.opr = reg(self.data, wire(), bus())
        self.opa = reg(self.data, wire(), bus())


    def always(self):
        if self.timing.ph1.v():
            if self.timing.m1.v():
                if self.fim() and self.dc:
                    self.cpu.index_reg[self.opa.v & 0b1110] = self.data.v()
                else:
                    self.opr._bo.v(self.data.v())
            elif self.timing.m2.v():
                if self.fim() and self.dc:
                    self.cpu.index_reg[self.opa.v | 0b0001] = self.data.v()
                else:
                    self.opa._bo.v(self.data.v())

    def nop(self):
        return self.opr.v == 0b0000 and self.opa.v == 0b0000

    def hlt(self):
        return self.opr.v == 0b0000 and self.opa.v == 0b0001

    def err(self):
        return self.opr.v == 0b0000 and self.opa.v == 0b0010

    def jcn(self):
        return self.opr.v == 0b0001

    def fim(self):
        return self.opr.v == 0b0010 and not self.opa.v & 0b0001

    def src(self):
        return self.opr.v == 0b0010 and self.opa.v & 0b0001

    def fin(self):
        return self.opr.v == 0b0011 and not self.opa.v & 0b0001

    def jin(self):
        return self.opr.v == 0b0011 and self.opa.v & 0b0001

    def jun(self):
        return self.opr.v == 0b0100

    def jms(self):
        return self.opr.v == 0b0101

    def inc(self):
        return self.opr.v == 0b0110

    def isz(self):
        return self.opr.v == 0b0111
