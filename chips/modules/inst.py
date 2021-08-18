from chips.modules.timing import *
import chips.modules.instx as x
from hdl import *


class inst:
    def __init__(self, cpu, scratch, timing, data, cm_rom, cm_ram):
        self.x = x.instx(self)
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

        self.timing = timing

        @M1ph2
        def _():
            if (self.fim() or self.fin()) and self.dc:
                self.scratch.setRegPairH()
            elif (self.jun() or self.jms()) and self.dc:
                self.cpu.addr.setPM()
            elif (self.jcn() or self.isz()) and self.dc:
                if self.cond:
                    self.cpu.addr.setPM()
            else:
                self.opr = self.data._v

        @M2ph1
        def _():
            if self.opr == 0b1110:
                self.cm_ram.v(self.ram_bank)

        @M2ph2
        def _():
            if (self.fim() or self.fin()) and self.dc:
                self.scratch.setRegPairL()
            elif (self.jun() or self.jms()) and self.dc:
                self.cpu.addr.setPL()
            elif (self.jcn() or self.isz()) and self.dc:
                if self.cond:
                    self.cpu.addr.setPL()
            else:
                self.opa = self.data._v

        @X1ph1
        def _():
            f = self.x.dispatch[self.opr][self.opa][x.X1][x.ph1]
            if f is not None:
                f(self)
            if self.opr == 0b1110:
                self.cm_ram.v(0) 

        @X1ph2
        def _():
            f = self.x.dispatch[self.opr][self.opa][x.X1][x.ph2]
            if f is not None:
                f(self)

        @X2ph1
        def _():
            f = self.x.dispatch[self.opr][self.opa][x.X2][x.ph1]
            if f is not None:
                f(self)

        @X2ph2
        def _():
            f = self.x.dispatch[self.opr][self.opa][x.X2][x.ph2]
            if f is not None:
                f(self)

        @X3ph1
        def _():
            f = self.x.dispatch[self.opr][self.opa][x.X3][x.ph1]
            if f is not None:
                f(self)

        @X3ph2
        def _():
            f = self.x.dispatch[self.opr][self.opa][x.X3][x.ph2]
            if f is not None:
                f(self)


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


    def dump(self):
        print("OPR/OPA:{:04b}/{:04b}  DC:{}  CM-RAM:{:04b}".format(self.opr, self.opa, self.dc, self.ram_bank), end = '')

