import chips.modules.instx as x
from hdl import *


class inst:
    def __init__(self, cpu, scratch, timing, data, cm_rom, cm_ram):
        self.x = x.instx(self)
        self.timing = timing
        self.cpu = cpu
        self.scratch = scratch
        self.data = data
        self.ram_bank = 1
        self.cm_rom = cm_rom
        self.cm_ram = cm_ram
        self.dc = 0
        self.cond = 0
        self.opr = 0
        self.opa = 0

        def M1ph2(self):
            if (self.fim() or self.fin()) and self.dc:
                self.scratch.index_reg[self.opa & 0b1110] = self.data._v
            elif (self.jun() or self.jms()) and self.dc:
                self.cpu.addr.setPM(self.data._v)
            elif (self.jcn() or self.isz()) and self.dc:
                if self.cond:
                    self.cpu.addr.setPM(self.data._v)
            else:
                self.opr = self.data._v
        self.timing.whenM1ph2(M1ph2, self)

        def M2ph1(self):
            if self.opr == 0b1110:
                self.cm_ram.v(self.ram_bank)
            else:
                self.cm_ram.v(0) 
        self.timing.whenM2ph1(M2ph1, self)

        def M2ph2(self):
            if (self.fim() or self.fin()) and self.dc:
                self.scratch.index_reg[self.opa | 0b0001] = self.data._v
            elif (self.jun() or self.jms()) and self.dc:
                self.cpu.addr.setPL(self.data._v)
            elif (self.jcn() or self.isz()) and self.dc:
                if self.cond:
                    self.cpu.addr.setPL(self.data._v)
            else:
                self.opa = self.data._v
        self.timing.whenM2ph2(M2ph2, self)

        def X1ph1(self):
            f = self.x.dispatch[self.opr][self.opa][x.X1][x.ph1]
            if f is not None:
                f(self)
            if self.opr == 0b1110:
                self.cm_ram.v(0) 
        self.timing.whenX1ph1(X1ph1, self)

        def X1ph2(self):
            f = self.x.dispatch[self.opr][self.opa][x.X1][x.ph2]
            if f is not None:
                f(self)
        self.timing.whenX1ph2(X1ph2, self)

        def X2ph1(self):
            f = self.x.dispatch[self.opr][self.opa][x.X2][x.ph1]
            if f is not None:
                f(self)
        self.timing.whenX2ph1(X2ph1, self)

        def X2ph2(self):
            f = self.x.dispatch[self.opr][self.opa][x.X2][x.ph2]
            if f is not None:
                f(self)
        self.timing.whenX2ph2(X2ph2, self)

        def X3ph1(self):
            f = self.x.dispatch[self.opr][self.opa][x.X3][x.ph1]
            if f is not None:
                f(self)
        self.timing.whenX3ph1(X3ph1, self)

        def X3ph2(self):
            f = self.x.dispatch[self.opr][self.opa][x.X3][x.ph2]
            if f is not None:
                f(self)
        self.timing.whenX3ph2(X3ph2, self)


    def nop(self):
        return self.opr == 0b0000 and self.opa == 0b0000

    def hlt(self):
        return self.opr == 0b0000 and self.opa == 0b0001

    def err(self):
        return self.opr == 0b0000 and self.opa == 0b0010

    def jcn(self):
        return self.opr == 0b0001

    def setJCNCond(self, z, c, t):
        invert = (self.opa & 0b1000) >> 3
        (zero, cy, test) = (self.opa & 0b0100, self.opa & 0b0010, self.opa & 0b0001)
        self.cond = 0
        if zero and (z ^ invert):
            self.cond = 1
        elif cy and (c ^ invert):
            self.cond = 1
        elif test and (t ^ invert):
            self.cond = 1

    def fim(self):
        return self.opr == 0b0010 and not self.opa & 0b0001

    def src(self):
        return self.opr == 0b0010 and self.opa & 0b0001

    def fin(self):
        return self.opr == 0b0011 and not self.opa & 0b0001

    def jin(self):
        return self.opr == 0b0011 and self.opa & 0b0001

    def jun(self):
        return self.opr == 0b0100

    def jms(self):
        return self.opr == 0b0101

    def inc(self):
        return self.opr == 0b0110

    def isz(self):
        return self.opr == 0b0111

    def setISZCond(self, r):
        self.cond = (r != 0)
