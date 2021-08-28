from chips.modules.timing import *
import chips.modules.instx as x
from hdl import *


# This class implements the instruction processing part of the CPU. It contains the DC (double cycle) flip-flop, the condition register.
# as well as the OPA and OPR register, which are populated via the data bus.
# It is also responsible for everything that happens during M1 and M2 in the CPU.


class inst:
    def __init__(self, cpu, timing, data, cm_rom, cm_ram):
        self.cpu = cpu
        self.data = data
        self.ram_bank = 1
        self.cm_rom = cm_rom
        self.cm_ram = cm_ram
        self.sc = 1
        self.cond = 0
        self.opr = 0
        self.opa = 0

        self.timing = timing

        @A12clk1
        def _():
            # WARNING
            if self.sc and (self.fin() or self.fim() or self.jun() or self.jms() or self.jcn() or self.isz()):
                self.sc = 0
                if self.jcn():
                    self.setJCNCond()
                if self.isz():
                    self.cond = ~self.cpu.alu.addZero() & 1
            else:
                self.sc = 1

        @M12clk2
        def _():
            if self.sc:
                self.opr = self.data.v

        @M22clk1
        def _():
            # This signal turned off at X12clk1 below
            if self.io():
                self.cm_ram.v(self.ram_bank)

        @M22clk2
        def _():
            if self.sc:
                self.opa = self.data.v

        @X12clk1
        def _():
            if self.io():
                self.cm_ram.v(0) 

        # self.registerX()


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


    def opa_odd(self):
        return self.opa & 1

    def opa_even(self):
        return not (self.opa & 1)

    def jcn(self):
        return self.opr == 0b0001
    
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

    def bbl(self):
        return self.opr == 0b1100

    def ope(self):
        return self.opr == 0b1111

    def tcs(self):
        return self.opr == 0b1111 and self.opa == 0b1001    

    def daa(self):
        return self.opr == 0b1111 and self.opa == 0b1011
   
    def kbp(self):
        return self.opr == 0b1111 and self.opa == 0b1100   

    # Inhibit program counter commit
    # inh = (jin_fin & sc) | ((jun_jms | (jcn_isz & cond)) & ~sc)
    def inh(self):
        return ((self.jin() or self.fin()) and self.sc) or (((self.jun() or self.jms()) or ((self.jcn() or self.isz()) and self.cond)) and not self.sc)