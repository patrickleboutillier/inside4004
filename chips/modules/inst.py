from chips.modules.timing import *
import chips.modules.instx as x
from hdl import *


# This class implements the instruction processing part of the CPU. It contains the DC (double cycle) flip-flop, the condition register.
# as well as the OPA and OPR register, which are populated via the data bus.
# It is also responsible for everything that happens during M1 and M2 in the CPU.


class inst:
    def __init__(self, cpu, scratch, timing, data, cm_rom, cm_ram):
        self.x = x.instx(self)
        self.cpu = cpu
        self.scratch = scratch
        self.data = data
        self.ram_bank = 1
        self.cm_rom = cm_rom
        self.cm_ram = cm_ram
        self.dcff = 0
        self.sc = 1
        self.cond = 0
        self.opr = 0
        self.opa = 0

        self.timing = timing

        @M1ph2
        def _():
            if (self.fim() or self.fin()) and self.dcff:
                self.scratch.setRegPairH()
            elif (self.jun() or self.jms()) and self.dcff:
                self.cpu.addr.setPM()
            elif (self.jcn() or self.isz()) and self.dcff:
                if self.cond:
                    self.cpu.addr.setPM()
            else:
                self.opr = self.data.v

        @M2ph1
        def _():
            # This slogan turned off at X1ph1 below
            if self.opr == 0b1110:
                self.cm_ram.v(self.ram_bank)

        @M2ph2
        def _():
            if (self.fim() or self.fin()) and self.dcff:
                self.scratch.setRegPairL()
            elif (self.jun() or self.jms()) and self.dcff:
                self.cpu.addr.setPL()
            elif (self.jcn() or self.isz()) and self.dcff:
                if self.cond:
                    self.cpu.addr.setPL()
            else:
                self.opa = self.data.v

        self.registerX()


    def jcn(self):
        return self.opr == 0b0001

    # C1 = 0 Do not invert jump condition
    # C1 = 1 Invert jump condition
    # C2 = 1 Jump if the accumulator content is zero
    # C3 = 1 Jump if the carry/link content is 1
    # C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
    def setJCNCond(self):
        z = self.cpu.alu.accZero()
        c = self.cpu.alu.carryOne()
        t = self.cpu.testZero()

        invert = (self.opa & 0b1000) >> 3
        (zero, cy, test) = (self.opa & 0b0100, self.opa & 0b0010, self.opa & 0b0001)
        self.cond = 0
        if zero and (z ^ invert):
            self.cond = 1
        elif cy and (c ^ invert):
            self.cond = 1
        elif test and (t ^ invert):
            self.cond = 1

    def setRAMBank(self):
        if self.cpu.alu.acc_out & 0b0111 == 0:
            self.ram_bank = 1
        elif self.cpu.alu.acc_out & 0b0111 == 1:
            self.ram_bank = 2
        elif self.cpu.alu.acc_out & 0b0111 == 2:
            self.ram_bank = 4
        elif self.cpu.alu.acc_out & 0b0111 == 3:
            self.ram_bank = 3
        elif self.cpu.alu.acc_out & 0b0111 == 4:
            self.ram_bank = 8
        elif self.cpu.alu.acc_out & 0b0111 == 5:
            self.ram_bank = 10
        elif self.cpu.alu.acc_out & 0b0111 == 6:
            self.ram_bank = 12
        elif self.cpu.alu.acc_out & 0b0111 == 7:
            self.ram_bank = 14

    def fim(self):
        return self.opr == 0b0010 and not self.opa & 0b0001

    def src(self):
        return self.opr == 0b0010 and self.opa & 0b0001

    def fin(self):
        return self.opr == 0b0011 and not self.opa & 0b0001

    def jun(self):
        return self.opr == 0b0100

    def jms(self):
        return self.opr == 0b0101

    def isz(self):
        return self.opr == 0b0111

    def io(self):
        return self.opr == 0b1110

    def iow(self):
        return self.io() and (self.opa >> 3) == 0

    def ior(self):
        return self.io() and (self.opa >> 3) == 1

    def ld(self):
        return self.opr == 0b1010

    def ope(self):
        return self.opr == 0b1111

    def tcs(self):
        return self.opr == 0b1111 and self.opa == 0b1001    

    def daa(self):
        return self.opr == 0b1111 and self.opa == 0b1011
   
    def kbp(self):
        return self.opr == 0b1111 and self.opa == 0b1100   

    def registerX(self):
        def dispatch(x, n):
            f = self.x.dispatch[self.opr][self.opa][x][n]
            if f is not None:
                f()

        @X1ph1
        def _():
            if self.opr == 0b1110:
                self.cm_ram.v(0) 
            dispatch(5, 0)

        @A1ph1
        def _():
            dispatch(0, 0)

        @X1ph2
        def _():
            dispatch(5, 2)

        @X2pre
        def _():
            dispatch(5, 3)

        @X2ph1
        def _():
            dispatch(6, 0)

        @X2ph2
        def _():
            dispatch(6, 2)

        @X3pre
        def _():
            dispatch(6, 3)

        @X3ph1
        def _():
            dispatch(7, 0)

        @X3ph2
        def _():
            dispatch(7, 2)
            

    def dump(self):
        print("OPR/OPA:{:04b}/{:04b}  DC:{}  CM-RAM:{:04b}".format(self.opr, self.opa, self.dcff, self.ram_bank), end = '')

