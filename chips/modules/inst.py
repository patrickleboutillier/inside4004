from chips.modules.timing import *
from hdl import *


# This class implements the instruction processing part of the CPU. It contains the DC (double cycle) flip-flop, the condition register.
# as well as the OPA and OPR register, which are populated via the data bus.
# It is also responsible for everything that happens during M1 and M2 in the CPU.


class inst:
    def __init__(self, data, timing, condw):
        self.data = data
        self.sc = 1
        self.cond = 0
        self.condw = condw
        self.opr = 0
        self.opa = 0

        self.timing = timing

        @A12clk1
        def _():
            # WARNING: Instruction logic here
            if self.sc and (self.fin() or self.fim() or self.jun() or self.jms() or self.jcn() or self.isz()):
                self.sc = 0
                if self.jcn():
                    self.setJCNCond()
                    self.condw.v = self.cond
                    #print(self.timing.cycle, "condJCN", self.cond)
                if self.isz():
                    self.cond = ~self.alu.addZero() & 1
                    self.condw.v = self.cond
                    #print(self.timing.cycle, "condISZ", self.cond)
            else:
                self.sc = 1

        @M12clk2
        def _():
            if self.sc:
                self.opr = self.data.v

        @M22clk2
        def _():
            if self.sc:
                self.opa = self.data.v


    # C1 = 0 Do not invert jump condition
    # C1 = 1 Invert jump condition
    # C2 = 1 Jump if the accumulator content is zero
    # C3 = 1 Jump if the carry/link content is 1
    # C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
    def setJCNCond(self):
        z = self.alu.accZero()
        c = self.alu.carryOne()
        t = self.ioc.testZero()

        #print(self.opa, "z", z, "c", c, "t", t)
        invert = (self.opa & 0b1000) >> 3
        (zero, cy, test) = (self.opa & 0b0100, self.opa & 0b0010, self.opa & 0b0001)
        self.cond = 0
        if zero and (z ^ invert):
            self.cond = 1
        elif cy and (c ^ invert):
            self.cond = 1
        elif test and (t ^ invert):
            self.cond = 1


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


    def dump(self):
        print("OPR/OPA:{:04b}/{:04b}  SC:{}".format(self.opr, self.opa, self.sc), end = '')